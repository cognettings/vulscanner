from back.test.unit.src.utils import (
    get_module_at_test,
)
from custom_utils.datetime import (
    get_utc_now,
)
from dataloaders import (
    get_new_context,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
    FindingCommentsRequest,
)
from findings.domain import (
    add_comment,
)
import pytest
import time

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_add_comment() -> None:
    loaders = get_new_context()
    finding_id = "463461507"
    current_time = get_utc_now()
    comment_id = str(round(time.time() * 1000))
    comment_data = FindingComment(
        finding_id=finding_id,
        comment_type=CommentType.COMMENT,
        id=comment_id,
        content="Test comment",
        creation_date=current_time,
        full_name="unittesting",
        parent_id="0",
        email="unittest@fluidattacks.com",
    )
    await add_comment(
        loaders=loaders,
        user_email="unittest@fluidattacks.com",
        comment_data=comment_data,
        finding_id=finding_id,
        group_name="unittesting",
    )
    loaders = get_new_context()
    finding_comments = await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.COMMENT, finding_id=finding_id
        )
    ) + await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.VERIFICATION, finding_id=finding_id
        )
    )
    assert finding_comments[-1].content == "Test comment"
    assert finding_comments[-1].full_name == "unittesting"

    current_time = get_utc_now()
    new_comment_data = comment_data._replace(
        id=str(round(time.time() * 1000)),
        creation_date=current_time,
        parent_id=str(comment_id),
    )
    await add_comment(
        loaders=loaders,
        user_email="unittest@fluidattacks.com",
        comment_data=new_comment_data,
        finding_id=finding_id,
        group_name="unittesting",
    )
    new_loaders = get_new_context()
    new_finding_comments = await new_loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.COMMENT, finding_id=finding_id
        )
    )
    assert new_finding_comments[-1].content == "Test comment"
    assert new_finding_comments[-1].parent_id == str(comment_id)
