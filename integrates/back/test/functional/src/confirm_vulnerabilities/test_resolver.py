from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.enums import (
    FindingStatus,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from decimal import (
    Decimal,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("confirm_vulnerabilities")
@pytest.mark.parametrize(
    ("email"),
    (("admin@gmail.com"),),
)
async def test_confirm_vulnerabilities_first(
    populate: bool,
    email: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    vuln_id: str = "be09edb7-cd5c-47ed-bee4-97c645acdce10"
    loaders = get_new_context()
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.SUBMITTED

    finding_data_1 = await loaders.finding.load(finding_id)
    assert finding_data_1 is not None
    indicators = finding_data_1.unreliable_indicators
    assert indicators.unreliable_status == FindingStatus.DRAFT
    assert indicators.open_vulnerabilities == 0
    assert indicators.max_open_severity_score == Decimal("0.0")
    assert indicators.oldest_vulnerability_report_date is None
    assert indicators.newest_vulnerability_report_date is None
    assert indicators.treatment_summary.untreated == 0
    assert indicators.treatment_summary.in_progress == 0
    assert indicators.treatment_summary.accepted == 0
    assert indicators.treatment_summary.accepted_undefined == 0

    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        vulnerability=vuln_id,
    )
    assert "errors" not in result
    assert result["data"]["confirmVulnerabilities"]["success"]

    loaders.finding.clear(finding_id)
    finding_data_2 = await loaders.finding.load(finding_id)
    assert finding_data_2 is not None
    indicators = finding_data_2.unreliable_indicators
    assert indicators.unreliable_status == FindingStatus.VULNERABLE
    assert indicators.open_vulnerabilities == 1
    assert indicators.max_open_severity_score == Decimal("4.1")
    assert indicators.oldest_vulnerability_report_date
    assert indicators.newest_vulnerability_report_date
    assert indicators.treatment_summary.untreated == 1
    assert indicators.treatment_summary.in_progress == 0
    assert indicators.treatment_summary.accepted == 0
    assert indicators.treatment_summary.accepted_undefined == 0

    loaders.vulnerability.clear(vuln_id)
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
    assert vulnerability.state.modified_by == email


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("confirm_vulnerabilities")
@pytest.mark.parametrize(
    ("email"),
    (("admin@gmail.com"),),
)
async def test_confirm_vulnerabilities_second(
    populate: bool,
    email: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    vuln_id: str = "be09edb7-cd5c-47ed-bee4-97c645acdce11"
    loaders = get_new_context()
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.SUBMITTED

    finding_data_1 = await loaders.finding.load(finding_id)
    assert finding_data_1 is not None
    indicators = finding_data_1.unreliable_indicators
    assert indicators.unreliable_status == FindingStatus.VULNERABLE
    assert indicators.open_vulnerabilities == 1
    assert indicators.max_open_severity_score == Decimal("4.1")

    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        vulnerability=vuln_id,
    )
    assert "errors" not in result
    assert result["data"]["confirmVulnerabilities"]["success"]

    loaders.finding.clear(finding_id)
    finding_data_2 = await loaders.finding.load(finding_id)
    assert finding_data_2 is not None
    indicators = finding_data_2.unreliable_indicators
    assert indicators.unreliable_status == FindingStatus.VULNERABLE
    assert indicators.open_vulnerabilities == 2
    assert indicators.max_open_severity_score == Decimal("4.8")

    loaders.vulnerability.clear(vuln_id)
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
    assert vulnerability.state.modified_by == email


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("confirm_vulnerabilities")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        (
            "hacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        (
            "reattacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        (
            "user@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        (
            "user_manager@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        (
            "vulnerability_manager@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        (
            "customer_manager@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        (
            "resourcer@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
    ),
)
async def test_confirm_vulnerabilities_fail(
    populate: bool,
    email: str,
    vuln_id: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        vulnerability=vuln_id,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
