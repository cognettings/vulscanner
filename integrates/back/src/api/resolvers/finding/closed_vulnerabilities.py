from .schema import (
    FINDING,
)
from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@FINDING.field("closedVulnerabilities")
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> int:
    return parent.unreliable_indicators.closed_vulnerabilities
