from .schema import (
    EVENT_EVIDENCE,
)
from db_model.events.types import (
    EventEvidences,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


@EVENT_EVIDENCE.field("image5")
def resolve(
    parent: EventEvidences,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Any:
    image_5 = parent.image_5
    return image_5
