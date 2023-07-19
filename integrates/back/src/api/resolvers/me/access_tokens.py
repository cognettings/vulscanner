from .schema import (
    ME,
)
from db_model.stakeholders.types import (
    AccessTokens,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from stakeholders.domain import (
    get_stakeholder,
)


@ME.field("accessTokens")
async def resolve(
    parent: dict, info: GraphQLResolveInfo
) -> list[AccessTokens]:
    user_email = str(parent["user_email"])
    stakeholder = await get_stakeholder(info.context.loaders, user_email)

    return stakeholder.access_tokens
