from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from custom_utils import (
    logs as logs_utils,
    stakeholders as stakeholders_utils,
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


@MUTATION.field("requestEventVerification")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    comments: str,
    event_id: str,
    group_name: str,
) -> SimplePayload:
    stakeholder_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    await events_domain.request_verification(
        loaders=info.context.loaders,
        event_id=event_id,
        comments=comments,
        group_name=group_name,
        stakeholder_email=str(stakeholder_info["user_email"]),
        stakeholder_full_name=stakeholders_utils.get_full_name(
            stakeholder_info
        ),
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Requested verification in event {event_id} successfully",
    )

    return SimplePayload(success=True)
