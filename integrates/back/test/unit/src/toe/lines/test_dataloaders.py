from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.toe_lines.types import (
    GroupToeLinesRequest,
    RootToeLinesRequest,
    SortsSuggestion,
    ToeLines,
    ToeLinesConnection,
    ToeLinesEdge,
    ToeLinesRequest,
    ToeLinesState,
)
from dynamodb.types import (
    PageInfo,
)
import pytest

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get() -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    root_id = "4039d098-ffc5-4984-8ed3-eb17bca98e19"
    filename = "test/test#.config"
    toe_lines = await loaders.toe_lines.load(
        ToeLinesRequest(
            group_name=group_name, root_id=root_id, filename=filename
        )
    )
    assert toe_lines == ToeLines(
        filename="test/test#.config",
        group_name="unittesting",
        root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
        state=ToeLinesState(
            attacked_at=datetime.fromisoformat("2021-02-20T05:00:00+00:00"),
            attacked_by="test2@test.com",
            attacked_lines=4,
            be_present=True,
            be_present_until=None,
            comments="comment 1",
            has_vulnerabilities=False,
            last_author="user@gmail.com",
            last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
            last_commit_date=datetime.fromisoformat(
                "2020-11-15T15:41:04+00:00"
            ),
            loc=180,
            first_attack_at=datetime.fromisoformat(
                "2020-02-19T15:41:04+00:00"
            ),
            modified_by="test2@test.com",
            modified_date=datetime.fromisoformat("2020-11-15T15:41:04+00:00"),
            seen_at=datetime.fromisoformat("2020-02-01T15:41:04+00:00"),
            sorts_risk_level=80,
            sorts_priority_factor=70,
            sorts_risk_level_date=datetime.fromisoformat(
                "2021-02-20T05:00:00+00:00"
            ),
            sorts_suggestions=[
                SortsSuggestion(
                    finding_title="083. XML injection (XXE)", probability=90
                ),
                SortsSuggestion(
                    finding_title=(
                        "033. Password change without identity check"
                    ),
                    probability=50,
                ),
            ],
        ),
    )
    group_name = "unittesting"
    root_id = "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
    filename = "test2/test.sh"
    toe_lines = await loaders.toe_lines.load(
        ToeLinesRequest(
            group_name=group_name, root_id=root_id, filename=filename
        )
    )
    assert toe_lines == ToeLines(
        filename="test2/test.sh",
        group_name="unittesting",
        root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
        state=ToeLinesState(
            attacked_at=datetime.fromisoformat("2021-01-20T05:00:00+00:00"),
            attacked_by="test@test.com",
            attacked_lines=120,
            be_present=False,
            be_present_until=datetime.fromisoformat(
                "2021-01-01T15:41:04+00:00"
            ),
            comments="comment 2",
            first_attack_at=datetime.fromisoformat(
                "2020-01-19T15:41:04+00:00"
            ),
            has_vulnerabilities=False,
            last_author="user@gmail.com",
            last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1",
            last_commit_date=datetime.fromisoformat(
                "2020-11-16T15:41:04+00:00"
            ),
            loc=172,
            modified_by="test2@test.com",
            modified_date=datetime.fromisoformat("2020-11-16T15:41:04+00:00"),
            seen_at=datetime.fromisoformat("2020-01-01T15:41:04+00:00"),
            sorts_risk_level=0,
            sorts_priority_factor=10,
            sorts_risk_level_date=datetime.fromisoformat(
                "2021-04-10T05:00:00+00:00"
            ),
            sorts_suggestions=[
                SortsSuggestion(
                    finding_title="027. Insecure file upload", probability=100
                ),
            ],
        ),
    )


