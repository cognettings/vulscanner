from .schema import (
    QUERY,
)
from aioextensions import (
    collect,
)
from custom_utils import (
    groups as groups_utils,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)


@QUERY.field("listUserGroups")
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> list[Group]:
    loaders: Dataloaders = info.context.loaders
    user_email: str = kwargs["user_email"]
    active, inactive = await collect(
        [
            groups_domain.get_groups_by_stakeholder(loaders, user_email),
            groups_domain.get_groups_by_stakeholder(
                loaders, user_email, active=False
            ),
        ]
    )
    user_groups = active + inactive
    groups = await collect(
        [
            groups_domain.get_group(loaders, user_group)
            for user_group in user_groups
        ]
    )

    return groups_utils.filter_active_groups(groups)
