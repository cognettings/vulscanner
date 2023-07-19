from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)


@MUTATION.field("requestGroupsUpgrade")
@require_login
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayload:
    user_info = await sessions_domain.get_jwt_content(info.context)
    email = user_info["user_email"]
    group_names: list[str] = kwargs["group_names"]
    await groups_domain.request_upgrade(
        loaders=info.context.loaders,
        email=email,
        group_names=group_names,
    )

    return SimplePayload(success=True)
