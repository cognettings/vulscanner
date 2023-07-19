from .roles import (
    ADMIN_ROLE,
    ARCHITECT_ROLE,
    CUSTOMER_MANAGER_ROLE,
    HACKER_ROLE,
    REATTACKER_ROLE,
    RESOURCER_ROLE,
    REVIEWER_ROLE,
    SERVICE_FORCES_ROLE,
    USER_MANAGER_ROLE,
    USER_ROLE,
    VULNERABILITY_MANAGER_ROLE,
)
from .types import (
    RoleModel,
)

FLUID_IDENTIFIER = "@fluidattacks.com"

GROUP_LEVEL_ROLES: RoleModel = dict(
    admin=ADMIN_ROLE["group_level"],
    hacker=HACKER_ROLE["group_level"],
    reattacker=REATTACKER_ROLE["group_level"],
    user=USER_ROLE["group_level"],
    user_manager=USER_MANAGER_ROLE["group_level"],
    customer_manager=CUSTOMER_MANAGER_ROLE["group_level"],
    resourcer=RESOURCER_ROLE["group_level"],
    reviewer=REVIEWER_ROLE["group_level"],
    architect=ARCHITECT_ROLE["group_level"],
    service_forces=SERVICE_FORCES_ROLE["group_level"],
    vulnerability_manager=VULNERABILITY_MANAGER_ROLE["group_level"],
)


ORGANIZATION_LEVEL_ROLES: RoleModel = dict(
    admin=ADMIN_ROLE["organization_level"],
    user=USER_ROLE["organization_level"],
    user_manager=USER_MANAGER_ROLE["organization_level"],
    customer_manager=CUSTOMER_MANAGER_ROLE["organization_level"],
)


USER_LEVEL_ROLES: RoleModel = dict(
    admin=ADMIN_ROLE["user_level"],
    hacker=HACKER_ROLE["user_level"],
    user=USER_ROLE["user_level"],
)

# Actions
GROUP_LEVEL_ACTIONS: set[str] = {
    action
    for definition in GROUP_LEVEL_ROLES.values()
    for action in definition["actions"]
}

ORGANIZATION_LEVEL_ACTIONS: set[str] = {
    action
    for definition in ORGANIZATION_LEVEL_ROLES.values()
    for action in definition["actions"]
}

USER_LEVEL_ACTIONS: set[str] = {
    action
    for definition in USER_LEVEL_ROLES.values()
    for action in definition["actions"]
}


def get_group_level_roles_model() -> RoleModel:
    """Returns a dict with every role at group level
    that can be assigned to.
    """
    return GROUP_LEVEL_ROLES


def get_organization_level_roles_model() -> RoleModel:
    """Returns a dict with every role at organization level
    that can be assigned to.
    """
    return ORGANIZATION_LEVEL_ROLES


def get_user_level_roles_model() -> RoleModel:
    """Returns a dict with every role at user level
    that can be assigned to.
    """
    return USER_LEVEL_ROLES


def get_group_level_actions_by_role(role: str) -> set[str]:
    """Returns a set with the actions that can be performed by `role`
    at group level.
    """
    if role in GROUP_LEVEL_ROLES:
        return GROUP_LEVEL_ROLES[role]["actions"]
    return set()


def get_organization_level_actions_by_role(role: str) -> set[str]:
    """Returns a set with the actions that can be performed by `role`
    at organization level.
    """
    if role in ORGANIZATION_LEVEL_ROLES:
        return ORGANIZATION_LEVEL_ROLES[role]["actions"]
    return set()


def get_user_level_actions_by_role(role: str) -> set[str]:
    """Returns a set with the actions that can be performed by `role`
    at user level.
    """
    if role in USER_LEVEL_ROLES:
        return USER_LEVEL_ROLES[role]["actions"]
    return set()
