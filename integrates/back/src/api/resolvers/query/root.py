from .schema import (
    QUERY,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    Root,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots import (
    utils as roots_utils,
)


@QUERY.field("root")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Root:
    group_name: str = kwargs["group_name"]
    root_id: str = kwargs["root_id"]
    loaders: Dataloaders = info.context.loaders
    root = await roots_utils.get_root(loaders, root_id, group_name)

    return root
