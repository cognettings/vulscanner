from .schema import (
    EVENT,
)
from custom_utils import (
    datetime as datetime_utils,
)
from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@EVENT.field("closingDate")
def resolve(
    parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    solving_date = parent.unreliable_indicators.unreliable_solving_date
    if solving_date:
        closing_date = datetime_utils.get_as_str(solving_date)
    else:
        closing_date = "-"

    return closing_date
