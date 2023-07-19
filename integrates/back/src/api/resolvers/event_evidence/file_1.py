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


@EVENT_EVIDENCE.field("file1")
def resolve(
    parent: EventEvidences,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Any:
    file_1 = parent.file_1
    return file_1
