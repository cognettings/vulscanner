from aioextensions import (
    collect,
)
import authz
from contextlib import (
    suppress,
)
from custom_exceptions import (
    GroupNotFound,
    InvalidAuthorization,
    RequestedInvitationTooSoon,
    StakeholderNotFound,
    StakeholderNotInGroup,
)
from custom_utils import (
    datetime as datetime_utils,
    validations,
)
from custom_utils.group_access import (
    format_invitation_state,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model import (
    group_access as group_access_model,
)
from db_model.group_access.enums import (
    GroupInvitiationState,
)
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessMetadataToUpdate,
    GroupAccessRequest,
    GroupAccessState,
)
from db_model.group_access.utils import (
    merge_group_access_changes,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from db_model.vulnerabilities.update import (
    update_assigned_index,
)
from jwcrypto.jwt import (
    JWTExpired,
)
import logging
import logging.config
from sessions import (
    domain as sessions_domain,
)
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


async def get_group_access(
    loaders: Dataloaders, group_name: str, email: str
) -> GroupAccess:
    group_access = await loaders.group_access.load(
        GroupAccessRequest(group_name=group_name, email=email)
    )
    if not group_access:
        raise StakeholderNotInGroup()
    return group_access


async def add_access(
    loaders: Dataloaders, email: str, group_name: str, role: str
) -> None:
    await update(
        loaders=loaders,
        email=email,
        group_name=group_name,
        metadata=GroupAccessMetadataToUpdate(
            has_access=True,
            state=GroupAccessState(modified_date=datetime_utils.get_utc_now()),
        ),
    )
    loaders.stakeholder.clear(email)
    loaders.group_access.clear(
        GroupAccessRequest(group_name=group_name, email=email)
    )

    await authz.grant_group_level_role(loaders, email, group_name, role)


async def get_access_by_url_token(
    loaders: Dataloaders, url_token: str
) -> GroupAccess:
    try:
        token_content = sessions_domain.decode_token(url_token)
        group_name: str = token_content["group_name"]
        email: str = token_content["user_email"]
    except (KeyError, JWTExpired) as ex:
        raise InvalidAuthorization() from ex

    return await get_group_access(loaders, group_name, email)


async def get_reattackers(
    loaders: Dataloaders, group_name: str, active: bool = True
) -> list[str]:
    stakeholders = await get_group_stakeholders_emails(
        loaders, group_name, active
    )
    stakeholder_roles = await collect(
        authz.get_group_level_role(loaders, email, group_name)
        for email in stakeholders
    )
    return [
        str(stakeholder)
        for stakeholder, stakeholder_role in zip(
            stakeholders, stakeholder_roles
        )
        if stakeholder_role == "reattacker"
    ]


async def get_stakeholder(
    loaders: Dataloaders,
    email: str,
    user_email: str | None = None,
) -> Stakeholder:
    if user_email and not validations.is_fluid_staff(user_email):
        if validations.is_fluid_staff(email):
            raise StakeholderNotFound()

    stakeholder = await loaders.stakeholder.load(email)

    if stakeholder:
        return stakeholder

    raise StakeholderNotFound()


async def get_group_stakeholders(
    loaders: Dataloaders,
    group_name: str,
    user_email: str | None = None,
) -> list[Stakeholder]:
    emails = [
        access.email
        for access in await loaders.group_stakeholders_access.load(group_name)
    ]
    stakeholders: list[Stakeholder] = []
    for email in emails:
        try:
            stakeholder = await get_stakeholder(loaders, email, user_email)
            stakeholders.append(stakeholder)
        except StakeholderNotFound:
            if not validations.is_fluid_staff(email):
                stakeholders.append(Stakeholder(email=email))
    return stakeholders


async def get_group_stakeholders_emails(
    loaders: Dataloaders, group_name: str, active: bool = True
) -> list[str]:
    stakeholders_access = await loaders.group_stakeholders_access.load(
        group_name
    )
    now_epoch = datetime_utils.get_as_epoch(datetime_utils.get_now())
    active_stakeholders_email = [
        access.email
        for access in stakeholders_access
        if access.has_access
        and (not access.expiration_time or access.expiration_time > now_epoch)
    ]
    if active:
        return active_stakeholders_email

    return [
        access.email
        for access in stakeholders_access
        if access.email not in active_stakeholders_email
    ]


async def get_managers(loaders: Dataloaders, group_name: str) -> list[str]:
    stakeholders = await get_group_stakeholders_emails(
        loaders, group_name, active=True
    )
    stakeholders_roles = await collect(
        [
            authz.get_group_level_role(loaders, stakeholder, group_name)
            for stakeholder in stakeholders
        ]
    )
    return [
        email
        for email, role in zip(stakeholders, stakeholders_roles)
        if role in {"user_manager", "vulnerability_manager"}
    ]


async def get_stakeholder_groups_names(
    loaders: Dataloaders, email: str, active: bool
) -> list[str]:
    groups_access = await loaders.stakeholder_groups_access.load(email)

    return [
        group_access.group_name
        for group_access in groups_access
        if group_access.has_access == active
    ]


async def get_stakeholders_subscribed_to_consult(
    *,
    loaders: Dataloaders,
    group_name: str,
    comment_type: str,
    is_finding_released: bool = True,
) -> list[str]:
    emails = await get_group_stakeholders_emails(loaders, group_name)
    if comment_type.lower() == "observation" or not is_finding_released:
        roles: tuple[str, ...] = await collect(
            tuple(
                authz.get_group_level_role(loaders, email, group_name)
                for email in emails
            ),
            workers=16,
        )
        hackers = [
            email for email, role in zip(emails, roles) if role == "hacker"
        ]

        return hackers

    return emails


async def get_stakeholders_email_by_preferences(
    *,
    loaders: Dataloaders,
    group_name: str,
    notification: str | None,
    roles: set[str],
    exclude_trial: bool = False,
    only_fluid_staff: bool = False,
) -> list[str]:
    group = await loaders.group.load(group_name)
    if not group:
        raise GroupNotFound()
    trial = (
        await loaders.trial.load(group.created_by)
        if "@" in group.created_by
        else None
    )
    is_trial = not (trial and trial.completed)
    email_list = await get_stakeholders_email_by_roles(
        loaders=loaders,
        group_name=group_name,
        roles=roles,
    )
    stakeholders_data: list[Stakeholder] = []
    for email in email_list:
        if stakeholder := await loaders.stakeholder.load(email):
            stakeholders_data.append(stakeholder)
        else:
            stakeholders_data.append(Stakeholder(email=email))
    stakeholders_email = [
        stakeholder.email
        for stakeholder in stakeholders_data
        if (
            not notification
            or notification
            in stakeholder.state.notifications_preferences.email
        )
        and not (exclude_trial and is_trial)
        and not (
            only_fluid_staff
            and not stakeholder.email.endswith("@fluidattacks.com")
        )
    ]
    return stakeholders_email


async def get_stakeholders_email_by_roles(
    *,
    loaders: Dataloaders,
    group_name: str,
    roles: set[str],
) -> list[str]:
    stakeholders = await get_group_stakeholders_emails(
        loaders, group_name, active=True
    )
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


async def exists(loaders: Dataloaders, group_name: str, email: str) -> bool:
    if await loaders.group_access.load(
        GroupAccessRequest(group_name=group_name, email=email)
    ):
        return True
    return False


async def remove_access(
    loaders: Dataloaders, email: str, group_name: str
) -> None:
    all_findings = await loaders.group_findings.load(group_name)
    me_vulnerabilities = await loaders.me_vulnerabilities.load(email)
    findings_ids: set[str] = {finding.id for finding in all_findings}
    group_vulnerabilities = list(
        vulnerability
        for vulnerability in me_vulnerabilities
        if vulnerability.finding_id in findings_ids
    )
    await collect(
        tuple(
            update_assigned_index(
                finding_id=vulnerability.finding_id,
                vulnerability_id=vulnerability.id,
                entry=None,
            )
            for vulnerability in group_vulnerabilities
        ),
        workers=4,
    )

    await group_access_model.remove(email=email, group_name=group_name)
    LOGGER.info(
        "Stakeholder removed from group",
        extra={
            "extra": {
                "email": email,
                "group_name": group_name,
            }
        },
    )


async def update(
    loaders: Dataloaders,
    email: str,
    group_name: str,
    metadata: GroupAccessMetadataToUpdate,
) -> None:
    with suppress(StakeholderNotInGroup):
        old_access = await get_group_access(loaders, group_name, email)
        metadata = merge_group_access_changes(old_access, metadata)
    await group_access_model.update_metadata(
        email=email, group_name=group_name, metadata=metadata
    )


def validate_new_invitation_time_limit(inv_expiration_time: int) -> bool:
    """Validates that new invitations to the same user in the same group/org
    are spaced out by at least one minute to avoid email flooding."""
    expiration_date: datetime = datetime_utils.get_from_epoch(
        inv_expiration_time
    )
    creation_date: datetime = datetime_utils.get_minus_delta(
        date=expiration_date, weeks=1
    )
    current_date: datetime = datetime_utils.get_now()
    if current_date - creation_date < timedelta(minutes=1):
        raise RequestedInvitationTooSoon()
    return True


async def get_stakeholder_role(
    loaders: Dataloaders,
    email: str,
    group_name: str,
    is_registered: bool,
) -> str:
    if not await exists(loaders, group_name, email):
        group_access = GroupAccess(
            email=email,
            group_name=group_name,
            state=GroupAccessState(modified_date=datetime_utils.get_utc_now()),
        )
    else:
        group_access = await get_group_access(loaders, group_name, email)
    group_invitation_state = format_invitation_state(
        invitation=group_access.invitation,
        is_registered=is_registered,
    )

    return (
        group_access.invitation.role
        if group_access.invitation
        and group_invitation_state == GroupInvitiationState.PENDING
        else await authz.get_group_level_role(loaders, email, group_name)
    )
