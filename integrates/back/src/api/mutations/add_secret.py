from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots.utils import (
    add_secret,
)


@MUTATION.field("addSecret")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(  # pylint: disable=too-many-arguments
    _: None,
    info: GraphQLResolveInfo,
    group_name: str,
    key: str,
    value: str,
    root_id: str,
    description: str | None = None,
) -> SimplePayload:
    result = await add_secret(
        info.context.loaders, group_name, root_id, key, value, description
    )

    return SimplePayload(success=result)
