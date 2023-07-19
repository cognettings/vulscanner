from datetime import (
    datetime,
)
from db_model.event_comments.types import (
    EventComment,
)
from dynamodb.types import (
    Item,
)


def format_event_comments(item: Item) -> EventComment:
    return EventComment(
        event_id=item["event_id"],
        group_name=item["group_name"],
        id=item["id"],
        parent_id=item["parent_id"],
        creation_date=datetime.fromisoformat(item["creation_date"]),
        full_name=item.get("full_name"),
        content=item["content"],
        email=item["email"],
    )
