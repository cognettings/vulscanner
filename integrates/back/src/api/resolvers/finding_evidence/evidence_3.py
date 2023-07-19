from .schema import (
    FINDING_EVIDENCE,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


@FINDING_EVIDENCE.field("evidence3")
def resolve(
    parent: dict[str, dict[str, Any]],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Any:
    return parent["evidence_3"]
