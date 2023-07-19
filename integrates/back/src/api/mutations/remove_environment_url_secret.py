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
    remove_environment_url_secret,
)


@MUTATION.field("removeEnvironmentUrlSecret")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(
    _: None,
    __: GraphQLResolveInfo,
    group_name: str,
    key: str,
    url_id: str,
    **_kwargs: object,
) -> SimplePayload:
    await remove_environment_url_secret(group_name, url_id, key)

    return SimplePayload(success=True)
