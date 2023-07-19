from .payloads.types import (
    AddEventPayload,
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
    require_asm,
    require_login,
)
from events import (
    domain as events_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)


@MUTATION.field("addEvent")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    group_name: str,
    **kwargs: Any,
) -> AddEventPayload:
    """Resolve add_event mutation."""
    user_info = await sessions_domain.get_jwt_content(info.context)
    hacker_email = user_info["user_email"]

    event_id = await events_domain.add_event(
        info.context.loaders,
        hacker_email=hacker_email,
        group_name=group_name.lower(),
        **kwargs,
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Added a new event in {group_name} group successfully",
    )

    return AddEventPayload(event_id=event_id, success=True)
