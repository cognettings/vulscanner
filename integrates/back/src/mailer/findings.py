from .common import (
    COMMENTS_TAG,
    GENERAL_TAG,
    send_mails_async,
    VERIFY_TAG,
)
import authz
from context import (
    BASE_URL,
    FI_MAIL_CUSTOMER_SUCCESS,
    FI_MAIL_REVIEWERS,
)
from custom_exceptions import (
    GroupNotFound,
)
from custom_utils import (
    validations,
)
from dataloaders import (
    Dataloaders,
)
from db_model.enums import (
    Notification,
    Source,
    StateRemovalJustification,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateReason,
)
from decimal import (
    Decimal,
)
from group_access import (
    domain as group_access_domain,
)
from mailer.enums import (
    MailVulnerabilityReportState,
)
from mailer.utils import (
    get_organization_name,
    get_vulnerability_report_group_emails,
)
from typing import (
    Any,
)


async def send_mail_comment(  # pylint: disable=too-many-locals
    *,
    loaders: Dataloaders,
    comment_data: FindingComment,
    user_mail: str,
    finding_id: str,
    finding_title: str,
    recipients: list[str],
    group_name: str,
    is_finding_released: bool,
) -> None:
    org_name = await get_organization_name(loaders, group_name)
    group = await loaders.group.load(group_name)
    if not group:
        raise GroupNotFound()
    has_machine: bool = group.state.has_machine
    has_squad: bool = group.state.has_squad
    type_ = comment_data.comment_type
    type_fmt = (
        "consulting"
        if type_ in [CommentType.COMMENT, CommentType.VERIFICATION]
        else "observation"
    )
    email_context: dict[str, Any] = {
        "comment": comment_data.content.splitlines(),
        "comment_type": type_fmt,
        "comment_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/"
            f'{"vulns" if is_finding_released else "drafts"}/{finding_id}/'
            f"{type_fmt}"
        ),
        "finding_id": finding_id,
        "finding_name": finding_title,
        "parent": str(comment_data.parent_id),
        "group": group_name,
        "has_machine": has_machine,
        "has_squad": has_squad,
        "user_email": user_mail,
    }

    stakeholders = await loaders.stakeholder.load_many(recipients)
    stakeholders_email = [
        stakeholder.email
        for stakeholder in stakeholders
        if stakeholder
        and Notification.NEW_COMMENT
        in stakeholder.state.notifications_preferences.email
    ]
    reviewers = FI_MAIL_REVIEWERS.split(",")
    customer_success_recipients = FI_MAIL_CUSTOMER_SUCCESS.split(",")
    if type_ == CommentType.OBSERVATION:
        await send_mails_async(
            loaders,
            [*stakeholders_email, *customer_success_recipients, *reviewers],
            context=email_context,
            tags=COMMENTS_TAG,
            subject=(
                "Fluid Attacks | New observation"
                f" in [{finding_title}] for [{group_name}]"
            ),
            template_name="new_comment",
        )


async def send_mail_remove_finding(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    finding_id: str,
    finding_name: str,
    group_name: str,
    discoverer_email: str,
    justification: StateRemovalJustification,
) -> None:
    justification_dict = {
        StateRemovalJustification.DUPLICATED: "It is duplicated",
        StateRemovalJustification.FALSE_POSITIVE: "It is a false positive",
        StateRemovalJustification.NO_JUSTIFICATION: "",
        StateRemovalJustification.NOT_REQUIRED: "Finding not required",
        StateRemovalJustification.REPORTING_ERROR: "It is a reporting error",
    }
    recipients = FI_MAIL_REVIEWERS.split(",")
    user_role = await authz.get_group_level_role(
        loaders, discoverer_email, group_name
    )
    mail_context: dict[str, Any] = {
        "hacker_email": discoverer_email,
        "finding_name": finding_name,
        "finding_id": finding_id,
        "justification": justification_dict[justification],
        "group": group_name,
        "user_role": user_role.replace("_", " "),
    }
    await send_mails_async(
        loaders,
        recipients,
        context=mail_context,
        tags=GENERAL_TAG,
        subject=(
            "Fluid Attacks | Type of vulnerability removed "
            f"[{finding_name}] in [{group_name}]"
        ),
        template_name="delete_finding",
    )


async def send_mail_remediate_finding(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    user_email: str,
    finding_id: str,
    finding_name: str,
    group_name: str,
    justification: str,
) -> None:
    org_name = await get_organization_name(loaders, group_name)
    recipients = await group_access_domain.get_reattackers(loaders, group_name)
    stakeholders = await loaders.stakeholder.load_many(recipients)
    stakeholders_email = [
        stakeholder.email
        for stakeholder in stakeholders
        if stakeholder
        and Notification.REMEDIATE_FINDING
        in stakeholder.state.notifications_preferences.email
    ]
    mail_context: dict[str, Any] = {
        "group": group_name.lower(),
        "organization": org_name,
        "finding_name": finding_name,
        "finding_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}"
            f"/vulns/{finding_id}/locations"
        ),
        "finding_id": finding_id,
        "user_email": user_email,
        "solution_description": justification.splitlines(),
    }
    await send_mails_async(
        loaders,
        stakeholders_email,
        context=mail_context,
        tags=VERIFY_TAG,
        subject="Fluid Attacks | New remediation for "
        + f"[{finding_name}] in [{group_name}]",
        template_name="remediate_finding",
    )


