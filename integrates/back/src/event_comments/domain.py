import authz
from dataloaders import (
    Dataloaders,
)
from db_model import (
    event_comments as event_comments_model,
)
from db_model.event_comments.types import (
    EventComment,
    EventCommentsRequest,
)


def _is_scope_comment(comment: EventComment) -> bool:
    return str(comment.content).strip() not in {"#external", "#internal"}


async def add(
    comment_data: EventComment,
) -> None:
    await event_comments_model.add(event_comment=comment_data)


async def remove_comments(event_id: str, group_name: str) -> None:
    await event_comments_model.remove_event_comments(
        event_id=event_id, group_name=group_name
    )


async def get_comments(
    loaders: Dataloaders, group_name: str, event_id: str, email: str
) -> list[EventComment]:
    comments = await loaders.event_comments.load(
        EventCommentsRequest(event_id=event_id, group_name=group_name)
    )
    enforcer = await authz.get_group_level_enforcer(loaders, email)
    if enforcer(group_name, "handle_comment_scope"):
        return comments

    return list(filter(_is_scope_comment, comments))
