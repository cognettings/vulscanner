from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("resubmit_vulnerabilities")
@pytest.mark.parametrize(
    ("email", "vuln_id"),
    (
        (
            "admin@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce10",
        ),
        (
            "hacker@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce11",
        ),
        (
            "reattacker@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce12",
        ),
    ),
)
async def test_resubmit_vulnerabilities(
    populate: bool,
    email: str,
    vuln_id: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    loaders = get_new_context()
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.REJECTED

    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        vulnerability=vuln_id,
    )
    assert "errors" not in result
    assert result["data"]["resubmitVulnerabilities"]["success"]

    loaders.vulnerability.clear(vuln_id)
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.SUBMITTED
    assert vulnerability.state.modified_by == email


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("resubmit_vulnerabilities")
@pytest.mark.parametrize(
    (
        "email",
        "vuln_id",
    ),
    (
        (
            "admin@fluidattacks.com",
            "98dae7f0-0caf-4bdf-b5c5-2bc2d5d1ddc8",
        ),
        (
            "hacker@fluidattacks.com",
            "e246ed65-e0d1-4faf-ad2b-23eeded37597",
        ),
        (
            "reattacker@fluidattacks.com",
            "027ea58c-e191-4f34-bf54-9c8ffe3233b8",
        ),
    ),
)
async def test_resubmit_vulnerabilities_non_rejected(
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
    assert (
        result["errors"][0]["message"]
        == "Exception - The vulnerability has not been rejected"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("resubmit_vulnerabilities")
@pytest.mark.parametrize(
    (
        "email",
        "vuln_id",
    ),
    (
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
    ),
)
async def test_resubmit_vulnerabilities_access_denied(
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
