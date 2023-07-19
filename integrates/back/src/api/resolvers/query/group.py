from .schema import (
    QUERY,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)


@QUERY.field("group")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Group:
    group_name: str = str(kwargs["group_name"]).lower()
    loaders: Dataloaders = info.context.loaders
    group = await groups_domain.get_group(loaders, group_name.lower())

    return group
