from . import (
    get_finding_header,
    get_finding_header_2,
    get_finding_info,
    get_finding_nzr_vulns,
    get_finding_title,
    get_finding_vuln_drafts,
    get_finding_zr_vulns,
    get_result,
)
from freezegun import (
    freeze_time,
)
import json
import os
import pytest
from typing import (
    Any,
)

path = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("finding")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
@freeze_time("2021-03-31")
async def test_get_finding(populate: bool, email: str, snapshot: Any) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict = await get_result(
        user=email, finding_id=finding_id, should_get_zero_risk=True
    )
    assert "errors" not in result
    json_result = str(json.dumps(result, indent=2))
    snapshot.assert_match(json_result, "snapshot.json")


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("finding")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@fluidattacks.com"],
        ["reviewer@gmail.com"],
    ],
)
@freeze_time("2021-03-31")
async def test_get_finding_consulting(
    populate: bool, email: str, snapshot: Any
) -> None:
    assert populate
    finding_id: str = "41e50cb7-5343-402d-bb98-55e8bf5e9cc4"
    result: dict = await get_result(
        user=email,
        finding_id=finding_id,
    )
    assert "errors" not in result
    json_result = str(json.dumps(result, indent=2))
    snapshot.assert_match(json_result, "snapshot.json")


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("finding")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@fluidattacks.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
@freeze_time("2021-03-31")
async def test_get_finding_fail(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict = await get_result(
        user=email, finding_id=finding_id, should_get_zero_risk=True
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("finding")
@pytest.mark.parametrize(
    ["email", "pag"],
    [
        ["user_manager@gmail.com", None],
        ["user_manager@gmail.com", 1],
        ["user_manager@gmail.com", 2],
    ],
)
async def test_get_finding_nzr_vulns_1(
    populate: bool, email: str, pag: int | None, snapshot: Any
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict = await get_finding_nzr_vulns(
        user=email, finding_id=finding_id, first=pag
    )
    json_result = str(json.dumps(result, indent=2))
    snapshot.assert_match(json_result, "snapshot.json")


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("finding")
@pytest.mark.parametrize(
    ["email", "pag"],
    [
        ["user_manager@gmail.com", None],
        ["user_manager@gmail.com", 2],
    ],
)
async def test_get_finding_nzr_vulns_2(
    populate: bool, email: str, pag: int | None, snapshot: Any
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict = await get_finding_nzr_vulns(
        user=email, finding_id=finding_id, first=pag
    )
    json_result = str(json.dumps(result, indent=2))
    snapshot.assert_match(json_result, "snapshot.json")


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("finding")
@pytest.mark.parametrize(
    ["email", "can_retrieve_drafts"],
    [
        ["admin@fluidattacks.com", True],
    ],
)
async def test_get_finding_vuln_drafts(
    populate: bool, email: str, can_retrieve_drafts: bool, snapshot: Any
) -> None:
    """
    Test for GetFindingVulnDrafts in
    /front/.../VulnerabilitiesView/queries.ts
    """
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict = await get_finding_vuln_drafts(
        user=email,
        finding_id=finding_id,
        can_retrieve_drafts=can_retrieve_drafts,
    )
    json_result = str(json.dumps(result, indent=2))
    snapshot.assert_match(json_result, "snapshot.json")


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("finding")
@pytest.mark.parametrize(
    ["email", "can_retrieve_zero_risk"],
    [
        ["admin@fluidattacks.com", True],
        ["admin@fluidattacks.com", False],
        ["admin@gmail.com", True],
        ["admin@gmail.com", False],
        ["reviewer@gmail.com", True],
        ["reviewer@gmail.com", False],
        ["architect@gmail.com", True],
        ["architect@gmail.com", False],
    ],
)
async def test_get_finding_zr_vulns(
    populate: bool,
    email: str,
    snapshot: Any,
    can_retrieve_zero_risk: bool,
) -> None:
    """
    Test for GetFindingZrVulns
    in /front/.../VulnerabilitiesView/queries.ts
    """
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict = await get_finding_zr_vulns(
        user=email,
        finding_id=finding_id,
        can_retrieve_zero_risk=can_retrieve_zero_risk,
    )
    json_result = str(json.dumps(result, indent=2))
    snapshot.assert_match(json_result, "snapshot.json")


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("finding")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
        ["admin@gmail.com"],
    ],
)
async def test_get_finding_info(
    populate: bool,
    email: str,
    snapshot: Any,
) -> None:
    """
    Test for GetFindingInfo
    in /front/.../VulnerabilitiesView/queries.ts
    """
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict = await get_finding_info(
        user=email,
        finding_id=finding_id,
    )
    json_result = str(json.dumps(result, indent=2))
    snapshot.assert_match(json_result, "snapshot.json")


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("finding")
@pytest.mark.parametrize(
    ["email", "finding"],
    [
        ["admin@gmail.com", "3c475384-834c-47b0-ac71-a41a022e401c"],
    ],
)
async def test_get_finding_header(
    populate: bool,
    email: str,
    finding: str,
    snapshot: Any,
) -> None:
    """
    Test for GetFindingHeader
    in /common/utils/retrieves/src/queries.ts
    """
    assert populate
    result: dict = await get_finding_header(user=email, finding_id=finding)
    json_result = json.dumps(result, indent=2)
    snapshot.assert_match(str(json_result), "snapshot.json")


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("finding")
@pytest.mark.parametrize(
    ["email", "finding"],
    [
        ["admin@gmail.com", "3c475384-834c-47b0-ac71-a41a022e401c"],
    ],
)
async def test_get_finding_header_2(
    populate: bool,
    email: str,
    finding: str,
    snapshot: Any,
) -> None:
    """
    Test for GetFindingHeader
    in /front/.../Finding-content/queries.ts
    """
    assert populate
    result: dict = await get_finding_header_2(user=email, finding_id=finding)
    json_result = json.dumps(result, indent=2)
    snapshot.assert_match(str(json_result), "snapshot.json")


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("finding")
@pytest.mark.parametrize(
    ["email", "finding"],
    [
        ["admin@gmail.com", "3c475384-834c-47b0-ac71-a41a022e401c"],
    ],
)
async def test_get_finding_title(
    populate: bool,
    email: str,
    finding: str,
    snapshot: Any,
) -> None:
    """
    Test for GetFindingTitle
    in /front/.../navbar/breadcrumb/queries.ts
    """
    assert populate
    result: dict = await get_finding_title(user=email, finding_id=finding)
    json_result = json.dumps(result, indent=2)
    snapshot.assert_match(str(json_result), "snapshot.json")
