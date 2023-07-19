from .schema import (
    FINDING,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    FindingVulnerabilitiesRequest,
    VulnerabilitiesConnection,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


@FINDING.field("vulnerabilitiesToReattackConnection")
async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> VulnerabilitiesConnection:
    loaders: Dataloaders = info.context.loaders

    return await loaders.finding_vulnerabilities_to_reattack_c.load(
        FindingVulnerabilitiesRequest(
            finding_id=parent.id,
            after=kwargs.get("after", None),
            first=kwargs.get("first", None),
            paginate=True,
        )
    )
