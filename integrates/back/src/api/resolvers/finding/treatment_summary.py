from .schema import (
    FINDING,
)
from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@FINDING.field("treatmentSummary")
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> dict[str, int]:
    return parent.unreliable_indicators.unreliable_treatment_summary._asdict()
