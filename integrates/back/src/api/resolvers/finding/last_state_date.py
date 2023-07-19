from .schema import (
    FINDING,
)
from custom_utils import (
    datetime as datetime_utils,
)
from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@FINDING.field("lastStateDate")
def resolve(
    parent: Finding,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    return datetime_utils.get_as_str(parent.state.modified_date)
