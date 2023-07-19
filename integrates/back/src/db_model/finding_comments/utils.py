from datetime import (
    datetime,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
)
from db_model.utils import (
    get_as_utc_iso_format,
)
from dynamodb.types import (
    Item,
)


def format_finding_comment_item(finding_comment: FindingComment) -> Item:
    return {
        "finding_id": finding_comment.finding_id,
        "id": finding_comment.id,
        "parent_id": finding_comment.parent_id,
        "comment_type": finding_comment.comment_type.value,
        "creation_date": get_as_utc_iso_format(finding_comment.creation_date),
        "content": finding_comment.content,
        "email": finding_comment.email,
        "full_name": finding_comment.full_name,
    }


def format_finding_comments(item: Item) -> FindingComment:
    return FindingComment(
        finding_id=item["finding_id"],
        id=item["id"],
        comment_type=CommentType[item["comment_type"]],
        parent_id=item["parent_id"],
        creation_date=datetime.fromisoformat(item["creation_date"]),
        full_name=item.get("full_name"),
        content=item["content"],
        email=item["email"],
    )
