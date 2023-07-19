from . import (
    get_result,
)
from custom_utils.filter_vulnerabilities import (
    filter_non_deleted,
    filter_non_zero_risk,
    filter_released_vulns,
)
from custom_utils.vulnerabilities import (
    is_reattack_on_hold,
)
from dataloaders import (
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    FindingVulnerabilitiesZrRequest,
    Vulnerability,
)
import pytest
from vulnerabilities.domain.core import (
    get_vulnerability,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("deactivate_root")
@pytest.mark.parametrize(
    ("group_name", "root_id"),
    (
        (
            "group1",
            "63298a73-9dff-46cf-b42d-9b2f01a56690",
        ),
        (
            "group2",
            "83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
        ),
        (
            "group2",
            "eee8b331-98b9-4e32-a3c7-ec22bd244ae8",
        ),
    ),
)
@pytest.mark.parametrize(
    ("reason", "other"),
    (
        ("OTHER", "custom reason"),
        ("OUT_OF_SCOPE", None),
        ("REGISTERED_BY_MISTAKE", None),
    ),
)
async def test_deactivate_root(
    populate: bool,
    group_name: str,
    root_id: str,
    reason: str,
    other: str | None,
) -> None:
    assert populate
    loaders = get_new_context()
    request_vulnerability_id, on_hold_event_id = next(
        (
            (vulnerability.id, vulnerability.event_id)
            for vulnerability in filter_released_vulns(
                filter_non_zero_risk(
                    filter_non_deleted(
                        await loaders.root_vulnerabilities.load(root_id)
                    )
                )
            )
            if is_reattack_on_hold(vulnerability) and vulnerability.event_id
        ),
        (None, None),
    )
    if request_vulnerability_id and on_hold_event_id:
        vulnerability: Vulnerability = await get_vulnerability(
            loaders=get_new_context(),
            vulnerability_id=request_vulnerability_id,
        )
        safe_connection = (
            await loaders.finding_vulnerabilities_released_nzr_c.load(
                FindingVulnerabilitiesZrRequest(
                    finding_id=vulnerability.finding_id,
                    paginate=False,
                    state_status=VulnerabilityStateStatus.SAFE,
                )
            )
        )
        vulnerable_connection = (
            await loaders.finding_vulnerabilities_released_nzr_c.load(
                FindingVulnerabilitiesZrRequest(
                    finding_id=vulnerability.finding_id,
                    paginate=False,
                    state_status=VulnerabilityStateStatus.VULNERABLE,
                )
            )
        )
        assert len([edge.node for edge in vulnerable_connection.edges]) == 3
        assert len([edge.node for edge in safe_connection.edges]) == 1
        assert (
            len(
                await loaders.event_vulnerabilities_loader.load(
                    on_hold_event_id.split("#")[1]
                )
            )
            == 1
        )
        assert (
            vulnerability.state.status is VulnerabilityStateStatus.VULNERABLE
        )

    result = await get_result(
        email="admin@gmail.com",
        group_name=group_name,
        identifier=root_id,
        reason=reason,
        other=other,
    )
    assert "errors" not in result
    assert result["data"]["deactivateRoot"]["success"]

    if request_vulnerability_id and on_hold_event_id:
        vulnerability = await get_vulnerability(
            loaders=get_new_context(),
            vulnerability_id=request_vulnerability_id,
        )
        assert bool(
            vulnerability.verification
            and vulnerability.verification.status
            == VulnerabilityVerificationStatus.VERIFIED
        )
        assert vulnerability.state.status is VulnerabilityStateStatus.SAFE
        loaders.event_vulnerabilities_loader.clear_all()
        loaders.finding_vulnerabilities_released_nzr_c.clear_all()
        safe_connection = (
            await loaders.finding_vulnerabilities_released_nzr_c.load(
                FindingVulnerabilitiesZrRequest(
                    finding_id=vulnerability.finding_id,
                    paginate=False,
                    state_status=VulnerabilityStateStatus.SAFE,
                )
            )
        )
        vulnerable_connection = (
            await loaders.finding_vulnerabilities_released_nzr_c.load(
                FindingVulnerabilitiesZrRequest(
                    finding_id=vulnerability.finding_id,
                    paginate=False,
                    state_status=VulnerabilityStateStatus.VULNERABLE,
                )
            )
        )
        assert len([edge.node for edge in vulnerable_connection.edges]) == 1
        assert len([edge.node for edge in safe_connection.edges]) == 3
        assert (
            len(
                await loaders.event_vulnerabilities_loader.load(
                    on_hold_event_id.split("#")[1]
                )
            )
            == 0
        )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("deactivate_root")
@pytest.mark.parametrize(
    ("group_name", "root_id"),
    (
        (
            "group2",
            "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
        ),
    ),
)
async def test_deactivate_root_fail_1(
    populate: bool,
    group_name: str,
    root_id: str,
) -> None:
    assert populate
    result = await get_result(
        email="admin@gmail.com",
        group_name=group_name,
        identifier=root_id,
        reason="REGISTERED_BY_MISTAKE",
        other=None,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Access denied or root not found"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("deactivate_root")
@pytest.mark.parametrize(
    ("group_name", "root_id"),
    (
        (
            "group2",
            "702b81b3-d741-4699-9173-ecbc30bfb0cb",
        ),
        (
            "group1",
            "44db9bee-c97d-4161-98c6-f124d7dc9a41",
        ),
        (
            "group1",
            "bd4e5e66-da26-4274-87ed-17de7c3bc2f1",
        ),
    ),
)
async def test_deactivate_root_fail_2(
    populate: bool,
    group_name: str,
    root_id: str,
) -> None:
    assert populate
    result = await get_result(
        email="admin@gmail.com",
        group_name=group_name,
        identifier=root_id,
        reason="REGISTERED_BY_MISTAKE",
        other=None,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
