from . import (
    get_result,
)
import asyncio
from dataloaders import (
    get_new_context,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingCommentsRequest,
)
from db_model.findings.enums import (
    FindingStatus,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityZeroRiskStatus as VZeroRiskStatus,
)
from db_model.vulnerabilities.types import (
    GroupVulnerabilitiesRequest,
)
from decimal import (
    Decimal,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("request_vulnerabilities_zero_risk")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("admin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("user@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce11"),
        ("user_manager@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce12"),
        (
            "customer_manager@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce13",
        ),
    ),
)
async def test_request_vulnerabilities_zero_risk(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    loaders = get_new_context()
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
    assert vulnerability.zero_risk is None
    vulnerable_locations = await loaders.group_vulnerabilities.load(
        GroupVulnerabilitiesRequest(
            group_name="group1",
            state_status=VulnerabilityStateStatus.VULNERABLE,
            paginate=False,
        )
    )
    assert vulnerability in tuple(
        edge.node for edge in vulnerable_locations.edges
    )

    result: dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" not in result
    assert "success" in result["data"]["requestVulnerabilitiesZeroRisk"]
    assert result["data"]["requestVulnerabilitiesZeroRisk"]["success"]

    loaders.vulnerability.clear(vuln_id)
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
    assert vulnerability.zero_risk
    assert vulnerability.zero_risk.status == VZeroRiskStatus.REQUESTED
    zero_risk_comments = await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.ZERO_RISK, finding_id=finding_id
        )
    )
    assert zero_risk_comments[-1].finding_id == finding_id
    assert zero_risk_comments[-1].content == "request zero risk vuln"
    assert zero_risk_comments[-1].comment_type == CommentType.ZERO_RISK
    assert zero_risk_comments[-1].email == email

    new_vulnerable_locations = (
        await loaders.group_vulnerabilities.clear_all().load(
            GroupVulnerabilitiesRequest(
                group_name="group1",
                state_status=VulnerabilityStateStatus.VULNERABLE,
                paginate=False,
            )
        )
    )
    assert vulnerability not in tuple(
        edge.node for edge in new_vulnerable_locations.edges
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("request_vulnerabilities_zero_risk")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        (
            "vulnerability_manager@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce14",
        ),
    ),
)
async def test_request_zero_risk_finding_indicators(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"

    loaders = get_new_context()
    await asyncio.sleep(2)
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
    assert vulnerability.zero_risk is None

    finding_data_1 = await loaders.finding.load(finding_id)
    assert finding_data_1 is not None
    indicators = finding_data_1.unreliable_indicators
    assert indicators.unreliable_status == FindingStatus.VULNERABLE
    assert indicators.open_vulnerabilities == 1
    assert indicators.max_open_severity_score == Decimal("4.1")
    assert indicators.oldest_vulnerability_report_date
    assert indicators.newest_vulnerability_report_date
    assert indicators.treatment_summary.untreated == 1

    result: dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" not in result
    assert "success" in result["data"]["requestVulnerabilitiesZeroRisk"]
    assert result["data"]["requestVulnerabilitiesZeroRisk"]["success"]

    loaders.finding.clear(finding_id)
    await asyncio.sleep(2)
    finding_data_2 = await loaders.finding.load(finding_id)
    assert finding_data_2 is not None
    indicators = finding_data_2.unreliable_indicators
    assert indicators.unreliable_status == FindingStatus.DRAFT
    assert indicators.open_vulnerabilities == 0
    assert indicators.max_open_severity_score == Decimal("0.0")
    assert indicators.oldest_vulnerability_report_date is None
    assert indicators.newest_vulnerability_report_date is None
    assert indicators.treatment_summary.untreated == 0


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("request_vulnerabilities_zero_risk")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (("admin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),),
)
async def test_request_vulnerabilities_zero_risk_fail_1(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Zero risk vulnerability is already requested"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("request_vulnerabilities_zero_risk")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("hacker@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("reattacker@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("resourcer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("reviewer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
    ),
)
async def test_request_vulnerabilities_zero_risk_fail_2(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("request_vulnerabilities_zero_risk")
async def test_request_vulnerabilities_zero_risk_fail_cannot_request(
    populate: bool,
) -> None:
    assert populate
    email = "admin@gmail.com"
    vuln_id = "fc700327-62bd-4f69-a688-34d48c3be672"
    finding_id = "31abef8a-1aec-4199-af0c-f0792d34b5a2"
    result = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
