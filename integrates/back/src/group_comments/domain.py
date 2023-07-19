import authz
from custom_exceptions import (
    InvalidCommentParent,
)
from custom_utils.validations_deco import (
    validate_fields_deco,
    validate_length_deco,
)
from dataloaders import (
    Dataloaders,
)
from db_model import (
    group_comments as group_comments_model,
)
from db_model.group_comments.types import (
    GroupComment,
)


def is_scope_comment(comment: GroupComment) -> bool:
    return comment.content.strip() not in {"#external", "#internal"}


@authz.validate_handle_comment_scope_deco(
    "loaders",
    "comment_data.content",
    "comment_data.email",
    "group_name",
    "comment_data.parent_id",
)
@validate_length_deco("comment_data.content", max_length=5000)
@validate_fields_deco(["comment_data.content"])
async def add_comment(
    *,
    loaders: Dataloaders,
    group_name: str,
    comment_data: GroupComment,
) -> None:
    """Add comment in a group."""
    parent_comment = comment_data.parent_id
    if parent_comment != "0":
        comments: list[GroupComment] = await loaders.group_comments.load(
            group_name
        )
        group_comments = [comment.id for comment in comments]
        if parent_comment not in group_comments:
            raise InvalidCommentParent()
    await group_comments_model.add(group_comment=comment_data)


async def remove_comments(group_name: str) -> None:
    await group_comments_model.remove_group_comments(group_name=group_name)


async def get_comments(
    loaders: Dataloaders, group_name: str, email: str
) -> tuple[GroupComment, ...]:
    enforcer = await authz.get_group_level_enforcer(loaders, email)
    comments: list[GroupComment] = await loaders.group_comments.load(
        group_name
    )

    if enforcer(group_name, "handle_comment_scope"):
        return tuple(comments)

    return tuple(filter(is_scope_comment, comments))
