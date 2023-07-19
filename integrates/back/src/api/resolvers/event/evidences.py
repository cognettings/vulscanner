from .schema import (
    EVENT,
)
from db_model.events.types import (
    Event,
    EventEvidences,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@EVENT.field("evidences")
def resolve(
    parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> EventEvidences:
    evidences = parent.evidences
    return evidences
