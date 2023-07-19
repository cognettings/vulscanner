from .schema import (
    TOE_LINES,
)
from db_model.toe_lines.types import (
    ToeLines,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@TOE_LINES.field("sortsPriorityFactor")
def resolve(
    parent: ToeLines, _info: GraphQLResolveInfo, **_kwargs: None
) -> int | None:
    return parent.state.sorts_priority_factor
