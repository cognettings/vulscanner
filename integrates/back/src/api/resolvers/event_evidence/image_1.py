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


@EVENT_EVIDENCE.field("image1")
def resolve(
    parent: EventEvidences,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Any:
    image_1 = parent.image_1
    return image_1
