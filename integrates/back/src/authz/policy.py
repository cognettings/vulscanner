from .model import (
    FLUID_IDENTIFIER,
    get_group_level_roles_model,
    get_organization_level_roles_model,
    get_user_level_roles_model,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    StakeholderNotFound,
)
from custom_utils import (
    datetime as datetime_utils,
)
from dataloaders import (
    Dataloaders,
)
from db_model import (
    group_access as group_access_model,
    organization_access as organization_access_model,
    stakeholders as stakeholders_model,
)
from db_model.group_access.types import (
    GroupAccessMetadataToUpdate,
    GroupAccessRequest,
    GroupAccessState,
)
from db_model.group_access.utils import (
    merge_group_access_changes,
)
from db_model.groups.enums import (
    GroupService,
    GroupStateStatus,
    GroupSubscriptionType,
)
from db_model.groups.types import (
    Group,
)
from db_model.organization_access.types import (
    OrganizationAccessMetadataToUpdate,
    OrganizationAccessRequest,
)
from db_model.stakeholders.types import (
    StakeholderMetadataToUpdate,
)
from typing import (
    NamedTuple,
)


class ServicePolicy(NamedTuple):
    group_name: str
    service: str


def get_group_service_policies(group: Group) -> tuple[str, ...]:
    """Gets a group's authorization policies."""
    policies: tuple[str, ...] = tuple(
        policy.service
        for policy in _get_service_policies(group)
        if policy.group_name == group.name
    )
    return policies


def _get_service_policies(group: Group) -> list[ServicePolicy]:
    """Return a list of policies for the given group."""
    has_squad = group.state.has_squad
    has_asm = group.state.status == GroupStateStatus.ACTIVE
    service = group.state.service
    type_ = group.state.type
    has_machine_squad: bool = has_squad or group.state.has_machine

    business_rules = (
        (has_asm, "asm"),
        (
            type_ == GroupSubscriptionType.CONTINUOUS
            and has_asm
            and has_machine_squad,
            "report_vulnerabilities",
        ),
        (service == GroupService.BLACK and has_asm, "service_black"),
        (service == GroupService.WHITE and has_asm, "service_white"),
        (
            has_asm and has_machine_squad,
            "request_zero_risk",
        ),
        (
            type_ == GroupSubscriptionType.CONTINUOUS and has_asm,
            "forces",
        ),
        (
            type_ == GroupSubscriptionType.CONTINUOUS
            and has_asm
            and has_squad,
            "squad",
        ),
        (type_ == GroupSubscriptionType.CONTINUOUS, "continuous"),
        (
            type_ == GroupSubscriptionType.ONESHOT and has_asm,
            "report_vulnerabilities",
        ),
        (
            type_ == GroupSubscriptionType.ONESHOT and has_asm and has_squad,
            "squad",
        ),
    )

    return [
        ServicePolicy(group_name=group.name, service=policy_name)
        for condition, policy_name in business_rules
        if condition
    ]


async def get_group_level_role(
    loaders: Dataloaders,
    email: str,
    group_name: str,
) -> str:
    """Returns the user's role in the group.
    Empty string if the user has no role.

    Admin users are granted access to all groups.
    """
    is_admin: bool = await get_user_level_role(loaders, email) == "admin"
    group_role: str = ""
    group_access = await loaders.group_access.load(
        GroupAccessRequest(group_name=group_name, email=email)
    )
    if group_access and group_access.role:
        group_role = group_access.role

    if not group_role and is_admin:
        return "admin"

    return group_role


async def get_group_level_roles(
    loaders: Dataloaders,
    email: str,
    groups: list[str],
) -> dict[str, str]:
    """Returns the user's role in each queried group.

    Admin users are `admin` if user does not have another role
    in the group. Otherwise, the role in group is returned.

    Returns:
        dict[str, str]: A dictionary with the group name as key
        and the user's role in the group as value.
    """
    is_admin: bool = await get_user_level_role(loaders, email) == "admin"
    groups_access = await loaders.stakeholder_groups_access.load(email)
    db_roles: dict[str, str] = {
        access.group_name: access.role
        for access in groups_access
        if access.role
    }

    return {
        group: "admin"
        if is_admin and group not in db_roles
        else db_roles.get(group, "")
        for group in groups
    }


