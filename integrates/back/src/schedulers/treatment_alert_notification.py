from aioextensions import (
    collect,
)
from context import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
)
from custom_exceptions import (
    UnableToSendMail,
)
from custom_utils import (
    datetime as datetime_utils,
)
from custom_utils.findings import (
    get_group_findings,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decorators import (
    retry_on_exceptions,
)
from findings import (
    domain as findings_domain,
)
import logging
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from mailer.groups import (
    send_mail_treatment_alert,
)
from mailer.utils import (
    get_group_emails_by_notification,
    get_organization_name,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
    TypedDict,
)

logging.config.dictConfig(LOGGING)

# Constants
DAYS_TO_EXPIRING = 7
LOGGER = logging.getLogger(__name__)

mail_treatment_alert = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=3,
    sleep_seconds=2,
)(send_mail_treatment_alert)


class ExpiringDataType(TypedDict):
    org_name: str
    email_to: tuple[str, ...]
    group_expiring_findings: tuple[tuple[str, dict[str, dict[str, int]]], ...]


def days_to_end(date: datetime) -> int:
    return (date - datetime_utils.get_utc_now()).days


async def expiring_vulnerabilities(
    loaders: Dataloaders, finding: Finding
) -> dict[str, dict[str, int]]:
    vulnerabilities: list[
        Vulnerability
    ] = await findings_domain.get_open_vulnerabilities(loaders, finding.id)
    return {
        finding.id: {
            f"{vulnerability.state.where}"
            + f" ({vulnerability.state.specific})": days_to_end(
                vulnerability.treatment.accepted_until
            )
            for vulnerability in vulnerabilities
            if vulnerability.treatment
            and vulnerability.treatment.status
            == VulnerabilityTreatmentStatus.ACCEPTED
            and (end_date := vulnerability.treatment.accepted_until)
            and days_to_end(end_date) in range(7)
        }
    }


async def findings_close_to_expiring(
    loaders: Dataloaders, group_name: str
) -> tuple[tuple[str, dict[str, dict[str, int]]], ...]:
    findings = await get_group_findings(group_name=group_name, loaders=loaders)
    finding_types = list(finding.title for finding in findings)
    vulnerabilities = await collect(
        [expiring_vulnerabilities(loaders, finding) for finding in findings]
    )

    findings_to_expiring = list(zip(finding_types, vulnerabilities))
    return tuple(
        (finding_type, data)
        for finding_type, data in findings_to_expiring
        if list(data.values())[0]
    )


def unique_emails(
    expiring_data: dict[str, ExpiringDataType],
    email_list: tuple[str, ...],
) -> tuple[str, ...]:
    if expiring_data:
        email_list += expiring_data.popitem()[1]["email_to"]
        return unique_emails(expiring_data, email_list)

    return tuple(set(email_list))


async def send_temporal_treatment_report() -> None:
    loaders: Dataloaders = get_new_context()
    groups_names = await orgs_domain.get_all_active_group_names(loaders)

    if FI_ENVIRONMENT == "production":
        groups_names = [
            group
            for group in groups_names
            if group not in FI_TEST_PROJECTS.split(",")
        ]

    groups_org_names = await collect(
        [
            get_organization_name(loaders, group_name)
            for group_name in groups_names
        ]
    )

    groups_stakeholders_email: tuple[list[str], ...] = await collect(
        [
            get_group_emails_by_notification(
                loaders=loaders,
                group_name=group_name,
                notification="vulnerabilities_expiring",
            )
            for group_name in groups_names
        ]
    )

    groups_expiring_findings = await collect(
        [
            findings_close_to_expiring(loaders, group_name)
            for group_name in groups_names
        ]
    )

    groups_data: dict[str, ExpiringDataType] = dict(
        zip(
            groups_names,
            [
                ExpiringDataType(
                    org_name=org_name,
                    email_to=tuple(email_to),
                    group_expiring_findings=tuple(
                        sorted(
                            expiring_findings,
                            key=lambda exp_finding: exp_finding[0],
                        )
                    ),
                )
                for org_name, email_to, expiring_findings in zip(
                    groups_org_names,
                    groups_stakeholders_email,
                    groups_expiring_findings,
                )
            ],
        )
    )

    groups_data = {
        group_name: data
        for (group_name, data) in groups_data.items()
        if data["email_to"] and data["group_expiring_findings"]
    }

    for email in unique_emails(dict(groups_data), ()):
        user_content: dict[str, Any] = {
            "groups_data": {
                group_name: {
                    "org_name": data["org_name"],
                    "finding_title": list(findings_data[0]),
                    "group_expiring_findings": list(findings_data[1]),
                }
                for group_name, data in groups_data.items()
                if email in data["email_to"]
                and (
                    findings_data := tuple(
                        zip(*data["group_expiring_findings"])
                    )
                )
            }
        }

        try:
            await mail_treatment_alert(
                loaders=loaders,
                context=user_content,
                email_to=email,
                email_cc=[],
            )
            LOGGER.info(
                "Temporary treatment alert email sent",
                extra={"extra": {"email": email}},
            )
        except KeyError:
            LOGGER.info(
                "Key error, Temporary treatment alert email not sent",
                extra={"extra": {"email": email}},
            )
            continue
    LOGGER.info("Temporary treatment alert execution finished.")


async def main() -> None:
    await send_temporal_treatment_report()
