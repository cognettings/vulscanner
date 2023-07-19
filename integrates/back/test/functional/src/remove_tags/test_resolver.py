from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_tags")
async def test_remove_single_tag(populate: bool) -> None:
    assert populate
    user_email = "hacker@gmail.com"
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    vuln_id: str = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
    tag_to_remove = "tag3"

    loaders = get_new_context()
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.tags == ["tag1", "tag2", "tag3"]

    result: dict[str, Any] = await get_result(
        user=user_email,
        finding=finding_id,
        vuln_id=vuln_id,
        tag=tag_to_remove,
    )
    assert "errors" not in result
    assert "success" in result["data"]["removeTags"]
    assert result["data"]["removeTags"]["success"]

    loaders.vulnerability.clear(vuln_id)
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.tags == ["tag1", "tag2"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_tags")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_remove_all_tags(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    vuln_id: str = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
    result: dict[str, Any] = await get_result(
        user=email, finding=finding_id, vuln_id=vuln_id
    )
    assert "errors" not in result
    assert "success" in result["data"]["removeTags"]
    assert result["data"]["removeTags"]["success"]

    loaders = get_new_context()
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.tags is None


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_tags")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["reattacker@gmail.com"],
    ],
)
async def test_remove_tags_fail(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    vuln_uuid: str = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
    result: dict[str, Any] = await get_result(
        user=email, finding=finding_id, vuln_id=vuln_uuid
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
