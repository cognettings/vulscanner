from .schema import (
    FINDING,
)
from db_model.findings.types import (
    Finding,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@FINDING.field("age")
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> int:
    indicators = parent.unreliable_indicators
    return findings_domain.get_report_days(
        indicators.oldest_vulnerability_report_date
    )
