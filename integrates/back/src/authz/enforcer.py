from .model import (
    get_group_level_actions_by_role,
    get_organization_level_actions_by_role,
    get_user_level_actions_by_role,
)
from .model.services import (
    SERVICE_ATTRIBUTES,
)
from .policy import (
    get_group_service_policies,
    get_user_level_role,
)
from collections.abc import (
    Callable,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)


async def get_group_level_enforcer(
    loaders: Dataloaders,
    email: str,
) -> Callable[[str, str], bool]:
    """Makes an enforcer for group-level authorization of `email`.

    The enforcer is a function that takes a group name and an action and
    returns `True` if these conditions are met:
    - User has access to the group
    - User has a role inside the group
    - That role allows to execute the action

    Or,

    - User is an admin and action is allowed for admins

    Returns:
        func(group_name: str, action: str) -> bool
    """
    groups_access = await loaders.stakeholder_groups_access.load(email)
    user_level_role = await get_user_level_role(loaders, email)

    def enforcer(group_name_to_test: str, action: str) -> bool:
        return any(
            # Regular user with a group policy set for the r_object
            group_name_to_test == access.group_name
            and access.role
            and action in get_group_level_actions_by_role(access.role)
            for access in groups_access
        ) or (
            # An admin
            user_level_role == "admin"
            and action in get_group_level_actions_by_role("admin")
        )

    return enforcer


def get_group_service_attributes_enforcer(
    group: Group,
) -> Callable[[str], bool]:
    """Makes an enforcer for service authorization of `group`.

    The enforcer is a function that takes a service attribute and
    returns `True` if the attribute is enabled on the group.

    Returns:
        func(attribute: str) -> bool
    """
    policies = get_group_service_policies(group)

    def enforcer(r_attribute: str) -> bool:
        should_grant_access: bool = any(
            r_attribute in SERVICE_ATTRIBUTES[p_service]
            for p_service in policies
        )
        return should_grant_access

    return enforcer


async def get_organization_level_enforcer(
    loaders: Dataloaders,
    email: str,
) -> Callable[[str, str], bool]:
    """Makes an enforcer for organization-level authorization of `email`.

    The enforcer is a function that takes an organization id and an action and
    returns `True` if these conditions are met:
    - User has access to the organization
    - User has a role inside the organization
    - That role allows to execute the action

    Or,

    - User is an admin and action is allowed for admins

    Returns:
        func(organization_id: str, action: str) -> bool
    """
    orgs_access = await loaders.stakeholder_organizations_access.load(email)
    user_level_role = await get_user_level_role(loaders, email)

    def enforcer(organization_id_to_test: str, action: str) -> bool:
        return any(
            # Regular user with an organization policy set for the r_object
            organization_id_to_test == access.organization_id
            and access.role
            and action in get_organization_level_actions_by_role(access.role)
            for access in orgs_access
        ) or (
            # An admin
            user_level_role == "admin"
            and action in get_organization_level_actions_by_role("admin")
        )

    return enforcer


async def get_user_level_enforcer(
    loaders: Dataloaders,
    email: str,
) -> Callable[[str], bool]:
    """Makes an enforcer for user-level authorization of `email`.

    The enforcer is a function that takes the action and
    returns `True` if these conditions are met:
    - User has a role
    - That role allows to execute the action

    Returns:
        func(action: str) -> bool
    """
    user_level_role = await get_user_level_role(loaders, email)

    def enforcer(action: str) -> bool:
        return bool(
            user_level_role
            and action in get_user_level_actions_by_role(user_level_role)
        )

    return enforcer
