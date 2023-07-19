from aioextensions import (
    collect,
)
from collections import (
    defaultdict,
)
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
    datetime as datetime_utils,
)
from custom_utils.vulnerabilities import (
    is_machine_vuln,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.events.types import (
    GroupEventsRequest,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
)
from decorators import (
    retry_on_exceptions,
)
from group_access.domain import (
    get_stakeholders_email_by_roles,
)
import logging
import logging.config
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from mailer import (
    vulnerabilities as vulns_mail,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
from typing import (
    Literal,
    TypedDict,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


mail_reviewer_progress_report = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=3,
    sleep_seconds=2,
)(vulns_mail.send_mail_reviewer_progress_report)


class OldestRejected(TypedDict):
    datetime: datetime
    finding_id: str
    finding_title: str
    group_name: str
    id: str
    org_name: str
    specific: str
    where: str


class StakeholderInfo(TypedDict):
    rejected_count: int
    vulnerable_count: int


class GlobalInfo(TypedDict):
    oldest_rejected: OldestRejected | None
    rejected_count: int
    submitted_count: int


class EmailContent(TypedDict):
    stakeholders_info: dict[str, StakeholderInfo]
    global_info: GlobalInfo


def _get_vulnerability_state_in_report_date(
    days_before: int, historic_state: list[VulnerabilityState]
) -> VulnerabilityState | None:
    report_date = datetime_utils.get_now_minus_delta(days=days_before).date()
    state_in_report_date = max(
        (
            state
            for state in historic_state
            if datetime_utils.as_zone(state.modified_date).date()
            <= report_date
        ),
        key=lambda state: state.modified_date,
        default=None,
    )

    return state_in_report_date


def _count_field_by_stakeholder(
    *,
    email_content: EmailContent,
    days_before: int,
    date_report: datetime,
    field: Literal["rejected_count", "vulnerable_count"],
    to_add: int = 1,
    stakeholder_email: str,
    allowed_stakeholders: set[str],
) -> None:
    if stakeholder_email in allowed_stakeholders:
        count_report = bool(
            datetime_utils.get_now_minus_delta(days=days_before).date()
            == datetime_utils.as_zone(date_report).date()
        )
        if count_report:
            email_content["stakeholders_info"][stakeholder_email][
                field
            ] += to_add


def _count_vulnerability_fields_by_stakeholder(
    days_before: int,
    email_content: EmailContent,
    historic_state: list[VulnerabilityState],
    stakeholder_emails: set[str],
    vulnerability: Vulnerability,
) -> None:
    for state in historic_state:
        if state.status is VulnerabilityStateStatus.REJECTED:
            _count_field_by_stakeholder(
                email_content=email_content,
                days_before=days_before,
                date_report=state.modified_date,
                field="rejected_count",
                stakeholder_email=vulnerability.state.modified_by,
                allowed_stakeholders=stakeholder_emails,
            )
        if state.status is VulnerabilityStateStatus.VULNERABLE:
            _count_field_by_stakeholder(
                email_content=email_content,
                days_before=days_before,
                date_report=state.modified_date,
                field="vulnerable_count",
                stakeholder_email=vulnerability.state.modified_by,
                allowed_stakeholders=stakeholder_emails,
            )


def _count_vulnerability_field_in_report_date(
    days_before: int,
    email_content: EmailContent,
    historic_state: list[VulnerabilityState],
    vulnerability: Vulnerability,
) -> None:
    if is_machine_vuln(vulnerability):
        return
    state_in_report_date = _get_vulnerability_state_in_report_date(
        days_before, historic_state
    )
    if state_in_report_date:
        if state_in_report_date.status is VulnerabilityStateStatus.REJECTED:
            email_content["global_info"]["rejected_count"] += 1
        if state_in_report_date.status is VulnerabilityStateStatus.SUBMITTED:
            email_content["global_info"]["submitted_count"] += 1


def _format_where(
    vulnerability: Vulnerability,
    root_nicknames: dict[str, str],
) -> str:
    if (
        vulnerability.type is VulnerabilityType.LINES
        and vulnerability.root_id
        and (root_nickname := root_nicknames.get(vulnerability.root_id))
    ):
        return f"{root_nickname}/{vulnerability.state.where}"

    return vulnerability.state.where


def _set_oldest_rejected_vulnerability(  # pylint: disable=too-many-arguments
    days_before: int,
    email_content: EmailContent,
    finding: Finding,
    group_has_events: bool,
    historic_state: list[VulnerabilityState],
    root_nicknames: dict[str, str],
    vulnerability: Vulnerability,
) -> None:
    if group_has_events or is_machine_vuln(vulnerability):
        return
    state_in_report_date = _get_vulnerability_state_in_report_date(
        days_before, historic_state
    )
    if state_in_report_date:
        if state_in_report_date.status is VulnerabilityStateStatus.REJECTED:
            if (
                email_content["global_info"]["oldest_rejected"]
                and email_content["global_info"]["oldest_rejected"]["datetime"]
                > state_in_report_date.modified_date
            ) or not email_content["global_info"]["oldest_rejected"]:
                email_content["global_info"][
                    "oldest_rejected"
                ] = OldestRejected(
                    datetime=state_in_report_date.modified_date,
                    finding_id=vulnerability.finding_id,
                    finding_title=finding.title,
                    group_name=vulnerability.group_name,
                    id=vulnerability.id,
                    org_name=vulnerability.organization_name,
                    specific=vulnerability.state.specific,
                    where=_format_where(vulnerability, root_nicknames),
                )


async def _vulnerabilities_report(
    *,
    days_before: int,
    email_content: EmailContent,
    group_name: str,
    loaders: Dataloaders,
    stakeholder_emails: set[str],
) -> None:
    findings = await loaders.group_findings.load(group_name)
    group_has_events = bool(
        await loaders.group_events.load(
            GroupEventsRequest(group_name=group_name, is_solved=False)
        )
    )
    vulnerabilities = await loaders.finding_vulnerabilities.load_many_chained(
        [finding.id for finding in findings]
    )
    vulnerability_historic_states = (
        await loaders.vulnerability_historic_state.load_many(
            [vulnerability.id for vulnerability in vulnerabilities]
        )
    )
    finding_map = {finding.id: finding for finding in findings}
    root_nicknames = {
        root.id: root.state.nickname
        for root in await loaders.group_roots.load(group_name)
    }
    for vulnerability, historic_state in zip(
        vulnerabilities, vulnerability_historic_states, strict=True
    ):
        _count_vulnerability_fields_by_stakeholder(
            days_before,
            email_content,
            historic_state,
            stakeholder_emails,
            vulnerability,
        )
        _count_vulnerability_field_in_report_date(
            days_before, email_content, historic_state, vulnerability
        )
        _set_oldest_rejected_vulnerability(
            days_before,
            email_content,
            finding_map[vulnerability.finding_id],
            group_has_events,
            historic_state,
            root_nicknames,
            vulnerability,
        )


async def _send_emails(
    days_before: int,
    email_content: EmailContent,
    loaders: Dataloaders,
) -> None:
    report_date = datetime_utils.get_now_minus_delta(days=days_before).date()
    await collect(
        tuple(
            mail_reviewer_progress_report(
                loaders=loaders,
                context=dict(
                    responsible=responsible,
                    global_info=email_content["global_info"],
                    stakeholder_info=email_content["stakeholders_info"][
                        responsible
                    ],
                ),
                email_cc=[FI_MAIL_COS, FI_MAIL_CTO],
                email_to=[responsible],
                responsible=responsible,
                report_date=report_date,
            )
            for responsible in email_content["stakeholders_info"]
        )
    )


async def _load_report_info_by_group(
    days_before: int,
    email_content: EmailContent,
    allowed_roles: set[str],
    group_name: str,
) -> None:
    loaders: Dataloaders = get_new_context()
    stakeholder_emails = set(
        await get_stakeholders_email_by_roles(
            loaders=loaders,
            group_name=group_name,
            roles=allowed_roles,
        )
    )
    await _vulnerabilities_report(
        days_before=days_before,
        email_content=email_content,
        group_name=group_name,
        loaders=loaders,
        stakeholder_emails=stakeholder_emails,
    )


async def _generate_progress_report(
    *,
    loaders: Dataloaders,
    group_names: set[str],
    days_before: int,
) -> None:
    email_content: EmailContent = dict(
        global_info=dict(
            oldest_rejected=None,
            rejected_count=0,
            submitted_count=0,
        ),
        stakeholders_info=defaultdict(
            lambda: dict(rejected_count=0, vulnerable_count=0)
        ),
    )
    allowed_roles = {"reviewer"}
    await collect(
        tuple(
            _load_report_info_by_group(
                days_before, email_content, allowed_roles, group_name
            )
            for group_name in group_names
        ),
        workers=5,
    )
    await _send_emails(days_before, email_content, loaders)


async def reviewers_progress_report() -> None:
    loaders: Dataloaders = get_new_context()
    active_groups = await orgs_domain.get_all_active_groups(loaders)
    test_group_names = set(FI_TEST_PROJECTS.split(","))
    test_organization_names = set(FI_TEST_ORGS.lower().split(","))
    test_organization_ids = set(
        organization.id
        for organization in await loaders.organization.load_many(
            test_organization_names
        )
        if organization
    )
    group_names_to_report = {
        group.name
        for group in active_groups
        if (
            group.name not in test_group_names
            and group.organization_id not in test_organization_ids
        )
        or FI_ENVIRONMENT == "development"
    }
    days_before = 1
    await _generate_progress_report(
        loaders=loaders,
        group_names=group_names_to_report,
        days_before=days_before,
    )


async def main() -> None:
    await reviewers_progress_report()
