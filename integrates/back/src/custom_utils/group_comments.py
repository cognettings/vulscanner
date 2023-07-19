from custom_utils.datetime import (
    format_comment_datetime,
)
from custom_utils.validations import (
    is_fluid_staff,
)
from db_model.group_comments.types import (
    GroupComment,
)
from dynamodb.types import (
    Item,
)


def _get_email(*, objective_data: GroupComment, target_email: str) -> str:
    objective_email = objective_data.email
    if is_fluid_staff(objective_email) and not is_fluid_staff(target_email):
        return "help@fluidattacks.com"

    return objective_email


def _get_fullname(*, objective_data: GroupComment, target_email: str) -> str:
    objective_email = objective_data.email
    objective_possible_fullname = (
        objective_data.full_name if objective_data.full_name else None
    )
    real_name = objective_possible_fullname or objective_email

    if is_fluid_staff(objective_email) and not is_fluid_staff(target_email):
        return "Fluid Attacks"

    return real_name


def format_group_consulting_resolve(
    *, group_comment: GroupComment, target_email: str
) -> Item:
    email = _get_email(objective_data=group_comment, target_email=target_email)
    fullname = _get_fullname(
        objective_data=group_comment, target_email=target_email
    )
    return {
        "content": group_comment.content,
        "created": format_comment_datetime(group_comment.creation_date),
        "email": email,
        "fullname": fullname if fullname else email,
        "id": group_comment.id,
        "modified": format_comment_datetime(group_comment.creation_date),
        "parent": group_comment.parent_id,
    }
