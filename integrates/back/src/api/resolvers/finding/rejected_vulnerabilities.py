from .schema import (
    FINDING,
)
from db_model.findings.types import (
    Finding,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@FINDING.field("rejectedVulnerabilities")
@enforce_group_level_auth_async
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> int:
    return parent.unreliable_indicators.rejected_vulnerabilities
