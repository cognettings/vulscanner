from .schema import (
    TOE_LINES,
)
from datetime import (
    datetime,
)
from db_model.toe_lines.types import (
    ToeLines,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@TOE_LINES.field("sortsRiskLevelDate")
def resolve(
    parent: ToeLines, _info: GraphQLResolveInfo, **_kwargs: None
) -> datetime | None:
    return parent.state.sorts_risk_level_date
