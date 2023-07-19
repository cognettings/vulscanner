from .schema import (
    FINDING,
)
from custom_utils.datetime import (
    get_as_str,
)
from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@FINDING.field("reportDate")
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> str | None:
    indicators = parent.unreliable_indicators
    if indicators.oldest_vulnerability_report_date:
        return get_as_str(indicators.oldest_vulnerability_report_date)
    if parent.creation:
        return get_as_str(parent.creation.modified_date)

    return None
