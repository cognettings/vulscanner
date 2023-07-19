from . import (
    run_mutation,
)
import asyncio
from dataloaders import (
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityVerificationStatus,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("close_vulnerabilities")
@pytest.mark.parametrize(
    ("email", "vulnerability_id"),
    (
        (
            "hacker@fluidattacks.com",
            "891b1d7f-a0fa-4e3d-834a-d07a9ad4b46f",
        ),
        (
            "reattacker@fluidattacks.com",
            "8e5b7694-1dca-4a1b-afbd-d7701843d97c",
        ),
    ),
)
async def test_close_vulnerabilities(
    populate: bool,
    email: str,
    vulnerability_id: str,
) -> None:
    assert populate
    finding_id = "3c475384-834c-47b0-ac71-a41a022e401c"
    loaders = get_new_context()
    vulnerability = await loaders.vulnerability.load(vulnerability_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE

    result = await run_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability_id,
    )
    assert "errors" not in result
    assert result["data"]["closeVulnerabilities"]["success"]

    loaders.vulnerability.clear(vulnerability_id)
    vulnerability = await loaders.vulnerability.load(vulnerability_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.SAFE
    assert vulnerability.state.modified_by == email


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("close_vulnerabilities")
@pytest.mark.parametrize(
    ("email", "vulnerability_id"),
    (
        (
            "hacker@fluidattacks.com",
            "891b1d7f-a0fa-4e3d-834a-d07a9ad4babc",
        ),
    ),
)
async def test_close_vulnerabilities_finding_indicators(
    populate: bool,
    email: str,
    vulnerability_id: str,
) -> None:
    assert populate
    await asyncio.sleep(2)
    finding_id = "3c475384-834c-47b0-ac71-a41a022e401c"
    loaders = get_new_context()
    vulnerability = await loaders.vulnerability.load(vulnerability_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE

    finding_data_1 = await loaders.finding.load(finding_id)
    assert finding_data_1 is not None
    indicators = finding_data_1.unreliable_indicators
    assert indicators.closed_vulnerabilities == 3

    result = await run_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability_id,
    )
    assert "errors" not in result
    assert result["data"]["closeVulnerabilities"]["success"]

    loaders.finding.clear(finding_id)
    await asyncio.sleep(2)
    finding_data_2 = await loaders.finding.load(finding_id)
    assert finding_data_2 is not None
    indicators = finding_data_2.unreliable_indicators
    assert indicators.closed_vulnerabilities == 4


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("close_vulnerabilities")
@pytest.mark.parametrize(
    ("email", "vulnerability_id"),
    (
        (
            "admin@fluidattacks.com",
            "c1df8737-1410-47ac-86f9-cd90a494c127",
        ),
    ),
)
async def test_close_vulnerabilities_verification(
    populate: bool,
    email: str,
    vulnerability_id: str,
) -> None:
    assert populate
    finding_id = "3c475384-834c-47b0-ac71-a41a022e401c"
    loaders = get_new_context()
    vulnerability = await loaders.vulnerability.load(vulnerability_id)
    assert vulnerability
    assert vulnerability.verification
    assert vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
    assert (
        vulnerability.verification.status
        == VulnerabilityVerificationStatus.REQUESTED
    )

    result = await run_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability_id,
    )
    assert "errors" not in result
    assert result["data"]["closeVulnerabilities"]["success"]

    loaders.vulnerability.clear(vulnerability_id)
    vulnerability = await loaders.vulnerability.load(vulnerability_id)
    assert vulnerability
    assert vulnerability.verification
    assert vulnerability.state.status == VulnerabilityStateStatus.SAFE
    assert (
        vulnerability.verification.status
        == VulnerabilityVerificationStatus.VERIFIED
    )
    assert vulnerability.state.modified_by == email


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("close_vulnerabilities")
@pytest.mark.parametrize(
    (
        "email",
        "vulnerability_id",
        "error_message",
    ),
    (
        (
            "admin@fluidattacks.com",
            "3d982277-a737-4046-ab7d-f3a2c4e6ecad",
            "Exception - The vulnerability has not been released",
        ),
        (
            "hacker@fluidattacks.com",
            "2ed00278-4481-4a44-8da4-04fe41751486",
            "Exception - The vulnerability has already been closed",
        ),
        (
            "reattacker@fluidattacks.com",
            "d6136f40-7609-4ac0-9741-9d9829932002",
            "Exception - The vulnerability has not been released",
        ),
    ),
)
async def test_close_vulnerabilities_non_vulnerable(
    populate: bool,
    email: str,
    vulnerability_id: str,
    error_message: str,
) -> None:
    assert populate
    finding_id = "3c475384-834c-47b0-ac71-a41a022e401c"
    result = await run_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability_id,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == error_message


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("close_vulnerabilities")
async def test_close_vulnerabilities_access_denied(populate: bool) -> None:
    assert populate
    result = await run_mutation(
        user="user@gmail.com",
        finding="3c475384-834c-47b0-ac71-a41a022e401c",
        vulnerability="d6136f40-7609-4ac0-9741-9d9829932002",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
