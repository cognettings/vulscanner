from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
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
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reject_vulnerabilities_zero_risk")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("admin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("reviewer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce11"),
    ),
)
async def test_reject_vulnerabilities_zero_risk(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    loaders = get_new_context()
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
    assert vulnerability.zero_risk
    assert vulnerability.zero_risk.status == VZeroRiskStatus.REQUESTED
    vulnerable_locations = await loaders.group_vulnerabilities.load(
        GroupVulnerabilitiesRequest(
            group_name="group1",
            state_status=VulnerabilityStateStatus.VULNERABLE,
            paginate=False,
        )
    )
    assert vulnerability not in tuple(
        edge.node for edge in vulnerable_locations.edges
    )

    result: dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" not in result
    assert "success" in result["data"]["rejectVulnerabilitiesZeroRisk"]
    assert result["data"]["rejectVulnerabilitiesZeroRisk"]["success"]

    loaders.vulnerability.clear(vuln_id)
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
    assert vulnerability.zero_risk
    assert vulnerability.zero_risk.status == VZeroRiskStatus.REJECTED
    zero_risk_comments = await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.ZERO_RISK, finding_id=finding_id
        )
    )
    assert zero_risk_comments[-1].finding_id == finding_id
    assert zero_risk_comments[-1].content == "reject zero risk vuln"
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
    assert vulnerability in tuple(
        edge.node for edge in new_vulnerable_locations.edges
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reject_vulnerabilities_zero_risk")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (("admin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce12"),),
)
async def test_reject_zero_risk_finding_indicators(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    loaders = get_new_context()

    finding = await loaders.finding.load(finding_id)
    assert finding
    assert (
        finding.unreliable_indicators.unreliable_status
        == FindingStatus.VULNERABLE
    )
    assert (
        finding.unreliable_indicators.oldest_vulnerability_report_date
        == datetime.fromisoformat("2018-04-08T00:45:11+00:00")
    )
    assert (
        finding.unreliable_indicators.newest_vulnerability_report_date
        == datetime.fromisoformat("2018-04-08T00:45:11+00:00")
    )

    result: dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" not in result
    assert "success" in result["data"]["rejectVulnerabilitiesZeroRisk"]
    assert result["data"]["rejectVulnerabilitiesZeroRisk"]["success"]

    loaders.finding.clear(finding_id)
    finding = await loaders.finding.load(finding_id)
    assert finding
    assert (
        finding.unreliable_indicators.unreliable_status
        == FindingStatus.VULNERABLE
    )
    assert (
        finding.unreliable_indicators.oldest_vulnerability_report_date
        == datetime.fromisoformat("2018-04-05T00:45:11+00:00")
    )
    assert (
        finding.unreliable_indicators.newest_vulnerability_report_date
        == datetime.fromisoformat("2018-04-08T00:45:11+00:00")
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reject_vulnerabilities_zero_risk")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("admin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce14"),
        ("reviewer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce14"),
    ),
)
async def test_reject_vulnerabilities_zero_risk_fail(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    loaders = get_new_context()
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.zero_risk is None

    result: dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Zero risk vulnerability is not requested"
    )
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


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reject_vulnerabilities_zero_risk")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("hacker@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("reattacker@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("user@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("user_manager@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        (
            "vulnerability_manager@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        (
            "customer_manager@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        ("resourcer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
    ),
)
async def test_access_denied_fail(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
