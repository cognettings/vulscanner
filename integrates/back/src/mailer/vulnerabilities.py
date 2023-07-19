from .common import (
    GENERAL_TAG,
    send_mails_async,
)
import authz
from context import (
    BASE_URL,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    date,
    datetime,
)
from db_model.enums import (
    Notification,
)
from group_access import (
    domain as group_access_domain,
)
from mailer.utils import (
    get_organization_name,
)
from typing import (
    Any,
)


async def send_mail_updated_treatment(
    *,
    loaders: Dataloaders,
    assigned: str,
    finding_id: str,
    finding_title: str,
    group_name: str,
    justification: str,
    treatment: str,
    vulnerabilities: str,
    modified_by: str,
) -> None:
    org_name = await get_organization_name(loaders, group_name)
    managers = await group_access_domain.get_managers(loaders, group_name)
    stakeholders = await loaders.stakeholder.load_many(managers)
    stakeholders_email = [
        stakeholder.email
        for stakeholder in stakeholders
        if stakeholder
        and Notification.UPDATED_TREATMENT
        in stakeholder.state.notifications_preferences.email
    ]
    stakeholder_role = await authz.get_group_level_role(
        loaders, modified_by, group_name
    )
    email_context: dict[str, str | list[str]] = {
        "assigned": assigned,
        "group": group_name,
        "justification": justification,
        "responsible": modified_by,
        "treatment": treatment,
        "finding": finding_title,
        "user_role": stakeholder_role.replace("_", " "),
        "vulnerabilities": vulnerabilities.splitlines(),
        "finding_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}"
            f"/vulns/{finding_id}"
        ),
    }
    await send_mails_async(
        loaders,
        stakeholders_email,
        context=email_context,
        tags=GENERAL_TAG,
        subject=(
            "Fluid Attacks | A vulnerability treatment has changed to "
            f'{email_context["treatment"]} in [{email_context["group"]}]'
        ),
        template_name="updated_treatment",
    )


async def send_mail_treatment_report(  # pylint: disable=too-many-locals
    *,
    loaders: Dataloaders,
    finding_id: str,
    finding_title: str,
    group_name: str,
    justification: str | None,
    managers_email: list[str],
    modified_by: str | None,
    modified_date: datetime,
    location: str,
    email_to: list[str],
    is_approved: bool,
) -> None:
    org_name = await get_organization_name(loaders, group_name)
    approve_state: str = (
        "has been approved" if is_approved else "has been requested"
    )
    user_email: str = modified_by if modified_by else ""
    user_role = await authz.get_group_level_role(
        loaders, user_email, group_name
    )
    email_context: dict[str, Any] = {
        "date": str(modified_date.date()),
        "group": group_name,
        "responsible": modified_by,
        "justification": justification,
        "finding": finding_title,
        "is_approved": is_approved,
        "vulnerabilities": location.splitlines(),
        "managers_email": managers_email,
        "approve_state": approve_state,
        "user_role": user_role.replace("_", " "),
        "finding_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}"
            f"/vulns/{finding_id}"
        ),
    }
    await send_mails_async(
        loaders,
        email_to,
        context=email_context,
        tags=GENERAL_TAG,
        subject=f"Fluid Attacks | A permanent treatment {approve_state} in "
        + f"[{group_name}]",
        template_name="treatment_report",
    )


async def send_mail_assigned_vulnerability(
    *,
    loaders: Dataloaders,
    email_to: list[str],
    is_finding_released: bool,
    group_name: str = "",
    finding_title: str,
    finding_id: str,
    responsible: str,
    where: str,
) -> None:
    org_name = await get_organization_name(loaders, group_name)

    email_context: dict[str, str | list[str]] = {
        "finding_title": finding_title,
        "group": group_name,
        "finding_url": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/"
            f'{"vulns" if is_finding_released else "drafts"}/{finding_id}/'
            "locations"
        ),
        "responsible": responsible,
        "where": where.splitlines(),
    }
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        context=email_context,
        tags=GENERAL_TAG,
        subject=(
            "Fluid Attacks | Newly assigned vulnerability in "
            f"[{finding_title}] for [{group_name}]"
        ),
        template_name="vulnerability_assigned",
    )


async def send_mail_reviewer_progress_report(
    *,
    loaders: Dataloaders,
    context: dict[str, Any],
    email_to: list[str],
    email_cc: list[str],
    report_date: date,
    responsible: str,
) -> None:
    user_login = str(responsible).split("@", maxsplit=1)[0]
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        email_cc=email_cc,
        tags=GENERAL_TAG,
        subject=f"Fluid Attacks | Reviewer progress report {user_login} "
        + f"[{report_date}]",
        context=context,
        template_name="reviewer_progress_report",
    )
