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
@pytest.mark.resolver_test_group("streams_process_executions")
@pytest.mark.parametrize(
    [
        "email",
        "commit",
        "group_name",
        "execution_id",
        "partition_key",
        "sort_key",
    ],
    [
        [
            "service_forces@gmail.com",
            "2e7b34c1358db2ff4123c3c76e7fe3bf9f2838f2",
            "group1",
            "18c1e735a73243f2ab1ee0757041f80e",
            "EXEC#18c1e735a73243f2ab1ee0757041f80e",
            "GROUP#group1",
        ],
    ],
)
# pylint: disable=too-many-arguments
async def test_streams_process_executions(
    populate: bool,
    email: str,
    commit: str,
    group_name: str,
    execution_id: str,
    partition_key: str,
    sort_key: str,
) -> None:
    assert populate

    query: str = f""""
    "match": {{
        "commit": "{commit}"
    }}
    """
    search_result = await search(
        index="forces_executions",
        limit=10,
        query=query,
    )

    assert search_result.total == 0

    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" not in result
    assert result["data"]["addForcesExecution"]["success"]

    await sleep(5)

    search_result = await search(
        index="forces_executions",
        limit=10,
        query=query,
    )
    item = search_result.items[0]
    assert search_result.total == 1
    assert item["id"] == execution_id
    assert item["commit"] == commit
    assert item["group_name"] == group_name
    assert item["pk"] == partition_key
    assert item["sk"] == sort_key


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("streams_process_executions")
@pytest.mark.parametrize(
    [
        "email",
        "commit",
        "group_name",
    ],
    [
        [
            "admin@gmail.com",
            "2e7b34c1358db2ff4123c3c76e7fe3bf9f2838f2",
            "group1",
        ],
        [
            "user@gmail.com",
            "2e7b34c1358db2ff4123c3c76e7fe3bf9f2838f2",
            "group1",
        ],
        [
            "user_manager@gmail.com",
            "2e7b34c1358db2ff4123c3c76e7fe3bf9f2838f2",
            "group1",
        ],
        [
            "vulnerability_manager@gmail.com",
            "2e7b34c1358db2ff4123c3c76e7fe3bf9f2838f2",
            "group1",
        ],
        [
            "hacker@gmail.com",
            "2e7b34c1358db2ff4123c3c76e7fe3bf9f2838f2",
            "group1",
        ],
        [
            "reattacker@gmail.com",
            "2e7b34c1358db2ff4123c3c76e7fe3bf9f2838f2",
            "group1",
        ],
        [
            "resourcer@gmail.com",
            "2e7b34c1358db2ff4123c3c76e7fe3bf9f2838f2",
            "group1",
        ],
        [
            "reviewer@gmail.com",
            "2e7b34c1358db2ff4123c3c76e7fe3bf9f2838f2",
            "group1",
        ],
    ],
)
async def test_streams_process_executions_no_add(
    populate: bool,
    email: str,
    commit: str,
    group_name: str,
) -> None:
    assert populate

    query: str = f""""
    "match": {{
        "commit": "{commit}"
    }}
    """
    search_result = await search(
        index="forces_executions",
        limit=10,
        query=query,
    )

    assert search_result.total == 1

    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"

    await sleep(5)

    search_result = await search(
        index="forces_executions",
        limit=10,
        query=query,
    )
    assert search_result.total == 1
