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


@EVENT_EVIDENCE.field("image6")
def resolve(
    parent: EventEvidences,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Any:
    image_6 = parent.image_6
    return image_6