async def test_get_by_group() -> None:
    group_name = "unittesting"
    loaders = get_new_context()
    group_toe_lines = await loaders.group_toe_lines.load(
        GroupToeLinesRequest(group_name=group_name)
    )
    assert group_toe_lines == ToeLinesConnection(
        edges=(
            ToeLinesEdge(
                node=ToeLines(
                    filename="test/test#.config",
                    group_name="unittesting",
                    root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    state=ToeLinesState(
                        attacked_at=datetime.fromisoformat(
                            "2021-02-20T05:00:00+00:00"
                        ),
                        attacked_by="test2@test.com",
                        attacked_lines=4,
                        be_present=True,
                        be_present_until=None,
                        comments="comment 1",
                        first_attack_at=datetime.fromisoformat(
                            "2020-02-19T15:41:04+00:00"
                        ),
                        has_vulnerabilities=False,
                        last_author="user@gmail.com",
                        last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                        last_commit_date=datetime.fromisoformat(
                            "2020-11-15T15:41:04+00:00"
                        ),
                        loc=180,
                        modified_by="test2@test.com",
                        modified_date=datetime.fromisoformat(
                            "2020-11-15T15:41:04+00:00"
                        ),
                        seen_at=datetime.fromisoformat(
                            "2020-02-01T15:41:04+00:00"
                        ),
                        sorts_risk_level=80,
                        sorts_priority_factor=70,
                        sorts_risk_level_date=datetime.fromisoformat(
                            "2021-02-20T05:00:00+00:00"
                        ),
                        sorts_suggestions=[
                            SortsSuggestion(
                                finding_title="083. XML injection (XXE)",
                                probability=90,
                            ),
                            SortsSuggestion(
                                finding_title="033. Password change without "
                                "identity check",
                                probability=50,
                            ),
                        ],
                    ),
                ),
                cursor=(
                    "eyJwayI6ICJHUk9VUCN1bml0dGVzdGluZyIsICJzayI6ICJMSU"
                    "5FUyNST09UIzQwMzlkMDk4LWZmYzUtNDk4NC04ZWQzLWViMTdi"
                    "Y2E5OGUxOSNGSUxFTkFNRSN0ZXN0L3Rlc3QjLmNvbmZpZyJ9"
                ),
            ),
            ToeLinesEdge(
                node=ToeLines(
                    filename="universe/path/to/file3.ext",
                    group_name="unittesting",
                    root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    seen_first_time_by=None,
                    state=ToeLinesState(
                        attacked_at=datetime.fromisoformat(
                            "2021-02-20T05:00:00+00:00"
                        ),
                        attacked_by="test2@test.com",
                        attacked_lines=4,
                        be_present=True,
                        be_present_until=None,
                        comments="comment 1",
                        first_attack_at=datetime.fromisoformat(
                            "2020-02-19T15:41:04+00:00"
                        ),
                        has_vulnerabilities=False,
                        last_author="user@gmail.com",
                        last_commit="e17059d1e17059d1e17059d1e17059d1e17059d1",
                        last_commit_date=datetime.fromisoformat(
                            "2020-11-15T15:41:04+00:00"
                        ),
                        loc=350,
                        modified_by="test2@test.com",
                        modified_date=datetime.fromisoformat(
                            "2020-11-15T15:41:04+00:00"
                        ),
                        seen_at=datetime.fromisoformat(
                            "2020-02-01T15:41:04+00:00"
                        ),
                        sorts_risk_level=80,
                        sorts_priority_factor=70,
                        sorts_risk_level_date=datetime.fromisoformat(
                            "2021-03-30T05:00:00+00:00"
                        ),
                        sorts_suggestions=[
                            SortsSuggestion(
                                finding_title="083. XML injection (XXE)",
                                probability=90,
                            ),
                            SortsSuggestion(
                                finding_title=(
                                    "033. Password change without identity "
                                    "check"
                                ),
                                probability=50,
                            ),
                        ],
                    ),
                ),
                cursor=(
                    "eyJwayI6ICJHUk9VUCN1bml0dGVzdGluZyIsICJzayI6ICJMSU"
                    "5FUyNST09UIzQwMzlkMDk4LWZmYzUtNDk4NC04ZWQzLWViMTdi"
                    "Y2E5OGUxOSNGSUxFTkFNRSN1bml2ZXJzZS9wYXRoL3RvL2ZpbG"
                    "UzLmV4dCJ9"
                ),
            ),
            ToeLinesEdge(
                node=ToeLines(
                    filename="test2/test.sh",
                    group_name="unittesting",
                    root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                    state=ToeLinesState(
                        attacked_at=datetime.fromisoformat(
                            "2021-01-20T05:00:00+00:00"
                        ),
                        attacked_by="test@test.com",
                        attacked_lines=120,
                        be_present=False,
                        be_present_until=datetime.fromisoformat(
                            "2021-01-01T15:41:04+00:00"
                        ),
                        comments="comment 2",
                        first_attack_at=datetime.fromisoformat(
                            "2020-01-19T15:41:04+00:00"
                        ),
                        has_vulnerabilities=False,
                        last_author="user@gmail.com",
                        last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1",
                        last_commit_date=datetime.fromisoformat(
                            "2020-11-16T15:41:04+00:00"
                        ),
                        loc=172,
                        modified_by="test2@test.com",
                        modified_date=datetime.fromisoformat(
                            "2020-11-16T15:41:04+00:00"
                        ),
                        seen_at=datetime.fromisoformat(
                            "2020-01-01T15:41:04+00:00"
                        ),
                        sorts_risk_level=0,
                        sorts_priority_factor=10,
                        sorts_risk_level_date=datetime.fromisoformat(
                            "2021-04-10T05:00:00+00:00"
                        ),
                        sorts_suggestions=[
                            SortsSuggestion(
                                finding_title="027. Insecure file upload",
                                probability=100,
                            ),
                        ],
                    ),
                ),
                cursor="eyJwayI6ICJHUk9VUCN1bml0dGVzdGluZyIsICJzayI6ICJMSU5FUy"
                "NST09UIzc2NWIxZDBmLWI2ZmItNDQ4NS1iNGUyLTJjMmNiMTU1NWIx"
                "YSNGSUxFTkFNRSN0ZXN0Mi90ZXN0LnNoIn0=",
            ),
        ),
        page_info=PageInfo(has_next_page=False, end_cursor="bnVsbA=="),
    )


