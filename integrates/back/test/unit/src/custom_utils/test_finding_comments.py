from custom_utils.finding_comments import (
    format_finding_consulting_resolve,
)
from datetime import (
    datetime,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_format_finding_consulting_resolve() -> None:
    test_data = FindingComment(
        finding_id="422286126",
        id="1566336916294",
        parent_id="0",
        comment_type=CommentType.COMMENT,
        creation_date=datetime.fromisoformat("2019-08-20T21:35:16+00:00"),
        content="This is a comenting test",
        email="unittest@fluidattacks.com",
        full_name="Unit Test",
    )

    assert (
        format_finding_consulting_resolve(finding_comment=test_data)[
            "fullname"
        ]
        == "Fluid Attacks"
    )
    assert (
        format_finding_consulting_resolve(
            finding_comment=test_data, target_email="userat@fluidattacks.com"
        )["fullname"]
        == "Unit Test"
    )
    assert (
        format_finding_consulting_resolve(
            finding_comment=test_data, is_draft=True
        )["fullname"]
        == "Unit Test"
    )

    test_data = test_data._replace(
        email="unittest@gmail.com",
    )
    assert (
        format_finding_consulting_resolve(finding_comment=test_data)[
            "fullname"
        ]
        == "Unit Test"
    )

    test_data = test_data._replace(full_name=None)
    assert (
        format_finding_consulting_resolve(finding_comment=test_data)[
            "fullname"
        ]
        == "unittest@gmail.com"
    )
