from . import (
    get_events_query,
    get_events_query_2,
    get_result,
)
import json
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("events")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_get_events(populate: bool, email: str) -> None:
    assert populate
    expected: list[dict[str, str]] = [
        {
            "id": "418900971",
            "groupName": "group1",
            "eventStatus": "CREATED",
            "detail": "ARM unit test1",
        },
        {
            "id": "418900980",
            "groupName": "group1",
            "eventStatus": "CREATED",
            "detail": "ARM unit test2",
        },
    ]
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(user=email, group=group_name)
    assert "errors" not in result
    assert "events" in result["data"]
    assert result["data"]["events"] == expected


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("events")
@pytest.mark.parametrize(
    ["email", "group"],
    [
        ["admin@gmail.com", "group1"],
    ],
)
async def test_get_events_query(
    populate: bool,
    email: str,
    group: str,
    snapshot: Any,
) -> None:
    """
    Test for {QueryName}
    in /front/.../Dashboard/group/queries.ts
    """
    assert populate
    result: dict = await get_events_query(user=email, group=group)
    json_result = str(json.dumps(result, indent=2))
    snapshot.assert_match(json_result, "snapshot.json")


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("events")
@pytest.mark.parametrize(
    ["email", "group"],
    [
        ["admin@gmail.com", "group1"],
    ],
)
async def test_get_events_query_2(
    populate: bool,
    email: str,
    group: str,
    snapshot: Any,
) -> None:
    """
    Test for GetEventsQuery
    in /front/.../GroupEventsView/queries.ts
    """
    assert populate
    result: dict = await get_events_query_2(
        user=email,
        group=group,
    )
    json_result = json.dumps(result, indent=2)
    snapshot.assert_match(str(json_result), "snapshot.json")
