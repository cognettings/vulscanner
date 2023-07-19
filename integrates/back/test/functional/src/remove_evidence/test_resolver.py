from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_evidence")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_remove_evidence(populate: bool, email: str) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        finding="3c475384-834c-47b0-ac71-a41a022e401c",
        evidence="EVIDENCE1",
    )
    assert "errors" not in result
    assert "success" in result["data"]["removeEvidence"]
    assert result["data"]["removeEvidence"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_evidence")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
    ],
)
async def test_remove_evidence_fail_1(populate: bool, email: str) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        finding="3c475384-834c-47b0-ac71-a41a022e401c",
        evidence="EVIDENCE1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Exception - Evidence not found"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_evidence")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_remove_evidence_fail_2(populate: bool, email: str) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        finding="3c475384-834c-47b0-ac71-a41a022e401c",
        evidence="EVIDENCE1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
