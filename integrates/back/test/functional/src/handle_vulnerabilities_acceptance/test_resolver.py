# pylint: disable=import-error
from . import (
    get_result,
)
from asyncio import (
    sleep,
)
from back.test.functional.src.update_vulnerabilities_treatment import (
    put_mutation,
)
from custom_exceptions import (
    SameValues,
    VulnNotFound,
)
from dataloaders import (
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    GroupVulnerabilitiesRequest,
)
from freezegun import (
    freeze_time,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("handle_vulnerabilities_acceptance")
@pytest.mark.parametrize(
    ("email", "accepted_vulnerability_id", "rejected_vulnerability_id"),
    (
        (
            "user_manager@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
        ),
        (
            "vulnerability_manager@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdc10",
            "be09edb7-cd5c-47ed-bee4-97c645acdc11",
        ),
    ),
)
async def test_handle_vulnerabilities_acceptance(
    populate: bool,
    email: str,
    accepted_vulnerability_id: str,
    rejected_vulnerability_id: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    loaders = get_new_context()

    accepted_vuln = await loaders.vulnerability.load(accepted_vulnerability_id)
    assert accepted_vuln
    assert accepted_vuln.treatment
    rejected_vuln = await loaders.vulnerability.load(rejected_vulnerability_id)
    assert rejected_vuln
    assert rejected_vuln.treatment
    assert (
        accepted_vuln.treatment.acceptance_status
        == rejected_vuln.treatment.acceptance_status
        == VulnerabilityAcceptanceStatus.SUBMITTED
    )

    vulnerable_locations = await loaders.group_vulnerabilities.load(
        GroupVulnerabilitiesRequest(
            is_accepted=False,
            group_name="group1",
            state_status=VulnerabilityStateStatus.VULNERABLE,
            paginate=False,
        )
    )
    assert {
        accepted_vuln,
        rejected_vuln,
    } & {edge.node for edge in vulnerable_locations.edges} == set()
    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        accepted_vulnerability_id=accepted_vulnerability_id,
        rejected_vulnerability_id=rejected_vulnerability_id,
    )
    assert "errors" not in result
    assert result["data"]["handleVulnerabilitiesAcceptance"]["success"]

    loaders.vulnerability.clear_all()
    loaders.vulnerability_historic_treatment.clear(accepted_vulnerability_id)
    accepted_vuln = await loaders.vulnerability.load(accepted_vulnerability_id)
    assert accepted_vuln
    assert accepted_vuln.treatment
    rejected_vuln = await loaders.vulnerability.load(rejected_vulnerability_id)
    assert rejected_vuln
    assert rejected_vuln.treatment
    assert (
        accepted_vuln.treatment.acceptance_status
        == VulnerabilityAcceptanceStatus.APPROVED
    )
    assert rejected_vuln.treatment.acceptance_status is None

    new_vulnerable_locations = (
        await loaders.group_vulnerabilities.clear_all().load(
            GroupVulnerabilitiesRequest(
                group_name="group1",
                is_accepted=False,
                state_status=VulnerabilityStateStatus.VULNERABLE,
                paginate=False,
            )
        )
    )
    assert {accepted_vuln, rejected_vuln} & {
        edge.node for edge in new_vulnerable_locations.edges
    } == {rejected_vuln}

    with freeze_time("2021-03-31"):
        result_update_treatment = await put_mutation(
            user=email,
            finding=finding_id,
            vulnerability=rejected_vulnerability_id,
            treatment=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED.value,
            assigned=email,
            acceptance_date="",
        )
    await sleep(5)
    assert "errors" not in result_update_treatment
    assert result_update_treatment["data"]["updateVulnerabilitiesTreatment"][
        "success"
    ]

    with freeze_time("2021-03-31"):
        result_update_treatment = await put_mutation(
            user=email,
            finding=finding_id,
            vulnerability=accepted_vulnerability_id,
            treatment=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED.value,
            assigned=email,
            acceptance_date="",
        )
    assert "errors" in result_update_treatment
    assert result_update_treatment["errors"][0]["message"] == str(SameValues())


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("handle_vulnerabilities_acceptance")
@pytest.mark.parametrize(
    "email",
    (
        "user_manager@gmail.com",
        "vulnerability_manager@gmail.com",
    ),
)
async def test_handle_vulnerabilities_acceptance_fail_1(
    populate: bool,
    email: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        accepted_vulnerability_id="6f023c26-5x10-4ded-aa27-xx563c2206ax",
        rejected_vulnerability_id="",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(VulnNotFound())


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("handle_vulnerabilities_acceptance")
@pytest.mark.parametrize(
    ("email", "accepted_vulnerability_id", "rejected_vulnerability_id"),
    (
        (
            "hacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
        ),
        (
            "reattacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
        ),
        (
            "resourcer@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
        ),
        (
            "reviewer@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
        ),
        (
            "customer_manager@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
        ),
    ),
)
async def test_handle_vulnerabilities_acceptance_fail_2(
    populate: bool,
    email: str,
    accepted_vulnerability_id: str,
    rejected_vulnerability_id: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        accepted_vulnerability_id=accepted_vulnerability_id,
        rejected_vulnerability_id=rejected_vulnerability_id,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
