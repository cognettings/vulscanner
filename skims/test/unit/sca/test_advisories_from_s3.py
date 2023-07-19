from importlib import (
    import_module,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from s3.model.types import (
    Advisory,
)
from sca import (
    format_advisories_from_s3,
    get_advisories_from_s3,
    get_remote_advisories,
)
from types import (
    ModuleType,
)

S3_ADVISORIES: list[Advisory] = [
    Advisory(
        id="CVE-ADVISORY-1",
        severity=None,
        cwe_ids=None,
        package_manager="gem",
        package_name="package_name_1",
        vulnerable_version=">=2.13.0 <2.15.0",
        source="MANUAL",
    ),
    Advisory(
        id="CVE-ADVISORY-3",
        severity=None,
        cwe_ids=None,
        package_manager="gem",
        package_name="package_name_1",
        vulnerable_version="1.1.0",
        source="MANUAL",
    ),
    Advisory(
        id="CVE-ADVISORY-2",
        severity=None,
        cwe_ids=None,
        package_manager="npm",
        package_name="package_name_2",
        vulnerable_version="<2.15.0",
        source="MANUAL",
    ),
]


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pkg_name, platform, s3_advs, s3_patch, expected",
    [
        (
            "package_name_2",
            "npm",
            S3_ADVISORIES,
            [],
            S3_ADVISORIES[2],
        ),
        ("package_name_1", "gem", {}, {}, {}),
        (
            "package_name_1",
            "gem",
            [],
            S3_ADVISORIES,
            S3_ADVISORIES[0],
        ),
        (
            "package_name_2",
            "npm",
            S3_ADVISORIES,
            None,
            S3_ADVISORIES[2],
        ),
        (
            "package_name_1",
            "gem",
            None,
            None,
            S3_ADVISORIES[0],
        ),
    ],
)
async def test_get_advisories_from_s3(  # pylint: disable=too-many-arguments
    mocker: MockerFixture,
    pkg_name: str,
    platform: str,
    s3_advs: list[Advisory] | None,
    s3_patch: list[Advisory] | None,
    expected: list[Advisory],
) -> None:
    module_test: ModuleType = import_module("sca")
    mocker.patch.object(module_test, "DATABASE", s3_advs)
    mocker.patch.object(module_test, "DATABASE_PATCH", s3_patch)

    def chose_advs_to_return(advs: list[Advisory] | None) -> list[Advisory]:
        return S3_ADVISORIES if advs is None else advs

    s3_start_mock = mocker.patch("sca.s3_start_resource")
    mocker.patch(
        "sca.download_advisories",
        return_value=(chose_advs_to_return(s3_advs)),
    )
    mocker.patch(
        "sca.download_patch_advisories",
        return_value=(chose_advs_to_return(s3_patch)),
    )
    s3_down_mock = mocker.patch("sca.s3_shutdown")
    format_advs_mock = mocker.patch(
        "sca.format_advisories_from_s3",
        return_value=expected,
    )
    result = await get_remote_advisories(pkg_name, platform)
    if s3_advs is None or s3_patch is None:
        assert s3_start_mock.await_count == 1
        assert s3_down_mock.await_count == 1
    else:
        assert s3_start_mock.await_count == 0
        assert s3_down_mock.await_count == 0
    assert format_advs_mock.call_count == 1
    assert result == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_get_advisories_from_s3_error(mocker: MockerFixture) -> None:
    s3_start_mock = mocker.patch("sca.s3_start_resource")
    mocker.patch("sca.download_advisories", side_effect=Exception())
    log_blocking_mock = mocker.patch("sca.log_blocking")
    result = await get_advisories_from_s3("test_pkg", "test_platform")
    assert s3_start_mock.await_count == 1
    assert log_blocking_mock.call_count == 1
    assert result is None


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "ads, patch_ads, expected",
    [
        (
            [S3_ADVISORIES[0]],
            [],
            [S3_ADVISORIES[0]],
        ),
        (
            [],
            [S3_ADVISORIES[0]],
            [S3_ADVISORIES[0]],
        ),
        (
            [S3_ADVISORIES[2]],
            [
                Advisory(
                    id="CVE-2021-1234",
                    severity=None,
                    cwe_ids=None,
                    package_manager="npm",
                    package_name="package_name_2",
                    vulnerable_version="1.2.3",
                    source="MANUAL",
                )
            ],
            [
                Advisory(
                    id="CVE-ADVISORY-2",
                    severity=None,
                    cwe_ids=None,
                    package_manager="npm",
                    package_name="package_name_2",
                    vulnerable_version="<2.15.0",
                    source="MANUAL",
                ),
                Advisory(
                    id="CVE-2021-1234",
                    severity=None,
                    cwe_ids=None,
                    package_manager="npm",
                    package_name="package_name_2",
                    vulnerable_version="1.2.3",
                    source="MANUAL",
                ),
            ],
        ),
        ([], [], []),
    ],
)
def test_format_advisories_from_s3(
    ads: list[Advisory],
    patch_ads: list[Advisory],
    expected: list[Advisory],
) -> None:
    result = format_advisories_from_s3(ads, patch_ads)
    assert result == expected
