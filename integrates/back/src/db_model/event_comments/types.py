from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
)


class EventComment(NamedTuple):
    event_id: str
    id: str
    parent_id: str
    creation_date: datetime
    content: str
    email: str
    group_name: str
    full_name: str | None = None


class EventCommentsRequest(NamedTuple):
    event_id: str
    group_name: str
