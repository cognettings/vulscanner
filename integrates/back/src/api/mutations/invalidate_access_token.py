from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from custom_exceptions import (
    UnavailabilityError,
)
from custom_utils import (
    logs as logs_utils,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from sessions import (
    domain as sessions_domain,
)
from stakeholders import (
    domain as stakeholders_domain,
)


@MUTATION.field("invalidateAccessToken")
@require_login
async def mutate(
    _: None, info: GraphQLResolveInfo, **kwargs: str
) -> SimplePayload:
    user_info = await sessions_domain.get_jwt_content(info.context)
    token_id = kwargs.get("id", None)
    try:
        await stakeholders_domain.remove_access_token(
            user_info["user_email"], info.context.loaders, token_id
        )
        logs_utils.cloudwatch_log(
            info.context, f'{user_info["user_email"]} invalidate access token'
        )
    except UnavailabilityError:
        logs_utils.cloudwatch_log(
            info.context,
            f'{user_info["user_email"]} attempted to invalidate access token',
        )

    return SimplePayload(success=True)
