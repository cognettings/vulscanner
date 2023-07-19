from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.types import (
    SeverityScore,
)
from decimal import (
    Decimal,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vulnerabilities_severity")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["architect@fluidattacks.com"],
        ["hacker@fluidattacks.com"],
        ["reattacker@fluidattacks.com"],
    ],
)
async def test_update_vulnerabilities_severity(
    populate: bool, email: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    vulnerability_ids = [
        "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        "be09edb7-cd5c-47ed-bee4-97c645acdce11",
    ]
    severity_score = SeverityScore(
        base_score=Decimal("5.0"),
        temporal_score=Decimal("4.5"),
        cvss_v3="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:L/E:P/"
        "RL:O/RC:C",
        cvssf=Decimal("2"),
    )
    result: dict[str, Any] = await get_result(
        email=email,
        cvss_vector=severity_score.cvss_v3,
        finding_id=finding_id,
        vulnerability_ids=vulnerability_ids,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateVulnerabilitiesSeverity"]
    assert result["data"]["updateVulnerabilitiesSeverity"]["success"]

    loaders: Dataloaders = get_new_context()
    for vulnerability_id in vulnerability_ids:
        vulnerability = await loaders.vulnerability.load(vulnerability_id)
        assert vulnerability
        assert vulnerability.severity_score == severity_score

    finding = await loaders.finding.load(finding_id)
    assert finding
    assert (
        finding.unreliable_indicators.max_open_severity_score
        == severity_score.temporal_score
    )
    assert (
        finding.unreliable_indicators.unreliable_total_open_cvssf
        == severity_score.cvssf
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vulnerabilities_severity")
@pytest.mark.parametrize(
    ["email"],
    [
        ["customer_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
    ],
)
async def test_update_vulnerabilities_severity_fail(
    populate: bool, email: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict[str, Any] = await get_result(
        email=email,
        cvss_vector="CVSS:3.1",
        finding_id=finding_id,
        vulnerability_ids=[],
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
