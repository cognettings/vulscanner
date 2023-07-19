from .schema import (
    FINDING,
)
from custom_utils import (
    findings as findings_utils,
)
from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@FINDING.field("verified")
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> bool:
    return findings_utils.is_verified(
        parent.unreliable_indicators.unreliable_verification_summary
    )
