from aioextensions import (
    collect,
    in_thread,
)
from collections.abc import (
    Iterable,
)
from context import (
    BASE_URL,
    FI_MAIL_PRODUCTION,
)
from custom_exceptions import (
    FindingNotFound,
    GroupNotFound,
)
from custom_utils import (
    datetime as datetime_utils,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.groups.enums import (
    GroupManaged,
    GroupStateJustification as GroupReason,
    GroupSubscriptionType,
)
from db_model.groups.types import (
    Group,
    GroupState,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
import html
from mailer import (
    groups as groups_mail,
    utils as mailer_utils,
)
from notifications import (
    dal as notifications_dal,
)
from organizations.utils import (
    get_organization,
)
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
    cast,
)


async def _get_recipient_first_name_async(
    loaders: Dataloaders, email: str
) -> str:
    stakeholder = await loaders.stakeholder.load(email)
    first_name = stakeholder.first_name if stakeholder else ""
    if not first_name:
        first_name = email.split("@")[0]
    else:
        # First name exists in database
        pass
    return str(first_name)


async def cancel_health_check(
    requester_email: str, group_name: str, repo_url: str, branch: str
) -> None:
    await in_thread(
        notifications_dal.create_ticket,
        subject=f"Fluid Attacks | Health Check canceled: {group_name}",
        description=f"""
            You are receiving this email because you have canceled a health
            check for a repository through ARM by Fluid Attacks.

            Here are the details of the repository:
            - URL: {repo_url}
            - branch: {branch}

            If you require any further information,
            do not hesitate to contact us.
        """,
        requester_email=requester_email,
    )


def translate_group_reason(reason: str) -> str:
    translation = {
        GroupReason.DIFF_SECTST.value: "Different security testing strategy",
        GroupReason.MIGRATION.value: "Information will be moved to a different"
        + " group",
        GroupReason.MISTAKE.value: "Created by mistake",
        GroupReason.NO_SECTST.value: "No more security testing",
        GroupReason.NO_SYSTEM.value: "System will be deprecated",
        GroupReason.OTHER.value: "Other reason not mentioned",
        GroupReason.RENAME.value: "Group rename",
        GroupReason.POC_OVER.value: "Proof of concept over",
        GroupReason.TR_CANCELLED.value: "Testing request cancelled",
        GroupReason.TRIAL_FINALIZATION.value: "Trial expiration",
    }
    if reason in translation:
        return translation[reason]
    return reason.capitalize().replace("_", " ")


def translate_group_subscription(group: Group) -> str:
    subscription = group.state.type
    has_squad = group.state.has_squad
    translation = {
        GroupSubscriptionType.CONTINUOUS: "Continuous Hacking - "
        + ("Squad Plan" if has_squad else "Machine Plan"),
        GroupSubscriptionType.ONESHOT: "Oneshot Hacking",
    }
    if subscription in translation:
        return translation[subscription]
    return subscription.capitalize().replace("_", " ")


async def delete_group(
    *,
    loaders: Dataloaders,
    deletion_date: datetime,
    group: Group,
    requester_email: str,
    reason: str,
    comments: str,
    attempt: bool | None = False,
) -> None:
    org_id = group.organization_id
    organization = await get_organization(loaders, org_id)
    org_name = organization.name
    users_email = await mailer_utils.get_group_emails_by_notification(
        loaders=loaders,
        group_name=group.name,
        notification="group_alert",
    )
    users_email.extend(FI_MAIL_PRODUCTION.split(","))
    await groups_mail.send_mail_group_alert(
        loaders,
        users_email,
        {
            "attempt": attempt,
            "created_by": group.created_by,
            "created_date": group.created_date.date(),
            "comments": html.escape(comments, quote=False),
            "date": deletion_date.date(),
            "group": group.name,
            "organization": org_name,
            "reason": translate_group_reason(reason),
            "responsible": requester_email,
            "state": "deleted",
            "subscription": translate_group_subscription(group),
        },
    )


async def update_group(  # pylint: disable=too-many-locals
    *,
    loaders: Dataloaders,
    comments: str,
    group_name: str,
    group_state: GroupState,
    had_arm: bool,
    has_arm: bool,
    has_machine: bool,
    has_squad: bool,
    reason: str,
    requester_email: str,
    service: str,
    subscription: str,
) -> bool:
    old_subscription: str = str(group_state.type.value).lower()
    old_service = group_state.service
    translations: dict[Any, str] = {
        "continuous": "Continuous Hacking",
        "oneshot": "One-Shot Hacking",
        True: "Active",
        False: "Inactive",
    }
    group_changes: dict[str, Any] = {
        "Name": group_name,
        "Type": {
            "from": translations.get(old_subscription, old_subscription),
            "to": translations.get(subscription, subscription),
        },
        "Service": {
            "from": str(old_service.value if old_service else "").capitalize(),
            "to": service.capitalize(),
        },
        "ARM": {
            "from": translations[had_arm],
            "to": translations[has_arm],
        },
        "Machine": {
            "from": translations[group_state.has_machine],
            "to": translations[has_machine],
        },
        "Squad": {
            "from": translations[group_state.has_squad],
            "to": translations[has_squad],
        },
        "Comments": comments,
        "Reason": reason.replace("_", " ").capitalize(),
    }

    description_body: str = ""

    for key, value in group_changes.items():
        description_body += f"- {key}: "
        description_body += (
            f"{html.escape(value, quote=True)}\n"
            if key in ["Comments", "Reason", "Name"]
            else f"\n\tfrom: {value['from']}\n\tto: {value['to']}\n"
        )

    description: str = (
        "You are receiving this email because you have edited a group through "
        "ARM by Fluid Attacks. \n\nHere are the details of the group:"
        f"\n{description_body}\n\nIf you require any further information, "
        "do not hesitate to contact us."
    )

    await send_mail_services(
        loaders=loaders,
        group_name=group_name,
        group_changes=group_changes,
        requester_email=requester_email,
    )

    return cast(
        bool,
        await in_thread(
            notifications_dal.create_ticket,
            subject=f"Fluid Attacks | Group edited: {group_name}",
            description=description,
            requester_email=requester_email,
        ),
    )


async def send_mail_services(
    *,
    loaders: Dataloaders,
    group_name: str,
    group_changes: dict[str, Any],
    requester_email: str,
) -> None:
    users_email = await mailer_utils.get_group_emails_by_notification(
        loaders=loaders,
        group_name=group_name,
        notification="updated_services",
    )

    await groups_mail.send_mail_updated_services(
        loaders=loaders,
        group_name=group_name,
        responsible=requester_email,
        group_changes=group_changes,
        report_date=datetime_utils.get_utc_now(),
        email_to=users_email,
    )


async def new_group(
    *,
    description: str,
    group_name: str,
    has_machine: bool,
    has_squad: bool,
    organization: str,
    requester_email: str,
    service: str,
    subscription: str,
) -> bool:
    translations: dict[str | bool, str] = {
        "continuous": "Continuous Hacking",
        "oneshot": "One-Shot Hacking",
        True: "Active",
        False: "Inactive",
    }

    return cast(
        bool,
        await in_thread(
            notifications_dal.create_ticket,
            subject=f"Fluid Attacks | Group created: {group_name}",
            description=f"""
                You are receiving this email because you have created a group
                through ARM by Fluid Attacks.

                Here are the details of the group:
                - Name: {group_name}
                - Description: {description}
                - Type: {translations.get(subscription, subscription)}
                - Service: {service}
                - Organization: {organization}
                - Squad: {translations[has_squad]}
                - Machine: {translations[has_machine]}

                If you require any further information,
                do not hesitate to contact us.
            """,
            requester_email=requester_email,
        ),
    )


async def request_managed(
    *,
    group_name: str,
    managed: GroupManaged,
    organization_name: str,
    requester_email: str,
) -> bool:
    translations: dict[str, str] = {
        "MANAGED": "Managed",
        "NOT_MANAGED": "Not Managed",
        "UNDER_REVIEW": "Under Review",
        "TRIAL": "Trial",
    }

    return cast(
        bool,
        await in_thread(
            notifications_dal.create_ticket,
            subject=(
                f"Fluid Attacks | {translations[managed]} managed requested:"
                f" {group_name}"
            ),
            description=f"""
                You are receiving this email because you have requested
                to {translations[managed]} managed a group, through ARM
                by Fluid Attacks.

                Here are the details of the group:
                - Name: {group_name}
                - Organization: {organization_name}

                If you require any further information,
                do not hesitate to contact us.
            """,
            requester_email=requester_email,
        ),
    )


async def new_password_protected_report(
    *,
    loaders: Dataloaders,
    user_email: str,
    group_name: str,
    file_type: str,
    file_link: str = "",
    include_report: bool = True,
) -> None:
    today = datetime_utils.get_now()
    fname = await _get_recipient_first_name_async(loaders, user_email)
    subject = (
        f'{file_type}{" Report for" if include_report else ""} [{group_name}]'
    )
    await groups_mail.send_mail_group_report(
        loaders=loaders,
        email_to=[user_email],
        context={
            "filetype": file_type,
            "fname": fname,
            "date": datetime_utils.get_as_str(today, "%Y-%m-%d"),
            "year": datetime_utils.get_as_str(today, "%Y"),
            "time": datetime_utils.get_as_str(today, "%H:%M"),
            "group_name": group_name,
            "subject": subject,
            "filelink": file_link,
        },
        report=include_report,
    )


async def request_health_check(
    requester_email: str, group_name: str, repo_url: str, branch: str
) -> None:
    await in_thread(
        notifications_dal.create_ticket,
        subject=f"Fluid Attacks | Health Check requested: {group_name}",
        description=f"""
            You are receiving this email because you have requested a health
            check for a repository in {group_name.capitalize()} group
            through ARM by Fluid Attacks.

            Here are the details of the repository:
            - URL: {repo_url}
            - branch: {branch}

            If you require any further information,
            do not hesitate to contact us.
        """,
        requester_email=requester_email,
    )


async def request_vulnerability_zero_risk(
    loaders: Dataloaders,
    finding_id: str,
    justification: str,
    requester_email: str,
    vulnerabilities: Iterable[Vulnerability],
) -> bool:
    finding = await loaders.finding.load(finding_id)
    if finding is None:
        raise FindingNotFound()

    finding_title = finding.title
    group_name = finding.group_name

    group = await loaders.group.load(group_name)
    if not group:
        raise GroupNotFound()
    org_id = group.organization_id
    organization = await get_organization(loaders, org_id)
    org_name = organization.name
    finding_url = (
        f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/vulns/"
        f"{finding_id}/locations"
    )
    new_line = "\n\t"
    description = f"""
        You are receiving this case because a zero risk vulnerability has been
        requested through ARM by Fluid Attacks.

        Here are the details of the zero risk vulnerability:
        Group: {group_name}

        - Finding: {finding_title}
        - ID: {finding_id}
        - URL: {finding_url}
        - Justification: {justification}

        Locations:
        {new_line+new_line.join(
            [
                f"- {vulnerability.state.where} "
                f"| {vulnerability.state.specific}"
                for vulnerability in vulnerabilities
            ]
        )}

        If you require any further information,
        do not hesitate to contact us.
    """

    return cast(
        bool,
        await in_thread(
            notifications_dal.create_ticket,
            subject="Fluid Attacks | Requested zero risk vulnerabilities",
            description=description,
            requester_email=requester_email,
        ),
    )


async def request_groups_upgrade(
    loaders: Dataloaders,
    user_email: str,
    groups: Iterable[Group],
) -> None:
    organization_ids = list(group.organization_id for group in groups)
    organizations = await collect(
        list(
            get_organization(loaders, organization_id)
            for organization_id in organization_ids
        )
    )
    organizations_message = "".join(
        f"""
            - Organization {organization.name}:
                {', '.join(
                    group.name
                    for group in groups
                    if group.organization_id == organization.id)
                }
        """
        for organization in organizations
    )

    await in_thread(
        notifications_dal.create_ticket,
        subject="Fluid Attacks | Subscription upgrade requested",
        description=f"""
            You are receiving this email because you have requested an upgrade
            to the Squad plan for the following groups:
            {organizations_message}
            If you require any further information,
            do not hesitate to contact us.
        """,
        requester_email=user_email,
    )


async def request_other_payment_methods(
    *,
    business_legal_name: str,
    city: str,
    country: str,
    efactura_email: str,
    rut: UploadFile | None,
    tax_id: UploadFile | None,
    user_email: str,
) -> None:
    attachments = tuple(
        attachment for attachment in (rut, tax_id) if attachment is not None
    )
    efactura_text = (
        f"- Email (e-factura): {efactura_email}" if efactura_email else ""
    )

    await in_thread(
        notifications_dal.create_ticket,
        attachments=attachments,
        subject="Fluid Attacks | Other payment methods requested",
        description=f"""
            You are receiving this email because you have requested other
            payment methods.

            - Business legal name: {business_legal_name}
            - Country: {country}
            - City: {city}
            {efactura_text}

            If you require any further information,
            do not hesitate to contact us.
        """,
        requester_email=user_email,
    )
