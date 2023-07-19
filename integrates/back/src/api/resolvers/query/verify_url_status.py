from .schema import (
    QUERY,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import requests


@QUERY.field("verifyUrlStatus")
@require_login
def resolve(
    _parent: None,
    _info: GraphQLResolveInfo,
    url: str,
    **_kwargs: None,
) -> bool:
    request = requests.get(url, timeout=10)
    website_is_up = request.status_code == 200
    return website_is_up
