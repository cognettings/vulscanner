from .schema import (
    GROUP,
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


@GROUP.field("forcesToken")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str | None:
    return parent.agent_token
