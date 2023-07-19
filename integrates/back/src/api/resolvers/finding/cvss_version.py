from .schema import (
    FINDING,
)
from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@FINDING.field("cvssVersion")
def resolve(_: Finding, _info: GraphQLResolveInfo, **_kwargs: None) -> str:
    return "3.1"
