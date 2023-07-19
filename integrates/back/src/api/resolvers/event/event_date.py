from .schema import (
    EVENT,
)
from custom_utils.datetime import (
    get_as_str,
)
from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@EVENT.field("eventDate")
def resolve(
    parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    return get_as_str(parent.event_date)
