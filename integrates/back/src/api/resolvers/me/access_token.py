from .schema import (
    ME,
)
from custom_utils.datetime import (
    get_as_utc_iso_format,
)
from dataloaders import (
    Dataloaders,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import json
from stakeholders.domain import (
    get_stakeholder,
)
from typing import (
    Any,
)


@ME.field("accessToken")
async def resolve(
    parent: dict[str, Any], info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    user_email = str(parent["user_email"])
    loaders: Dataloaders = info.context.loaders
    stakeholder: Stakeholder = await get_stakeholder(loaders, user_email)
    access_tokens = stakeholder.access_tokens

    return json.dumps(
        {
            "hasAccessToken": bool(access_tokens),
            "issuedAt": (
                str(access_tokens[-1].issued_at) if access_tokens else ""
            ),
            "lastAccessTokenUse": get_as_utc_iso_format(
                access_tokens[-1].last_use
            )
            if access_tokens and access_tokens[-1].last_use
            else None,
        }
    )
