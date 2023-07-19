from . import (
    get_result,
)
from asyncio import (
    sleep,
)
from dataloaders import (
    get_new_context,
)
from db_model.events.enums import (
    EventType,
)
from db_model.events.types import (
    EventRequest,
)
import pytest
from search.operations import (
    search,
)
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("streams_process_events")
@pytest.mark.parametrize(
    [
        "email",
        "event_id",
        "event_type",
        "solving_reason",
        "other_solving_reason",
        "partition_key",
        "sort_key",
    ],
    [
        [
            "admin@gmail.com",
            "418900971",
            "DATA_UPDATE_REQUIRED",
            "DATA_UPDATED",
            "",
            "EVENT#418900971",
            "GROUP#group1",
        ],
        [
            "admin@gmail.com",
            "418900972",
            "DATA_UPDATE_REQUIRED",
            "DATA_UPDATED",
            "",
            "EVENT#418900972",
            "GROUP#group1",
        ],
        [
            "admin@gmail.com",
            "418900973",
            "DATA_UPDATE_REQUIRED",
            "DATA_UPDATED",
            "",
            "EVENT#418900973",
            "GROUP#group1",
        ],
        [
            "admin@gmail.com",
            "418900974",
            "DATA_UPDATE_REQUIRED",
            "DATA_UPDATED",
            "",
            "EVENT#418900974",
            "GROUP#group1",
        ],
        [
            "admin@gmail.com",
            "418900975",
            "DATA_UPDATE_REQUIRED",
            "DATA_UPDATED",
            "",
            "EVENT#418900975",
            "GROUP#group1",
        ],
    ],
)
# pylint: disable=too-many-arguments
async def test_streams_process_events(
    populate: bool,
    email: str,
    event_id: str,
    event_type: str,
    solving_reason: str,
    other_solving_reason: str,
    partition_key: str,
    sort_key: str,
) -> None:
    assert populate
    loaders = get_new_context()
    event = await loaders.event.load(
        EventRequest(event_id=event_id, group_name="group1")
    )
    assert event
    assert event.type == EventType.OTHER

    query: str = f"""
    "match": {{
        "query": "{event_id}",
        "fields": ["id"]
    }}
    """

    search_result = await search(index="events", limit=10, query=query)
    item = search_result.items[0]

    assert search_result.total == 1
    assert item["id"] == event_id
    assert item["type"] == EventType.OTHER

    result: dict[str, Any] = await get_result(
        user=email,
        event_id=event_id,
        event_type=event_type,
        solving_reason=solving_reason,
        other_solving_reason=other_solving_reason,
    )

    assert "errors" not in result
    assert "success" in result["data"]["updateEvent"]

    loaders.event.clear_all()
    loaders = get_new_context()

    event = await loaders.event.load(
        EventRequest(event_id=event_id, group_name="group1")
    )
    assert event
    assert event.type == event_type

    await sleep(5)

    search_result = await search(index="events", limit=10, query=query)
    item = search_result.items[0]

    assert search_result.total == 1
    assert item["id"] == event_id
    assert item["pk"] == partition_key
    assert item["sk"] == sort_key
    assert item["type"] == event_type
