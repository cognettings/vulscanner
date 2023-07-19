from importlib import (
    import_module,
)
from model import (
    core,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from s3.model.types import (
    Advisory,
)
from sca import (
    get_remote_advisories,
    get_vulnerabilities,
)
from types import (
    ModuleType,
)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "source, return_value",
    [
        (
            "s3",
            {
                "CVE-2023-22491": {
                    "vulnerable_version": "<0",
                    "cvss": None,
                    "cwe_ids": None,
                },
                "CVE-2022-25863": {
                    "vulnerable_version": "<2.14.1 || >=3.0.0 <3.15.2",
                    "cvss": None,
                    "cwe_ids": None,
                },
            },
        ),
        ("s3", None),
    ],
)
async def test_get_remote_advisories(
    mocker: MockerFixture,
    source: str | None,
    return_value: list[Advisory] | None,
) -> None:
    module_test: ModuleType = import_module("sca")
    db_info = None if source == "dynamodb" else "mock_info"
    mocker.patch.object(module_test, "DATABASE", db_info)
    get_advs_mock = mocker.patch(
        f"sca.get_advisories_from_{source}",
        return_value=None if return_value == [] else return_value,
    )
    pkg_name: str = "test_pkg"
    platfom: str = "test_platform"
    result = await get_remote_advisories(pkg_name, platfom)
    assert get_advs_mock.await_count == 1
    assert get_advs_mock.call_args.args == (pkg_name, platfom)
    assert result == return_value


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "advisories, expected_output",
    [
        (
            [
                Advisory(
                    id="CVE-2021-1234",
                    severity=None,
                    cwe_ids=None,
                    package_manager="maven",
                    package_name="package",
                    vulnerable_version="invalid",
                    source="MANUAL",
                ),
                Advisory(
                    id="CVE-2021-5678",
                    severity=None,
                    cwe_ids=None,
                    package_manager="maven",
                    package_name="package",
                    vulnerable_version="^1.2.0",
                    source="MANUAL",
                ),
            ],
            [
                Advisory(
                    id="CVE-2021-5678",
                    severity=None,
                    cwe_ids=None,
                    package_manager="maven",
                    package_name="package",
                    vulnerable_version="^1.2.0",
                    source="MANUAL",
                )
            ],
        ),
        (
            [
                Advisory(
                    id="CVE-2021-1234",
                    severity=None,
                    cwe_ids=None,
                    package_manager="maven",
                    package_name="package",
                    vulnerable_version="invalid",
                    source="MANUAL",
                ),
                Advisory(
                    id="CVE-2018-5689",
                    severity=None,
                    cwe_ids=None,
                    package_manager="maven",
                    package_name="package",
                    vulnerable_version="=1.0.0",
                    source="MANUAL",
                ),
                Advisory(
                    id="CVE-2021-3456",
                    severity=None,
                    cwe_ids=None,
                    package_manager="maven",
                    package_name="package",
                    vulnerable_version="^1.2.0",
                    source="MANUAL",
                ),
            ],
            [
                Advisory(
                    id="CVE-2018-5689",
                    severity=None,
                    cwe_ids=None,
                    package_manager="maven",
                    package_name="package",
                    vulnerable_version="=1.0.0",
                    source="MANUAL",
                ),
                Advisory(
                    id="CVE-2021-3456",
                    severity=None,
                    cwe_ids=None,
                    package_manager="maven",
                    package_name="package",
                    vulnerable_version="^1.2.0",
                    source="MANUAL",
                ),
            ],
        ),
    ],
)
async def test_get_vulnerabilities(
    mocker: MockerFixture,
    advisories: list[Advisory],
    expected_output: list[Advisory],
) -> None:
    platform = core.Platform.NPM
    product = "my_product"
    version = "1.2.3"
    get_remote_mock = mocker.patch(
        "sca.get_remote_advisories", return_value=advisories
    )
    semver_match_mock = mocker.patch(
        "sca.semver_match",
        side_effect=lambda _, constraints: constraints != "invalid",
    )
    result = await get_vulnerabilities(platform, product, version)
    assert get_remote_mock.call_args.args == (product, platform.value.lower())
    assert semver_match_mock.call_count == len(advisories)
    assert result == expected_output
