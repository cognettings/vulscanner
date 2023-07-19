from .schema import (
    FINDING,
)
from db_model.findings.types import (
    CVSS31Severity,
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@FINDING.field("severity")
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> CVSS31Severity:
    return parent.severity