async def get_organization_level_role(
    loaders: Dataloaders,
    email: str,
    organization_id: str,
) -> str:
    """Returns the user's role in the organization.
    Empty string if the user has no role.

    Admin users are granted access to all organizations.
    """
    is_admin: bool = await get_user_level_role(loaders, email) == "admin"
    organization_role: str = ""
    org_access = await loaders.organization_access.load(
        OrganizationAccessRequest(organization_id=organization_id, email=email)
    )
    if org_access and org_access.role:
        organization_role = org_access.role

    if not organization_role and is_admin:
        return "admin"

    return organization_role


async def get_user_level_role(
    loaders: Dataloaders,
    email: str,
) -> str:
    """Returns the user's role. Empty string if the user
    is not a stakeholder.

    Valid roles are:
    `admin`, `hacker`, `reattacker`, `resourcer`,
    `reviewer`, `architect`, `service_forces`,
    `user`, `user_manager`, `vulnerability_manager`.
    """
    user_role: str = ""
    with suppress(StakeholderNotFound):
        stakeholder = await loaders.stakeholder.load(email)
        if stakeholder and stakeholder.role:
            user_role = stakeholder.role

    return user_role


async def grant_group_level_role(
    loaders: Dataloaders,
    email: str,
    group_name: str,
    role: str,
) -> None:
    if role not in get_group_level_roles_model():
        raise ValueError(f"Invalid role value: {role}")
    metadata = GroupAccessMetadataToUpdate(
        has_access=True,
        role=role,
        state=GroupAccessState(modified_date=datetime_utils.get_utc_now()),
    )
    group_access = await loaders.group_access.load(
        GroupAccessRequest(group_name=group_name, email=email)
    )
    if group_access:
        metadata = merge_group_access_changes(
            old_access=group_access, changes=metadata
        )
    await group_access_model.update_metadata(
        email=email,
        group_name=group_name,
        metadata=metadata,
    )
    # If there is no user-level role for this user add one
    if not await get_user_level_role(loaders, email):
        user_level_role: str = (
            role if role in get_user_level_roles_model() else "user"
        )
        await grant_user_level_role(email, user_level_role)


async def grant_organization_level_role(
    loaders: Dataloaders,
    email: str,
    organization_id: str,
    role: str,
) -> None:
    if role not in get_organization_level_roles_model():
        raise ValueError(f"Invalid role value: {role}")

    await organization_access_model.update_metadata(
        email=email,
        organization_id=organization_id,
        metadata=OrganizationAccessMetadataToUpdate(role=role),
    )
    # If there is no user-level role for this user add one
    if not await get_user_level_role(loaders, email):
        user_level_role: str = (
            role if role in get_user_level_roles_model() else "user"
        )
        await grant_user_level_role(email, user_level_role)


async def grant_user_level_role(email: str, role: str) -> None:
    if role not in get_user_level_roles_model():
        raise ValueError(f"Invalid role value: {role}")

    role = (
        "hacker"
        if role == "user" and email.endswith(FLUID_IDENTIFIER)
        else role
    )

    await stakeholders_model.update_metadata(
        email=email,
        metadata=StakeholderMetadataToUpdate(role=role),
    )


async def has_access_to_group(
    loaders: Dataloaders,
    email: str,
    group_name: str,
) -> bool:
    return bool(await get_group_level_role(loaders, email, group_name))


async def revoke_group_level_role(
    loaders: Dataloaders, email: str, group_name: str
) -> None:
    group_access = await loaders.group_access.load(
        GroupAccessRequest(group_name=group_name, email=email)
    )
    if group_access and group_access.role:
        metadata = merge_group_access_changes(
            old_access=group_access,
            changes=GroupAccessMetadataToUpdate(
                role="",
                state=GroupAccessState(
                    modified_date=datetime_utils.get_utc_now()
                ),
            ),
        )
        await group_access_model.update_metadata(
            email=email, group_name=group_name, metadata=metadata
        )


async def revoke_organization_level_role(
    loaders: Dataloaders, email: str, organization_id: str
) -> None:
    org_access = await loaders.organization_access.load(
        OrganizationAccessRequest(organization_id=organization_id, email=email)
    )
    if org_access and org_access.role:
        await organization_access_model.update_metadata(
            email=email,
            organization_id=organization_id,
            metadata=OrganizationAccessMetadataToUpdate(role=""),
        )


async def revoke_user_level_role(loaders: Dataloaders, email: str) -> None:
    stakeholder = await loaders.stakeholder.load(email)
    if stakeholder and stakeholder.role:
        await stakeholders_model.update_metadata(
            email=email,
            metadata=StakeholderMetadataToUpdate(role=""),
        )
