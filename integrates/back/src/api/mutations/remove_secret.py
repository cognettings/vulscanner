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
from roots.domain import (
    remove_secret,
)


@MUTATION.field("removeSecret")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(
    _: None,
    __: GraphQLResolveInfo,
    key: str,
    root_id: str,
    **_kwargs: str,
) -> SimplePayload:
    await remove_secret(root_id, key)

    return SimplePayload(success=True)
