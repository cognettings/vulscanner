from .payloads.types import (
    AddRootPayload,
)
from .schema import (
    MUTATION,
)
from custom_utils import (
    logs as logs_utils,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_service_black,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots import (
    domain as roots_domain,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)


@MUTATION.field("addUrlRoot")
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_service_black
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> AddRootPayload:
    user_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    user_email: str = user_info["user_email"]

    root = await roots_domain.add_url_root(
        loaders=info.context.loaders, user_email=user_email, **kwargs
    )
    logs_utils.cloudwatch_log(
        info.context,
        f'Security: Added a root in {kwargs["group_name"].lower()}',
    )

    return AddRootPayload(root_id=root, success=True)
