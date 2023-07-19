from .schema import (
    QUERY,
)
from db_model.roots.get import (
    get_git_environment_url_by_id,
)
from db_model.roots.types import (
    RootEnvironmentUrl,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@QUERY.field("environmentUrl")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def resolve(
    _parent: None, _info: GraphQLResolveInfo, url_id: str, **kwargs: str
) -> RootEnvironmentUrl | None:
    url = await get_git_environment_url_by_id(url_id=url_id)

    if url:
        return url._replace(group_name=kwargs["group_name"])
    return None
