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
    add_root_environment_secret,
)


@MUTATION.field("addGitEnvironmentSecret")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(
    _: None,
    __: GraphQLResolveInfo,
    group_name: str,
    key: str,
    value: str,
    url_id: str,
    description: str | None = None,
    **_kwargs: None,
) -> SimplePayload:
    result = await add_root_environment_secret(
        group_name, url_id, key, value, description
    )

    return SimplePayload(success=result)
