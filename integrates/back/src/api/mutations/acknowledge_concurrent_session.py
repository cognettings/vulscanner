from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
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


@MUTATION.field("acknowledgeConcurrentSession")
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
) -> SimplePayload:
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    await stakeholders_domain.acknowledge_concurrent_session(user_email)

    return SimplePayload(success=True)
