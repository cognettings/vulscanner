from . import (
    get_result,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("drafts_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_draft(
    populate: bool,
    email: str,
) -> None:
    assert populate
    result: dict = await get_result(user=email)
    draft = result["data"]["me"]["draftsConnection"]["edges"]
    assert len(draft) == 1
    assert draft[0]["node"]["currentState"] == "CREATED"
    assert draft[0]["node"]["groupName"] == "group1"
    assert draft[0]["node"]["hacker"] == "admin@fluidattacks.com"
    assert draft[0]["node"]["id"] == "475041521"
    assert draft[0]["node"]["lastStateDate"] == "2017-04-07 19:45:11"
    assert draft[0]["node"]["openVulnerabilities"] == 0
    assert draft[0]["node"]["reportDate"] == "2017-04-07 19:45:11"
    assert draft[0]["node"]["severityScore"] == 4.1
    assert (
        draft[0]["node"]["title"]
        == "060. Insecure service configuration - Host verification"
    )