async def test_get_by_root() -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    root_id = "4039d098-ffc5-4984-8ed3-eb17bca98e19"
    root_toe_lines = await loaders.root_toe_lines.load(
        RootToeLinesRequest(group_name=group_name, root_id=root_id)
    )
    assert root_toe_lines == ToeLinesConnection(
        edges=(
            ToeLinesEdge(
                node=ToeLines(
                    filename="test/test#.config",
                    group_name="unittesting",
                    root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    state=ToeLinesState(
                        attacked_at=datetime.fromisoformat(
                            "2021-02-20T05:00:00+00:00"
                        ),
                        attacked_by="test2@test.com",
                        attacked_lines=4,
                        be_present=True,
                        be_present_until=None,
                        comments="comment 1",
                        first_attack_at=datetime.fromisoformat(
                            "2020-02-19T15:41:04+00:00"
                        ),
                        has_vulnerabilities=False,
                        last_author="user@gmail.com",
                        last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                        last_commit_date=datetime.fromisoformat(
                            "2020-11-15T15:41:04+00:00"
                        ),
                        loc=180,
                        modified_by="test2@test.com",
                        modified_date=datetime.fromisoformat(
                            "2020-11-15T15:41:04+00:00"
                        ),
                        seen_at=datetime.fromisoformat(
                            "2020-02-01T15:41:04+00:00"
                        ),
                        sorts_risk_level=80,
                        sorts_priority_factor=70,
                        sorts_risk_level_date=datetime.fromisoformat(
                            "2021-02-20T05:00:00+00:00"
                        ),
                        sorts_suggestions=[
                            SortsSuggestion(
                                finding_title="083. XML injection (XXE)",
                                probability=90,
                            ),
                            SortsSuggestion(
                                finding_title="033. Password change without "
                                "identity check",
                                probability=50,
                            ),
                        ],
                    ),
                ),
                cursor=(
                    "eyJwayI6ICJHUk9VUCN1bml0dGVzdGluZyIsICJzayI6ICJMSU"
                    "5FUyNST09UIzQwMzlkMDk4LWZmYzUtNDk4NC04ZWQzLWViMTdi"
                    "Y2E5OGUxOSNGSUxFTkFNRSN0ZXN0L3Rlc3QjLmNvbmZpZyJ9"
                ),
            ),
            ToeLinesEdge(
                node=ToeLines(
                    filename="universe/path/to/file3.ext",
                    group_name="unittesting",
                    root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    seen_first_time_by=None,
                    state=ToeLinesState(
                        attacked_at=datetime.fromisoformat(
                            "2021-02-20T05:00:00+00:00"
                        ),
                        attacked_by="test2@test.com",
                        attacked_lines=4,
                        be_present=True,
                        be_present_until=None,
                        comments="comment 1",
                        first_attack_at=datetime.fromisoformat(
                            "2020-02-19T15:41:04+00:00"
                        ),
                        has_vulnerabilities=False,
                        last_author="user@gmail.com",
                        last_commit="e17059d1e17059d1e17059d1e17059d1e17059d1",
                        last_commit_date=datetime.fromisoformat(
                            "2020-11-15T15:41:04+00:00"
                        ),
                        loc=350,
                        modified_by="test2@test.com",
                        modified_date=datetime.fromisoformat(
                            "2020-11-15T15:41:04+00:00"
                        ),
                        seen_at=datetime.fromisoformat(
                            "2020-02-01T15:41:04+00:00"
                        ),
                        sorts_risk_level=80,
                        sorts_priority_factor=70,
                        sorts_risk_level_date=datetime.fromisoformat(
                            "2021-03-30T05:00:00+00:00"
                        ),
                        sorts_suggestions=[
                            SortsSuggestion(
                                finding_title="083. XML injection (XXE)",
                                probability=90,
                            ),
                            SortsSuggestion(
                                finding_title=(
                                    "033. Password change without identity "
                                    "check"
                                ),
                                probability=50,
                            ),
                        ],
                    ),
                ),
                cursor=(
                    "eyJwayI6ICJHUk9VUCN1bml0dGVzdGluZyIsICJzayI6ICJMSU"
                    "5FUyNST09UIzQwMzlkMDk4LWZmYzUtNDk4NC04ZWQzLWViMTdi"
                    "Y2E5OGUxOSNGSUxFTkFNRSN1bml2ZXJzZS9wYXRoL3RvL2ZpbG"
                    "UzLmV4dCJ9"
                ),
            ),
        ),
        page_info=PageInfo(has_next_page=False, end_cursor="bnVsbA=="),
    )
    group_name = "unittesting"
    root_id = "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
    root_toe_lines = await loaders.root_toe_lines.load(
        RootToeLinesRequest(group_name=group_name, root_id=root_id)
    )
    assert root_toe_lines == ToeLinesConnection(
        edges=(
            ToeLinesEdge(
                node=ToeLines(
                    filename="test2/test.sh",
                    group_name="unittesting",
                    root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                    state=ToeLinesState(
                        attacked_at=datetime.fromisoformat(
                            "2021-01-20T05:00:00+00:00"
                        ),
                        attacked_by="test@test.com",
                        attacked_lines=120,
                        be_present=False,
                        be_present_until=datetime.fromisoformat(
                            "2021-01-01T15:41:04+00:00"
                        ),
                        comments="comment 2",
                        first_attack_at=datetime.fromisoformat(
                            "2020-01-19T15:41:04+00:00"
                        ),
                        has_vulnerabilities=False,
                        last_author="user@gmail.com",
                        last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1",
                        last_commit_date=datetime.fromisoformat(
                            "2020-11-16T15:41:04+00:00"
                        ),
                        loc=172,
                        modified_by="test2@test.com",
                        modified_date=datetime.fromisoformat(
                            "2020-11-16T15:41:04+00:00"
                        ),
                        seen_at=datetime.fromisoformat(
                            "2020-01-01T15:41:04+00:00"
                        ),
                        sorts_risk_level=0,
                        sorts_priority_factor=10,
                        sorts_risk_level_date=datetime.fromisoformat(
                            "2021-04-10T05:00:00+00:00"
                        ),
                        sorts_suggestions=[
                            SortsSuggestion(
                                finding_title="027. Insecure file upload",
                                probability=100,
                            ),
                        ],
                    ),
                ),
                cursor="eyJwayI6ICJHUk9VUCN1bml0dGVzdGluZyIsICJzayI6ICJMSU5FUy"
                "NST09UIzc2NWIxZDBmLWI2ZmItNDQ4NS1iNGUyLTJjMmNiMTU1NWIx"
                "YSNGSUxFTkFNRSN0ZXN0Mi90ZXN0LnNoIn0=",
            ),
        ),
        page_info=PageInfo(has_next_page=False, end_cursor="bnVsbA=="),
    )
