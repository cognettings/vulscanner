from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.enums import (
    FindingVerificationStatus as FVStatus,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityVerificationStatus,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("request_vulnerabilities_verification")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        ("admin@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce8"),
        ("hacker@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce9"),
        ("reattacker@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce10"),
        ("user@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce11"),
        ("user_manager@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce12"),
        ("resourcer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce14"),
        ("reviewer@gmail.com", "be09edb7-cd5c-47ed-bee4-97c645acdce15"),
        (
            "customer_manager@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce16",
        ),
        (
            "vulnerability_manager@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce13",
        ),
    ),
)
async def test_request_verification_vuln(
    populate: bool, email: str, vuln_id: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" not in result
    assert "success" in result["data"]["requestVulnerabilitiesVerification"]
    assert result["data"]["requestVulnerabilitiesVerification"]["success"]

    loaders = get_new_context()
    finding = await loaders.finding.load(finding_id)
    assert finding
    assert finding.verification
    assert finding.verification.status == FVStatus.REQUESTED
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.verification
    assert (
        vulnerability.verification.status
        == VulnerabilityVerificationStatus.REQUESTED
    )
