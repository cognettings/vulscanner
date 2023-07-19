from .schema import (
    FINDING,
)
from custom_utils.findings import (
    get_formatted_evidence,
)
from db_model.findings.types import (
    Finding,
)
from findings.domain.evidence import (
    filter_drafts,
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


@FINDING.field("evidence")
async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> dict[str, dict[str, Any]]:
    user_data = await sessions_domain.get_jwt_content(info.context)

    return await filter_drafts(
        email=user_data["user_email"],
        evidences=get_formatted_evidence(parent),
        group_name=parent.group_name,
        loaders=info.context.loaders,
    )
