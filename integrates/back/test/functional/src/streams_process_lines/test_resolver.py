from . import (
    get_result,
)
from asyncio import (
    sleep,
)
import pytest
from search.operations import (
    search,
)
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("streams_process_lines")
@pytest.mark.parametrize(
    [
        "email",
        "filename",
        "root_id",
    ],
    [
        [
            "admin@fluidattacks.com",
            "test/test1.py",
            "63298a73-9dff-46cf-b42d-9b2f01a56690",
        ],
    ],
)
async def test_streams_process_lines(
    populate: bool,
    email: str,
    filename: str,
    root_id: str,
) -> None:
    assert populate

    partition_key: str = "GROUP#group1"
    sort_key: str = f"LINES#ROOT#{root_id}#FILENAME#{filename}"

    query: str = f""""
    "match": {{
        "root_id": "{root_id}",
        "group_name": "group1"
    }}
    """

    search_result = await search(index="toe_lines", limit=10, query=query)

    assert search_result.total == 0

    result: dict[str, Any] = await get_result(
        user=email,
        filename=filename,
        group_name="group1",
        root_id=root_id,
        last_author="test@test.com",
        last_commit="d9e4beba70c4f34d6117c3b0c23ebe6b2bff66c4",
        loc=50,
        modified_date="2020-11-19T13:37:10+00:00",
    )

    assert "errors" not in result

    await sleep(5)

    search_result = await search(index="toe_lines", limit=10, query=query)

    assert search_result.total == 1

    item = search_result.items[0]

    assert item["pk"] == partition_key
    assert item["sk"] == sort_key
