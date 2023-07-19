from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from enum import (
    Enum,
)
from tap_announcekit.objs.id_objs import (
    ExtUserId,
    FeedbackId,
    IndexedObj,
)
from typing import (
    Optional,
)


class ActionSource(Enum):
    WIDGET = "widget"
    EMAIL = "email"
    FEED = "feed"


@dataclass(frozen=True)
class Feedback:
    reaction: Optional[str]
    comment: Optional[str]
    source: ActionSource
    created_at: datetime
    external_user_id: ExtUserId


FeedbackObj = IndexedObj[FeedbackId, Feedback]
