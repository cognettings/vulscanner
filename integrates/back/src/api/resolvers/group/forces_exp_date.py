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
from forces import (
    domain as forces_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP.field("forcesExpDate")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str | None:
    if not isinstance(parent.agent_token, str):
        return None

    return forces_domain.get_expiration_date(parent.agent_token)
