from .common import (
    get_recipient_first_name,
    send_mails_async,
)
from context import (
    BASE_URL,
    FI_MAIL_CUSTOMER_EXPERIENCE,
    FI_MAIL_PRODUCTION,
)
from custom_utils import (
    analytics,
    datetime as datetime_utils,
)
from dataloaders import (
    Dataloaders,
)
from db_model.enums import (
    GitCloningStatus,
)
from mailer.types import (
    TrialEngagementInfo,
)
from mailer.utils import (
    get_organization_country,
    get_organization_name,
    get_organization_name_by_org_id,
)
from typing import (
    Any,
)


async def send_abandoned_trial_notification(
    loaders: Dataloaders,
    email_to: str,
    first_time: bool,
) -> None:
    fname = await get_recipient_first_name(loaders, email_to)
    await send_mails_async(
        loaders,
        email_to=[email_to],
        subject=(
            f"[{fname}], start your Continuous Hacking Free Trial"
            + ("" if first_time else " (reminder)")
        ),
        template_name="abandoned_trial",
    )


async def send_add_members_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    org_name = await get_organization_name(loaders, info.group_name)
    context = {
        "stakeholders_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{info.group_name}/members"
        ),
    }
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        context=context,
        subject=(
            f"[{fname}], make the most of your Free Trial: "
            "add members to your group."
        ),
        template_name="add_members",
    )


async def send_add_repositories_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    org_name = await get_organization_name(loaders, info.group_name)
    context = {
        "scope_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{info.group_name}/scope"
        ),
    }
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        context=context,
        subject=(f"[{fname}], add more repos; find more vulnerabilities!"),
        template_name="add_repositories",
    )


async def send_define_treatments_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    org_name = await get_organization_name(loaders, info.group_name)
    context = {
        "vulnerabilities_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{info.group_name}/vulns"
        ),
    }
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        context=context,
        subject=(
            f"[{fname}], define treatments for your vulnerabilities. "
            "Make the most out of your Free Trial"
        ),
        template_name="define_treatments",
    )


async def send_devsecops_agent_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    org_name = await get_organization_name(loaders, info.group_name)
    context = {
        "devsecops_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{info.group_name}/devsecops"
        ),
    }
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        context=context,
        subject=(f"[{fname}], remediate faster with our DevSecOps Agent!"),
        template_name="devsecops_agent",
    )


async def send_how_improve_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        subject=(f"[{fname}], how can we improve?"),
        template_name="how_improve",
    )


async def send_mail_free_trial_over(
    loaders: Dataloaders, email_to: list[str], group_name: str
) -> None:
    org_name = await get_organization_name(loaders, group_name)
    context = {
        "vulnerabilities_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/vulns"
        ),
    }
    await send_mails_async(
        loaders,
        email_to=email_to,
        context=context,
        subject="Fluid Attacks | your free trial ends today.",
        template_name="free_trial_over",
    )


async def context_mail_free_trial_start(
    loaders: Dataloaders, email_to: str, full_name: str, group_name: str
) -> dict[str, Any]:
    org_name = await get_organization_name(loaders, group_name)
    org_country = await get_organization_country(loaders, group_name)
    context = {
        "country": org_country,
        "email": email_to,
        "empty_notification_notice": True,
        "enrolled_date": datetime_utils.get_as_str(
            datetime_utils.get_now(), "%Y-%m-%d %H:%M:%S %Z"
        ),
        "enrolled_name": full_name,
        "expires_date": datetime_utils.get_as_str(
            datetime_utils.get_now_plus_delta(days=21)
        ),
        "policies_link": f"{BASE_URL}/orgs/{org_name}/policies",
        "scope_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/scope"
        ),
        "stakeholders_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{group_name}/stakeholders"
        ),
    }

    return context


async def send_mail_free_trial_start(
    loaders: Dataloaders, email_to: str, full_name: str, group_name: str
) -> None:
    first_name = full_name.split(" ")[0]
    context: dict[str, Any] = await context_mail_free_trial_start(
        loaders, email_to, full_name, group_name
    )
    await analytics.mixpanel_track(email_to, "AutoenrollSuccess")
    await send_mails_async(
        loaders,
        email_to=[email_to],
        context=context,
        subject=(
            f"[{first_name}] Continuous Hacking just started "
            "on your applications"
        ),
        template_name="free_trial",
    )


