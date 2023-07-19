from .schema import (
    QUERY,
)
from custom_utils import (
    datetime as datetime_utils,
)
from decorators import (
    require_login,
)
from dynamodb.types import (
    Item,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from sessions import (
    domain as sessions_domain,
)


@QUERY.field("me")
@require_login
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Item:
    caller_origin: str = kwargs.get("caller_origin", "API")
    user_data: Item = await sessions_domain.get_jwt_content(info.context)
    exp: str = datetime_utils.get_as_utc_iso_format(
        datetime_utils.get_from_epoch(user_data["exp"])
    )
    return {
        "caller_origin": caller_origin,
        "session_expiration": exp,
        "user_email": user_data["user_email"],
        "user_name": " ".join(
            [user_data.get("first_name", ""), user_data.get("last_name", "")]
        ),
    }
