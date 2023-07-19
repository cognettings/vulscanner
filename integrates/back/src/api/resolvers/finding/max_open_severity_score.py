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


@FINDING.field("maxOpenSeverityScore")
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> Decimal:
    return parent.unreliable_indicators.max_open_severity_score
