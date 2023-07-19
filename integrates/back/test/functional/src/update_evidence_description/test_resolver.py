from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_evidence_description")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
    ],
)
async def test_update_evidence_description(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    description: str = "this is a test description"
    evidence_name: str = "EVIDENCE1"
    result: dict[str, Any] = await get_result(
        user=email,
        description=description,
        finding_id=finding_id,
        evidence=evidence_name,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateEvidenceDescription"]
    assert result["data"]["updateEvidenceDescription"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_evidence_description")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["resourcer@fluidattacks.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_update_evidence_description_fail(
    populate: bool, email: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    description: str = "this is a test description"
    evidence_name: str = "EVIDENCE1"
    result: dict[str, Any] = await get_result(
        user=email,
        description=description,
        finding_id=finding_id,
        evidence=evidence_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
