from decimal import (
    Decimal,
)
from forces.apis.integrates.api import (
    get_findings,
    get_groups_access,
    get_vulnerabilities,
    get_vulnerabilities_fallback,
)
from forces.apis.integrates.client import (
    ApiError,
)
from forces.model import (
    ForcesConfig,
    KindEnum,
)
import pytest


@pytest.mark.asyncio
async def test_get_findings(
    test_group: str,
    test_token: str,
    test_finding: str,
) -> None:
    result = await get_findings(test_group, api_token=test_token)
    assert test_finding in result[1]["id"]
    assert (
        len(
            tuple(
                finding
                for finding in result
                if str(finding["status"]).upper() == "DRAFT"
            )
        )
        == 0
    )
    assert (
        len(
            tuple(
                finding
                for finding in result
                if str(finding["status"]).upper() != "DRAFT"
            )
        )
        == 7
    )


@pytest.mark.asyncio
async def test_get_vulnerabilities(
    test_token: str, test_config: ForcesConfig
) -> None:
    result = await get_vulnerabilities(test_config, api_token=test_token)
    assert len(result) == 26
    assert "192.168.100.105" in result[0]["where"]


@pytest.mark.asyncio
async def test_get_vulnerabilities_fallback(
    test_token: str, test_config: ForcesConfig
) -> None:
    result = await get_vulnerabilities_fallback(
        test_config, api_token=test_token
    )
    assert len(result) == 29
    assert "192.168.100.113" in result[0]["where"]


@pytest.mark.asyncio
async def test_compare_vulnerability_fetchers(
    test_token: str, test_config: ForcesConfig
) -> None:
    current_result = await get_vulnerabilities_fallback(
        test_config, api_token=test_token
    )
    preview_result = await get_vulnerabilities(
        test_config, api_token=test_token
    )
    assert (
        len(
            tuple(
                filter(
                    lambda vuln: vuln["state"] != "ACCEPTED", current_result
                )
            )
        )
        == len(preview_result)
        == 26
    )


@pytest.mark.asyncio
async def test_vulnerabilities_api_filter_static(test_token: str) -> None:
    test_config = ForcesConfig(
        organization="okada",
        group="unittesting",
        kind=KindEnum.STATIC,
    )
    result = await get_vulnerabilities_fallback(
        test_config, api_token=test_token
    )
    for vuln in result:
        assert vuln["vulnerabilityType"] == "lines"


@pytest.mark.asyncio
@pytest.mark.skip(
    reason="""
    The severity filter is not linked to the new severityTemporalScore value
    """
)
async def test_vulnerabilities_api_filter_severity(test_token: str) -> None:
    test_config = ForcesConfig(
        organization="okada",
        group="unittesting",
        breaking_severity=Decimal("3.2"),
        verbose_level=1,
    )
    result = await get_vulnerabilities_fallback(
        test_config, api_token=test_token
    )
    for vuln in result:
        if vuln["severityTemporalScore"] is not None:
            assert vuln["severityTemporalScore"] >= 3.0


@pytest.mark.asyncio
async def test_vulnerabilities_api_filter_open(test_token: str) -> None:
    test_config = ForcesConfig(
        organization="okada",
        group="unittesting",
        verbose_level=2,
    )
    result = await get_vulnerabilities_fallback(
        test_config, api_token=test_token
    )
    for vuln in result:
        assert vuln["state"] in ["VULNERABLE", "ACCEPTED"]  # ZRs & Treatments


@pytest.mark.asyncio
async def test_get_group_access() -> None:
    try:
        await get_groups_access(api_token="bad_token")
    except ApiError as exc:
        assert (
            "Login required" in exc.messages
            or "Token format unrecognized" in exc.messages
        )