async def send_mail_new_enrolled_user(
    loaders: Dataloaders, email_to: str, full_name: str, group_name: str
) -> None:
    context: dict[str, Any] = await context_mail_free_trial_start(
        loaders, email_to, full_name, group_name
    )
    enrolled_email_to: list = FI_MAIL_PRODUCTION.split(",")
    enrolled_email_to.extend(FI_MAIL_CUSTOMER_EXPERIENCE.split(","))
    await send_mails_async(
        loaders,
        email_to=enrolled_email_to,
        context=context,
        subject=f"Fluid Attacks | New enrolled user [{email_to}] "
        + f"from [{context['country']}]",
        template_name="new_enrolled",
    )


async def send_support_channels_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        subject=(
            f"[{fname}], Need help with Continuous Hacking? "
            "Use our support channels."
        ),
        template_name="support_channels",
    )


async def send_trial_corporate_email(
    loaders: Dataloaders,
    email_to: list[str],
) -> None:
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        subject="Free trial: Don’t miss out on trying Fluid Attacks’ "
        + "scanning tool!",
        context={},
        template_name="trial_corporate_email",
    )


async def send_trial_ended_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    org_name = await get_organization_name(loaders, info.group_name)
    context = {
        "vulnerabilities_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{info.group_name}/vulns"
        ),
    }
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        context=context,
        subject=(
            f"[{fname}], your free trial has ended. "
            "Here’s what you can do next."
        ),
        template_name="trial_ended",
    )


async def send_trial_ending_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    org_name = await get_organization_name(loaders, info.group_name)
    context = {
        "expires_date": datetime_utils.get_plus_delta(
            info.start_date, days=21
        ).date(),
        "vulnerabilities_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{info.group_name}/vulns"
        ),
    }
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        context=context,
        subject=(f"[{fname}], your free trial ends in 3 days."),
        template_name="trial_ending",
    )


async def send_trial_first_scanning(
    loaders: Dataloaders,
    email_to: list[str],
    have_vulns: bool,
    group_name: str,
    cloning_status: GitCloningStatus | None = None,
) -> None:
    org_name = await get_organization_name(loaders, group_name)
    app_link = f"{BASE_URL}/orgs/{org_name}/groups/{group_name}"
    context = {
        "app_link": f"{app_link}/vulns" if have_vulns else f"{app_link}/scope",
        "cloning_status": cloning_status.value
        if cloning_status
        else cloning_status,
        "have_vulnerabilities": have_vulns,
    }
    subject = "We found" if have_vulns else "Could not find"
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        subject=f"Fluid Attacks | {subject} "
        + "vulnerabilities in your repository!",
        context=context,
        template_name="trial_first_scanning",
    )


async def send_trial_reports_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    org_name = await get_organization_name(loaders, info.group_name)
    context = {
        "vulnerabilities_link": (
            f"{BASE_URL}/orgs/{org_name}/groups/{info.group_name}/vulns"
        ),
    }
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        context=context,
        subject=(f"[{fname}], download vulnerability reports."),
        template_name="trial_reports",
    )


async def send_upgrade_squad_notification(
    loaders: Dataloaders, info: TrialEngagementInfo
) -> None:
    fname = await get_recipient_first_name(loaders, info.email_to)
    await send_mails_async(
        loaders,
        email_to=[info.email_to],
        subject=(
            f"[{fname}], find more severe vulnerabilities with Squad Plan!"
        ),
        template_name="upgrade_squad",
    )


async def new_enrolled_user_mail(
    *,
    loaders: Dataloaders,
    user_email: str,
    full_name: str,
    group_name: str,
    organization_id: str,
) -> None:
    organization_name = await get_organization_name_by_org_id(
        loaders, organization_id
    )

    org_roots = await loaders.organization_roots.load(organization_name)

    if not org_roots:
        await send_mail_new_enrolled_user(
            loaders, user_email, full_name, group_name
        )
