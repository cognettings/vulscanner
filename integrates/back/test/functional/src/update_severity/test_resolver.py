from . import (
    get_finding_severity,
    get_result,
    get_result2,
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
@pytest.mark.resolver_test_group("update_severity")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["hacker@fluidattacks.com"],
    ],
)
async def test_update_severity(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e402c"
    result: dict[str, Any] = await get_result(
        email=email, finding_id=finding_id
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateSeverity"]
    assert result["data"]["updateSeverity"]["success"]

    expected_severity = {
        "attackComplexity": 0.77,
        "attackVector": 0.62,
        "availabilityImpact": 0,
        "availabilityRequirement": 1,
        "confidentialityImpact": 0,
        "confidentialityRequirement": 1,
        "exploitability": 0.91,
        "integrityImpact": 0.22,
        "integrityRequirement": 1,
        "modifiedAttackComplexity": 0.77,
        "modifiedAttackVector": 0.62,
        "modifiedAvailabilityImpact": 0,
        "modifiedConfidentialityImpact": 0,
        "modifiedIntegrityImpact": 0.22,
        "modifiedPrivilegesRequired": 0.62,
        "modifiedSeverityScope": 0,
        "modifiedUserInteraction": 0.85,
        "privilegesRequired": 0.62,
        "remediationLevel": 0.97,
        "reportConfidence": 0.92,
        "severityScope": 0,
        "userInteraction": 0.85,
    }
    result = await get_finding_severity(email=email, finding_id=finding_id)
    assert result["data"]["finding"]["severity"] == expected_severity

    loaders: Dataloaders = get_new_context()
    finding = await loaders.finding.load(finding_id)
    assert finding
    assert finding.severity_score
    assert finding.severity_score == SeverityScore(
        base_score=Decimal("3.5"),
        temporal_score=Decimal("2.9"),
        cvss_v3="CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/"
        "E:U/RL:W/RC:U/MAV:A/MAC:L/MPR:L/MUI:N/MS:U/MI:L",
        cvssf=Decimal("0.218"),
    )
    assert (
        finding.unreliable_indicators.unreliable_max_open_severity_score
        == Decimal("0.0")  # No open vulns
    )
    assert finding.unreliable_indicators.max_open_severity_score == Decimal(
        "0.0"
    )  # No open vulns
    assert (
        finding.unreliable_indicators.unreliable_total_open_cvssf
        == Decimal("0.0")  # No open vulns
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_severity")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["hacker@fluidattacks.com"],
    ],
)
async def test_update_severity_from_cvss_vector(
    populate: bool, email: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e402c"
    cvss_vector = (
        "CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/"
        "RL:W/RC:U/CR:M/IR:H/AR:L/MAV:A/MAC:L/MPR:L/MUI:N/MS:U/MI:L"
    )
    result: dict[str, Any] = await get_result2(
        email=email, finding_id=finding_id, cvss_vector=cvss_vector
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateSeverity"]
    assert result["data"]["updateSeverity"]["success"]

    expected_severity = {
        "attackComplexity": 0.77,
        "attackVector": 0.62,
        "availabilityImpact": 0.0,
        "availabilityRequirement": 0.5,
        "confidentialityImpact": 0.0,
        "confidentialityRequirement": 1.0,
        "exploitability": 0.91,
        "integrityImpact": 0.22,
        "integrityRequirement": 1.5,
        "modifiedAttackComplexity": 0.77,
        "modifiedAttackVector": 0.62,
        "modifiedAvailabilityImpact": 0.0,
        "modifiedConfidentialityImpact": 0.0,
        "modifiedIntegrityImpact": 0.22,
        "modifiedPrivilegesRequired": 0.62,
        "modifiedSeverityScope": 0.0,
        "modifiedUserInteraction": 0.85,
        "privilegesRequired": 0.62,
        "remediationLevel": 0.97,
        "reportConfidence": 0.92,
        "severityScope": 0.0,
        "userInteraction": 0.85,
    }
    result = await get_finding_severity(email=email, finding_id=finding_id)
    assert result["data"]["finding"]["severity"] == expected_severity

    loaders: Dataloaders = get_new_context()
    finding = await loaders.finding.load(finding_id)
    assert finding
    assert finding.severity_score
    assert finding.severity_score == SeverityScore(
        base_score=Decimal("3.5"),
        temporal_score=Decimal("2.9"),
        cvss_v3=cvss_vector,
        cvssf=Decimal("0.218"),
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_severity")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
    ],
)
async def test_update_severity_fail(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e402c"
    result: dict[str, Any] = await get_result(
        email=email, finding_id=finding_id
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
