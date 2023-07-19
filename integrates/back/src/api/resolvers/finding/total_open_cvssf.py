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


@FINDING.field("totalOpenCVSSF")
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> Decimal:
    return parent.unreliable_indicators.unreliable_total_open_cvssf
