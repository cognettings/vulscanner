# pylint: disable=consider-using-f-string
from aioextensions import (
    collect,
)
import authz
from context import (
    FI_ENVIRONMENT,
    FI_MAIL_COS,
    FI_MAIL_CTO,
    FI_TEST_ORGS,
    FI_TEST_PROJECTS,
)
from custom_exceptions import (
    UnableToSendMail,
)
from custom_utils import (
    cvss as cvss_utils,
    datetime as datetime_utils,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    date,
    datetime,
)
from db_model.findings.enums import (
    FindingVerificationStatus,
)
from db_model.findings.types import (
    Finding,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
    ToeInputsConnection,
)
from db_model.toe_lines.types import (
    GroupToeLinesRequest,
    ToeLinesConnection,
)
from db_model.toe_ports.types import (
    GroupToePortsRequest,
    ToePortsConnection,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from decimal import (
    Decimal,
)
from decorators import (
    retry_on_exceptions,
)
import logging
import logging.config
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from mailer import (
    groups as groups_mail,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


mail_numerator_report = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=3,
    sleep_seconds=2,
)(groups_mail.send_mail_numerator_report)


def _validate_date(date_attr: date, from_day: int, to_day: int) -> bool:
    validate_date: bool = (
        datetime_utils.get_now_minus_delta(days=from_day).date()
        <= date_attr
        < datetime_utils.get_now_minus_delta(days=to_day).date()
    )
    return validate_date


def _generate_count_fields() -> dict[str, Any]:
    fields: dict[str, Any] = {
        "count": {
            "past_day": 0,
            "today": 0,
        },
    }
    return fields


def _generate_fields() -> dict[str, Any]:
    fields: dict[str, Any] = {
        "enumerated_inputs": _generate_count_fields(),
        "enumerated_ports": _generate_count_fields(),
        "verified_inputs": _generate_count_fields(),
        "verified_ports": _generate_count_fields(),
        "loc": _generate_count_fields(),
        "reattacked": _generate_count_fields(),
        "released": _generate_count_fields(),
        "sorts_verified_lines": _generate_count_fields(),
        "sorts_verified_lines_priority": _generate_count_fields(),
        "sorts_verified_lines_priority_avg": _generate_count_fields(),
        "submitted": _generate_count_fields(),
        "max_cvss": 0.0,
        "groups": {},
    }
    return fields


def _generate_group_fields() -> dict[str, Any]:
    fields: dict[str, Any] = {
        "verified_inputs": 0,
        "verified_ports": 0,
        "enumerated_inputs": 0,
        "enumerated_ports": 0,
        "loc": 0,
        "reattacked": 0,
        "released": 0,
        "sorts_verified_lines": 0,
        "sorts_verified_lines_priority": 0,
        "sorts_verified_lines_priority_avg": 0,
        "submitted": 0,
        "subscription": "-",
    }
    return fields


def _common_write_to_dict_today(
    *,
    content: dict[str, Any],
    user_email: str,
    field: str,
    group: str,
    to_add: int = 1,
) -> None:
    if not dict(content[user_email]["groups"]).get(group):
        content[user_email]["groups"][group] = _generate_group_fields()

    content[user_email]["groups"][group][field] = (
        int(content[user_email]["groups"][group][field]) + to_add
    )

    content[user_email][field]["count"]["today"] = (
        int(content[user_email][field]["count"]["today"]) + to_add
    )


def _common_write_to_dict_yesterday(
    *,
    content: dict[str, Any],
    user_email: str,
    field: str,
    to_add: int = 1,
) -> None:
    content[user_email][field]["count"]["past_day"] = (
        int(content[user_email][field]["count"]["past_day"]) + to_add
    )


def _set_severity_released(
    content: dict[str, Any],
    cvss: Decimal,
    field: str,
    user_email: str,
) -> None:
    if field in ["released"]:
        _max_severity_released(content, cvss, user_email)


def _common_generate_count_report(
    *,
    content: dict[str, Any],
    date_range: int,
    date_report: datetime | None,
    field: str,
    group: str,
    to_add: int = 1,
    user_email: str,
    allowed_users: list[str],
    cvss: Decimal = Decimal("0.0"),
) -> None:
    if user_email in allowed_users and date_report:
        date_format: date = datetime_utils.as_zone(date_report).date()
        is_valid_date = _validate_date(date_format, date_range, date_range - 1)

        if not content.get(user_email):
            content[user_email] = _generate_fields()

        if is_valid_date:
            _common_write_to_dict_today(
                content=content,
                user_email=user_email,
                field=field,
                group=group,
                to_add=to_add,
            )

            _set_severity_released(content, cvss, field, user_email)

        else:
            if datetime_utils.get_now().weekday() == 1:
                date_range = 3
            if _validate_date(date_format, date_range + 1, date_range):
                _common_write_to_dict_yesterday(
                    content=content,
                    user_email=user_email,
                    field=field,
                    to_add=to_add,
                )


async def _finding_reattacked(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    finding_id: str,
    group: str,
    date_range: int,
    content: dict[str, Any],
    users_email: list[str],
) -> None:
    historic_verification = await loaders.finding_historic_verification.load(
        finding_id
    )
    for verification in historic_verification:
        if (
            verification.vulnerability_ids
            and verification.status == FindingVerificationStatus.VERIFIED
        ):
            _common_generate_count_report(
                content=content,
                date_range=date_range,
                date_report=verification.modified_date,
                field="reattacked",
                group=group,
                to_add=len(verification.vulnerability_ids),
                user_email=verification.modified_by,
                allowed_users=users_email,
            )


async def _finding_vulns_released(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    finding: Finding,
    group: str,
    date_range: int,
    content: dict[str, Any],
    users_email: list[str],
) -> None:
    cvss = cvss_utils.get_severity_score(finding.severity)
    vulnerabilities = await loaders.finding_vulnerabilities.load(finding.id)
    historic_state_loader = loaders.vulnerability_historic_state
    for vuln in vulnerabilities:
        historic_state_loader.clear(vuln.id)
        historic_state = await historic_state_loader.load(vuln.id)
        for state in historic_state:
            if state.status == VulnerabilityStateStatus.VULNERABLE:
                _common_generate_count_report(
                    content=content,
                    date_range=date_range,
                    date_report=state.modified_date,
                    field="released",
                    group=group,
                    user_email=vuln.hacker_email,
                    allowed_users=users_email,
                    cvss=cvss,
                )


async def _finding_vulns_submitted(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    finding: Finding,
    group: str,
    date_range: int,
    content: dict[str, Any],
    users_email: list[str],
) -> None:
    cvss = cvss_utils.get_severity_score(finding.severity)
    vulnerabilities = await loaders.finding_vulnerabilities.load(finding.id)
    historic_state_loader = loaders.vulnerability_historic_state
    for vuln in vulnerabilities:
        historic_state_loader.clear(vuln.id)
        historic_state = await historic_state_loader.load(vuln.id)
        for state in historic_state:
            if state.status == VulnerabilityStateStatus.SUBMITTED:
                _common_generate_count_report(
                    content=content,
                    date_range=date_range,
                    date_report=state.modified_date,
                    field="submitted",
                    group=group,
                    user_email=vuln.hacker_email,
                    allowed_users=users_email,
                    cvss=cvss,
                )


def _max_severity_released(
    content: dict[str, Any],
    cvss: Decimal,
    user_email: str,
) -> None:
    if content[user_email]["max_cvss"] < cvss:
        content[user_email]["max_cvss"] = cvss


async def _finding_content(
    loaders: Dataloaders,
    group: str,
    date_range: int,
    content: dict[str, Any],
    users_email: list[str],
) -> None:
    findings = await loaders.group_findings.load(group)
    for finding in findings:
        await collect(
            [
                _finding_reattacked(
                    loaders,
                    finding.id,
                    group,
                    date_range,
                    content,
                    users_email,
                ),
                _finding_vulns_released(
                    loaders, finding, group, date_range, content, users_email
                ),
                _finding_vulns_submitted(
                    loaders, finding, group, date_range, content, users_email
                ),
            ]
        )

    LOGGER.info("- finding report generated in group %s", group)


async def _toe_input_content(
    loaders: Dataloaders,
    group: str,
    date_range: int,
    content: dict[str, Any],
    users_email: list[str],
) -> None:
    group_toe_inputs: ToeInputsConnection = (
        await loaders.group_toe_inputs.load(
            GroupToeInputsRequest(group_name=group)
        )
    )
    for toe_inputs in group_toe_inputs.edges:
        _common_generate_count_report(
            content=content,
            date_range=date_range,
            date_report=toe_inputs.node.state.seen_at,
            field="enumerated_inputs",
            group=group,
            user_email=toe_inputs.node.state.seen_first_time_by,
            allowed_users=users_email,
        )

        _common_generate_count_report(
            content=content,
            date_range=date_range,
            date_report=toe_inputs.node.state.attacked_at,
            field="verified_inputs",
            group=group,
            user_email=toe_inputs.node.state.attacked_by,
            allowed_users=users_email,
        )

    LOGGER.info("- toe input report generated in group %s", group)


async def _toe_line_content(
    loaders: Dataloaders,
    group: str,
    date_range: int,
    content: dict[str, Any],
    users_email: list[str],
) -> None:
    group_toe_lines: ToeLinesConnection = await loaders.group_toe_lines.load(
        GroupToeLinesRequest(group_name=group)
    )
    priority_factor_list = [
        toe_lines.node.state.sorts_priority_factor
        for toe_lines in group_toe_lines.edges
        if toe_lines.node.state.sorts_priority_factor is not None
        and toe_lines.node.state.sorts_priority_factor != -1
        and isinstance(toe_lines.node.state.sorts_priority_factor, int)
    ]

    for toe_lines in group_toe_lines.edges:
        _common_generate_count_report(
            content=content,
            date_range=date_range,
            date_report=toe_lines.node.state.attacked_at,
            field="loc",
            group=group,
            user_email=toe_lines.node.state.attacked_by,
            to_add=toe_lines.node.state.attacked_lines,
            allowed_users=users_email,
        )
        if (
            toe_lines.node.state.sorts_priority_factor != -1
            and toe_lines.node.state.sorts_priority_factor is not None
            and isinstance(toe_lines.node.state.sorts_priority_factor, int)
        ):
            try:
                normalized_priority_factor = (
                    (
                        toe_lines.node.state.sorts_priority_factor
                        - min(priority_factor_list)
                    )
                    / (max(priority_factor_list) - min(priority_factor_list))
                    * 100
                )
            except ZeroDivisionError:
                normalized_priority_factor = (
                    toe_lines.node.state.sorts_priority_factor
                )
            _common_generate_count_report(
                content=content,
                date_range=date_range,
                date_report=toe_lines.node.state.attacked_at,
                field="sorts_verified_lines",
                group=group,
                user_email=toe_lines.node.state.attacked_by,
                allowed_users=users_email,
            )
            _common_generate_count_report(
                content=content,
                date_range=date_range,
                date_report=toe_lines.node.state.attacked_at,
                field="sorts_verified_lines_priority",
                group=group,
                user_email=toe_lines.node.state.attacked_by,
                to_add=int(normalized_priority_factor),
                allowed_users=users_email,
            )

    LOGGER.info("- toe lines report generated in group %s", group)


async def _toe_port_content(
    loaders: Dataloaders,
    group: str,
    date_range: int,
    content: dict[str, Any],
    users_email: list[str],
) -> None:
    group_toe_ports: ToePortsConnection = await loaders.group_toe_ports.load(
        GroupToePortsRequest(group_name=group)
    )
    for toe_inputs in group_toe_ports.edges:
        if toe_inputs.node.seen_first_time_by:
            _common_generate_count_report(
                content=content,
                date_range=date_range,
                date_report=toe_inputs.node.seen_at,
                field="enumerated_ports",
                group=group,
                user_email=toe_inputs.node.seen_first_time_by,
                allowed_users=users_email,
            )

        if toe_inputs.node.state.attacked_by:
            _common_generate_count_report(
                content=content,
                date_range=date_range,
                date_report=toe_inputs.node.state.attacked_at,
                field="verified_ports",
                group=group,
                user_email=toe_inputs.node.state.attacked_by,
                allowed_users=users_email,
            )

    LOGGER.info("- toe port report generated in group %s", group)


async def get_stakeholders_email_by_roles(
    *,
    loaders: Dataloaders,
    group_name: str,
    roles: set[str],
) -> list[str]:
    stakeholders_access = await loaders.group_stakeholders_access.load(
        group_name
    )
    stakeholders = [
        stakeholder_access.email for stakeholder_access in stakeholders_access
    ]
    stakeholder_roles = await collect(
        tuple(
            authz.get_group_level_role(loaders, stakeholder, group_name)
            for stakeholder in stakeholders
        )
    )
    email_list = [
        str(stakeholder)
        for stakeholder, stakeholder_role in zip(
            stakeholders, stakeholder_roles
        )
        if stakeholder_role in roles
    ]
    return email_list


def _get_average(count: int, observations: int) -> float:
    try:
        average = count / observations
    except ZeroDivisionError:
        average = 0
    return average


def _generate_field_average(
    content: dict[str, Any],
    user_email: str,
    field_of_avg: str,
    field_of_sum: str,
    field_of_observations: str,
) -> None:
    user_data = content[user_email]
    user_data[field_of_avg]["count"]["today"] = _get_average(
        count=user_data[field_of_sum]["count"]["today"],
        observations=user_data[field_of_observations]["count"]["today"],
    )
    user_data[field_of_avg]["count"]["past_day"] = _get_average(
        count=user_data[field_of_sum]["count"]["past_day"],
        observations=user_data[field_of_observations]["count"]["past_day"],
    )

    for group_name in user_data["groups"]:
        content[user_email]["groups"][group_name][field_of_avg] = _get_average(
            count=user_data["groups"][group_name][field_of_sum],
            observations=user_data["groups"][group_name][
                field_of_observations
            ],
        )


async def _generate_numerator_report(
    loaders: Dataloaders, groups_names: list[str], date_range: int
) -> dict[str, Any]:
    content: dict[str, Any] = {}
    allowed_roles: set[str] = {
        "architect",
        "hacker",
        "reattacker",
        "resourcer",
        "reviewer",
    }

    for group in groups_names:
        users_email: list[str] = await get_stakeholders_email_by_roles(
            loaders=loaders,
            group_name=group,
            roles=allowed_roles,
        )
        await collect(
            [
                _toe_input_content(
                    loaders, group, date_range, content, users_email
                ),
                _toe_line_content(
                    loaders, group, date_range, content, users_email
                ),
                _toe_port_content(
                    loaders, group, date_range, content, users_email
                ),
                _finding_content(
                    loaders, group, date_range, content, users_email
                ),
            ]
        )

    for user_email, user_data in content.items():
        _generate_field_average(
            content=content,
            user_email=user_email,
            field_of_avg="sorts_verified_lines_priority_avg",
            field_of_sum="sorts_verified_lines_priority",
            field_of_observations="sorts_verified_lines",
        )
        for group_name, group_data in user_data["groups"].items():
            group_data = await loaders.group.load(group_name)
            user_data["groups"][group_name]["subscription"] = (
                "o"
                if group_data and group_data.state.type == "ONESHOT"
                else "c"
            )

    LOGGER.info("- general report successfully generated")

    return content


def get_percent(num_a: float, num_b: float) -> str:
    try:
        variation: float = num_a / num_b
    except TypeError:
        return "-"
    except ValueError:
        return "-"
    except ZeroDivisionError:
        return "-"
    return "{:+.0%}".format(variation)


def _generate_count_and_variation(content: dict[str, Any]) -> dict[str, Any]:
    count_and_variation: dict[str, Any] = {
        key: {
            "count": (count := value["count"])["today"],
            "variation": get_percent(
                count["today"] - count["past_day"],
                count["past_day"],
            ),
        }
        for key, value in content.items()
    }

    return count_and_variation


async def _send_mail_report(
    loaders: Dataloaders,
    content: dict[str, Any],
    report_date: date,
    responsible: str,
) -> None:
    groups_content = content.pop("groups")
    max_cvss = content.pop("max_cvss")
    count_var_report: dict[str, Any] = _generate_count_and_variation(content)

    context: dict[str, Any] = {
        "count_var_report": count_var_report,
        "groups": groups_content,
        "max_cvss": max_cvss,
        "responsible": responsible,
    }

    await mail_numerator_report(
        loaders=loaders,
        context=context,
        email_to=[responsible],
        email_cc=[FI_MAIL_COS, FI_MAIL_CTO],
        report_date=report_date,
    )


async def _validate_content(
    content: dict[str, Any], report_date: date, loaders: Dataloaders
) -> None:
    if content:
        for user_email, user_content in content.items():
            try:
                await _send_mail_report(
                    loaders, user_content, report_date, user_email
                )
            except KeyError:
                LOGGER.info(
                    "- key error, email not sent",
                    extra={"extra": {"email": user_email}},
                )
                continue
    else:
        LOGGER.info("- numerator report NOT sent")


async def send_numerator_report() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = await orgs_domain.get_all_active_group_names(loaders)
    test_group_names = FI_TEST_PROJECTS.split(",")

    async for _, org_name, org_groups_names in (
        orgs_domain.iterate_organizations_and_groups(loaders)
    ):
        for group_name in org_groups_names:
            if (
                org_name in FI_TEST_ORGS.lower().split(",")
            ) and group_name not in test_group_names:
                test_group_names += org_groups_names
    date_range = 3 if datetime_utils.get_now().weekday() == 0 else 1
    report_date = datetime_utils.get_now_minus_delta(days=date_range).date()

    if FI_ENVIRONMENT == "production":
        group_names = [
            group for group in group_names if group not in test_group_names
        ]
    LOGGER.info("info", extra={"extra": {"info": group_names}})

    content: dict[str, Any] = await _generate_numerator_report(
        loaders, group_names, date_range
    )

    await _validate_content(content, report_date, loaders)


async def main() -> None:
    await send_numerator_report()
