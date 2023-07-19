from .enforcer import (
    get_group_level_enforcer,
    get_group_service_attributes_enforcer,
    get_organization_level_enforcer,
    get_user_level_enforcer,
)
from .model import (
    get_group_level_roles_model,
    get_organization_level_roles_model,
    get_user_level_roles_model,
    GROUP_LEVEL_ACTIONS,
    ORGANIZATION_LEVEL_ACTIONS,
    USER_LEVEL_ACTIONS,
)
from .model.services import (
    SERVICE_ATTRIBUTES_SET,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
import logging
import logging.config
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def get_group_level_actions(
    loaders: Dataloaders, email: str, group: str
) -> set[str]:
    """Returns an action set with every action
    that `email` can perform on `group`.

    Args:
        loaders (Dataloaders): Database loader
        email (str): User email
        group (str): Group to check
    """
    enforcer = await get_group_level_enforcer(loaders, email)
    group_actions = {
        action
        for action in GROUP_LEVEL_ACTIONS
        if enforcer(group.lower(), action)
    }
    if not group_actions:
        LOGGER.error(
            "Empty group actions on get_group_level_actions",
            extra=dict(extra=locals()),
        )
    return group_actions


async def get_group_level_roles_a_user_can_grant(
    *,
    loaders: Dataloaders,
    group: str,
    requester_email: str,
) -> tuple[str, ...]:
    """Return a tuple of group level roles that users
    can grant based on their role.
    """
    enforcer = await get_group_level_enforcer(loaders, requester_email)
    roles_the_user_can_grant: tuple[str, ...] = tuple(
        role
        for role in get_group_level_roles_model()
        if enforcer(group, f"grant_group_level_role:{role}")
    )
    return roles_the_user_can_grant


def get_group_level_roles_with_tag(tag: str) -> set[str]:
    """Returns a set of group level roles that have `tag` in their tags."""
    return {
        role_name
        for role_name, role_definition in get_group_level_roles_model().items()
        if tag in role_definition.get("tags", [])
    }


def get_group_service_attributes(group: Group) -> set[str]:
    """Returns a set of service attributes that `group` has."""
    enforcer = get_group_service_attributes_enforcer(group)
    return set(filter(enforcer, SERVICE_ATTRIBUTES_SET))


async def get_organization_level_actions(
    loaders: Dataloaders, email: str, organization_id: str
) -> set[str]:
    """Returns an action set with every action
    that `email` can perform on `organization`.

    Args:
        loaders (Dataloaders): Database loader
        email (str): User email
        organization_id (str): Id of organization to check
    """
    enforcer = await get_organization_level_enforcer(loaders, email)
    organization_actions = {
        action
        for action in ORGANIZATION_LEVEL_ACTIONS
        if enforcer(organization_id, action)
    }
    if not organization_actions:
        LOGGER.error(
            "Empty organization actions on get_organization_level_actions",
            extra=dict(
                extra=dict(
                    email=email,
                    organization_id=organization_id,
                )
            ),
        )
    return organization_actions


async def get_organization_level_roles_a_user_can_grant(
    *,
    loaders: Dataloaders,
    organization_id: str,
    requester_email: str,
) -> tuple[str, ...]:
    """Return a tuple of organization level roles
    that users can grant based on their role.
    """
    enforcer = await get_organization_level_enforcer(loaders, requester_email)
    roles_the_user_can_grant: tuple[str, ...] = tuple(
        role
        for role in get_organization_level_roles_model()
        if enforcer(organization_id, f"grant_organization_level_role:{role}")
    )
    return roles_the_user_can_grant


async def get_user_level_actions(loaders: Dataloaders, email: str) -> set[str]:
    """Returns an action set with every action
    that `email` can perform at user level.

    Args:
        loaders (Dataloaders): Database loader
        email (str): User email
    """
    enforcer = await get_user_level_enforcer(loaders, email)
    user_actions = {
        action for action in USER_LEVEL_ACTIONS if enforcer(action)
    }
    if not user_actions:
        LOGGER.error(
            "Empty user actions on get_user_level_actions",
            extra=dict(extra=locals()),
        )
    return user_actions


async def get_user_level_roles_a_user_can_grant(
    *,
    loaders: Dataloaders,
    requester_email: str,
) -> tuple[str, ...]:
    """Return a tuple of user level roles
    that users can grant based on their role.
    """
    enforcer = await get_user_level_enforcer(loaders, requester_email)
    roles_the_user_can_grant: tuple[str, ...] = tuple(
        role
        for role in get_user_level_roles_model()
        if enforcer(f"grant_user_level_role:{role}")
    )
    return roles_the_user_can_grant
