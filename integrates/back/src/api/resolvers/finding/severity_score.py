from .schema import (
    FINDING,
)
from db_model.findings.types import (
    Finding,
)
from decimal import (
    Decimal,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@FINDING.field("severityScore")
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> Decimal:
    return parent.severity_score.temporal_score