async def send_mail_vulnerability_report(  # pylint: disable=too-many-locals
    *,
    loaders: Dataloaders,
    group_name: str = "",
    finding_title: str,
    finding_id: str,
    vulnerabilities_properties: dict[str, dict[str, dict[str, str]]],
    responsible: str,
    severity_score: Decimal,
    severity_level: str,
    state: MailVulnerabilityReportState = (
        MailVulnerabilityReportState.REPORTED
    ),
    remaining_exposure: int | None = None,
) -> None:
    group_findings = await loaders.group_findings.load(group_name)
    org_name = await get_organization_name(loaders, group_name)
    stakeholders_email = await get_vulnerability_report_group_emails(
        loaders=loaders,
        group_name=group_name,
        severity_score=severity_score,
        group_findings=group_findings,
    )
    email_context: dict[str, Any] = {
        "finding": finding_title,
        "group": group_name.lower(),
        "finding_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/vulns/"
            f"{finding_id}/locations"
        ),
        "vulns_props": vulnerabilities_properties,
        "responsible": responsible,
        "remaining_exposure": remaining_exposure,
        "severity_score": severity_score,
        "severity_level": severity_level.capitalize(),
        "state": str(state.value).lower(),
        "is_escape": False,
    }
    await send_mails_async(
        loaders,
        email_to=stakeholders_email,
        context=email_context,
        tags=GENERAL_TAG,
        subject=(
            f"Fluid Attacks | {finding_title} {str(state.value).lower()} in"
            f" [{group_name}]."
        ),
        template_name="vulnerability_report",
    )
    if (state is MailVulnerabilityReportState.REPORTED) and any(
        map(
            lambda repo: any(
                map(
                    lambda id: vulnerabilities_properties[repo][id]["source"]
                    == Source.ESCAPE.value,
                    vulnerabilities_properties[repo].keys(),
                )
            ),
            vulnerabilities_properties.keys(),
        )
    ):
        email_context["is_escape"] = True
        group_stakeholders = await group_access_domain.get_group_stakeholders(
            loaders, group_name
        )
        recipients = [stakeholder.email for stakeholder in group_stakeholders]
        stakeholders = await loaders.stakeholder.load_many(recipients)
        stakeholders_email = [
            stakeholder.email
            for stakeholder in stakeholders
            if stakeholder and validations.is_fluid_staff(stakeholder.email)
        ]
        await send_mails_async(
            loaders,
            email_to=stakeholders_email,
            context=email_context,
            tags=GENERAL_TAG,
            subject=(
                f"Fluid Attacks | {finding_title} "
                + f"{str(state.value).lower()} as"
                " escape in "
            )
            + f"[{group_name}].",
            template_name="vulnerability_report",
        )


async def send_mail_reject_vulnerability(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    finding: Finding,
    stakeholder_email: str,
    rejection_reasons: set[VulnerabilityStateReason],
    other_reason: str | None,
    vulnerabilities_properties: dict[str, dict[str, dict[str, str]]],
    severity_score: Decimal,
    severity_level: str,
    submitters_emails: set[str],
) -> None:
    org_name = await get_organization_name(loaders, finding.group_name)
    recipients = set(FI_MAIL_REVIEWERS.split(","))
    recipients.add(stakeholder_email)
    recipients.update(submitters_emails)
    explanations: dict[VulnerabilityStateReason, str] = {
        VulnerabilityStateReason.CONSISTENCY: (
            "There are consistency issues with the vulnerabilities, the"
            " severity or the evidence"
        ),
        VulnerabilityStateReason.EVIDENCE: "The evidence is insufficient",
        VulnerabilityStateReason.NAMING: (
            "The vulnerabilities should be submitted under another Finding "
            "type"
        ),
        VulnerabilityStateReason.OMISSION: (
            "More data should be gathered before submission"
        ),
        VulnerabilityStateReason.SCORING: "Faulty severity scoring",
        VulnerabilityStateReason.WRITING: "The writing could be improved",
        VulnerabilityStateReason.OTHER: other_reason.capitalize()
        if other_reason
        else "",
    }
    reasons: dict[str, str] = {
        str(reason.value).capitalize(): explanation
        for reason, explanation in explanations.items()
        if reason in rejection_reasons
    }
    email_context: dict[str, Any] = {
        "finding": finding.title,
        "finding_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{finding.group_name}"
            f"/vulns/{finding.id}/locations"
        ),
        "group": finding.group_name,
        "vulns_props": vulnerabilities_properties,
        "responsible": finding.hacker_email,
        "severity_score": severity_score,
        "severity_level": severity_level,
        "reasons": reasons,
    }
    await send_mails_async(
        loaders,
        list(recipients),
        context=email_context,
        tags=GENERAL_TAG,
        subject=(
            f"Fluid Attacks | Rejected location of [{finding.title}] in"
            f" [{finding.group_name}]"
        ),
        template_name="vulnerability_rejection",
    )


async def send_mail_submit_vulnerability(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    finding: Finding,
    responsible: str,
    vulnerabilities_properties: dict[str, dict[str, dict[str, str]]],
    severity_score: Decimal,
    severity_level: str,
) -> None:
    org_name = await get_organization_name(loaders, finding.group_name)
    recipients = set(FI_MAIL_REVIEWERS.split(","))
    recipients.add(responsible)
    email_context: dict[str, Any] = {
        "finding": finding.title,
        "finding_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{finding.group_name}"
            f"/vulns/{finding.id}/locations"
        ),
        "group": finding.group_name,
        "vulns_props": vulnerabilities_properties,
        "responsible": responsible,
        "severity_score": severity_score,
        "severity_level": severity_level,
    }
    await send_mails_async(
        loaders,
        list(recipients),
        context=email_context,
        tags=GENERAL_TAG,
        subject=(
            f"Fluid Attacks | Submitted location of [{finding.title}] in"
            f" [{finding.group_name}]"
        ),
        template_name="vulnerability_submission",
    )
