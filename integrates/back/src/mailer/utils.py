from aioextensions import (
    collect,
)
import authz
from custom_exceptions import (
    GroupNotFound,
    OrganizationNotFound,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderState,
)
from decimal import (
    Decimal,
)
from group_access.domain import (
    get_stakeholders_email_by_preferences,
)
from mailer.preferences import (
    MAIL_PREFERENCES,
)


async def get_available_notifications(
    loaders: Dataloaders, email: str
) -> list[str]:
    stakeholder_roles = await get_stakeholder_roles(loaders, email)
    available_notifications_by_template = [
        template.email_preferences
        for template in MAIL_PREFERENCES.values()
        if template.email_preferences
        and (
            any(
                item in template.roles.group
                for item in stakeholder_roles["group"]
            )
            or any(
                item in template.roles.org for item in stakeholder_roles["org"]
            )
        )
    ]
    return sorted(set(available_notifications_by_template))


async def get_group_emails_by_notification(
    *,
    loaders: Dataloaders,
    group_name: str,
    notification: str,
) -> list[str]:
    preferences = MAIL_PREFERENCES[notification]
    group_roles = preferences.roles.group
    return await get_stakeholders_email_by_preferences(
        loaders=loaders,
        group_name=group_name,
        notification=preferences.email_preferences.value
        if preferences.email_preferences
        else None,
        roles=set(group_roles),
        exclude_trial=preferences.exclude_trial,
        only_fluid_staff=preferences.only_fluid_staff,
    )


async def get_org_groups(loaders: Dataloaders, org_id: str) -> list[Group]:
    return await loaders.organization_groups.load(org_id)


async def get_organization_country(
    loaders: Dataloaders, group_name: str
) -> str | None:
    group = await loaders.group.load(group_name)
    if not group:
        raise GroupNotFound()
    organization = await loaders.organization.load(group.organization_id)
    if not organization:
        raise OrganizationNotFound()
    return organization.country


async def get_organization_name(loaders: Dataloaders, group_name: str) -> str:
    group = await loaders.group.load(group_name)
    if not group:
        raise GroupNotFound()
    organization = await loaders.organization.load(group.organization_id)
    if not organization:
        raise OrganizationNotFound()
    return organization.name


async def get_organization_name_by_org_id(
    loaders: Dataloaders, organization_id: str
) -> str:
    organization = await loaders.organization.load(organization_id)

    if not organization:
        raise OrganizationNotFound()
    return organization.name


async def get_stakeholder_roles(
    loaders: Dataloaders, email: str
) -> dict[str, set[str]]:
    stakeholder_orgs = await loaders.stakeholder_organizations_access.load(
        email
    )
    org_roles = await collect(
        [
            authz.get_organization_level_role(
                loaders, email, org.organization_id
            )
            for org in stakeholder_orgs
        ]
    )
    org_groups = await collect(
        [
            get_org_groups(loaders, org.organization_id)
            for org in stakeholder_orgs
        ]
    )
    group_roles = await collect(
        [
            authz.get_group_level_role(loaders, email, item.name)
            for group in org_groups
            for item in group
        ]
    )
    return dict(
        group=set(" ".join(group_roles).split()),
        org=set(" ".join(org_roles).split()),
    )


async def get_vulnerability_report_group_emails(
    loaders: Dataloaders,
    group_name: str,
    severity_score: Decimal,
    group_findings: list[Finding],
) -> list[str]:
    group_emails = await get_group_emails_by_notification(
        loaders=loaders,
        group_name=group_name,
        notification="vulnerability_report",
    )
    stakeholders = await loaders.stakeholder.load_many(group_emails)
    return [
        stakeholder.email
        for stakeholder in stakeholders
        if stakeholder
        and should_send_vulnerability_mail(
            severity_score=severity_score,
            stakeholder=stakeholder,
            group_findings=group_findings,
        )
    ]


def should_send_vulnerability_mail(
    *,
    severity_score: Decimal,
    stakeholder: Stakeholder,
    group_findings: list[Finding],
) -> bool:
    state: StakeholderState = stakeholder.state
    return (
        severity_score
        >= state.notifications_preferences.parameters.min_severity
        or not group_findings
    )
