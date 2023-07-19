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


@MUTATION.field("updateTours")
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    tours: dict[str, bool],
) -> SimplePayload:
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    await stakeholders_domain.update_tours(user_email, tours)

    return SimplePayload(success=True)
