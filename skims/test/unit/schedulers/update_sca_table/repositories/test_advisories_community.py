import pytest
from pytest_mock import (
    MockerFixture,
)
from s3.model.types import (
    Advisory,
)
from schedulers.update_sca_table.repositories.advisories_community import (
    _format_ranges,
    fix_pip_composer_range,
    format_range,
    format_ranges,
    get_advisories_community,
    get_platform_advisories,
    PLATFORMS,
    RE_RANGES,
    URL_ADVISORIES_COMMUNITY,
)
from test.unit.schedulers.types import (
    ADVS_COMM_MOD_STR,
)
import yaml  # type: ignore


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "ranges,expected",
    [
        ("[5.0.0,6.0.0)[6.0.0,6.0.4]", ["[5.0.0,6.0.0)", "[6.0.0,6.0.4]"]),
        ("(,0.3.13]", ["(,0.3.13]"]),
        ("[1.1.4]", ["[1.1.4]"]),
        ("12345]", []),
    ],
)
def test_re_ranges_pattern(ranges: str, expected: list[str]) -> None:
    match_ranges: list[str] = RE_RANGES.findall(ranges)
    assert match_ranges == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "range_str,expected",
    [
        ("[5.0.0,6.0.0)", ">=5.0.0 <6.0.0"),
        ("(,0.3.13]", ">=0 <=0.3.13"),
        ("[1.1.4]", "=1.1.4"),
    ],
)
def test_advs_format_range(range_str: str, expected: str) -> None:
    formated_range: str = format_range(range_str)
    assert formated_range == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "range_str,expected",
    [
        (">=4.0,<4.3||>=5.0,<5.2", ">=4.0 <4.3||>=5.0 <5.2"),
        ("==3.1||>=4.0.0,<=4.0.2", "=3.1||>=4.0.0 <=4.0.2"),
        (">=1.0,<=1.0.1", ">=1.0 <=1.0.1"),
    ],
)
def test_fix_pip_composer_range(range_str: str, expected: str) -> None:
    formated_range: str = fix_pip_composer_range(range_str)
    assert formated_range == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "platform,range_str,format_func,expected",
    [
        ("pypi", ">=1.0,<=1.0.1", "fix_pip_composer_range", ">=1.0 <=1.0.1"),
        (
            "npm",
            "<5.2.4.4||>=6.0.0.0 <6.0.3.3",
            None,
            "<5.2.4.4||>=6.0.0.0 <6.0.3.3",
        ),
        ("maven", "[1.1.4]", "format_range", "=1.1.4"),
    ],
)
def test_format_ranges_internal(
    mocker: MockerFixture,
    platform: str,
    range_str: str,
    format_func: str | None,
    expected: str,
) -> None:
    format_func_mock = None
    if format_func:
        format_func_mock = mocker.patch(
            f"{ADVS_COMM_MOD_STR}.{format_func}", return_value=expected
        )
    formated_range: str = _format_ranges(platform, range_str)
    if format_func_mock:
        assert format_func_mock.call_count == 1
    assert formated_range == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "platform,range_str,internal_return,expected",
    [
        ("pypi", "1.0", "<1.0||>=2.4.1 <3.2.1", ">=0 <1.0 || >=2.4.1 <3.2.1"),
        (
            "gem",
            "<5.2.4.4||>=6.0.0.0 <6.0.3.3",
            "<5.2.4.4||>=6.0.0.0 <6.0.3.3",
            ">=0 <5.2.4.4 || >=6.0.0.0 <6.0.3.3",
        ),
        ("nuget", "[12.3.5]", "=12.3.5", "=12.3.5"),
    ],
)
def test_format_ranges(
    mocker: MockerFixture,
    platform: str,
    range_str: str,
    internal_return: str,
    expected: str,
) -> None:
    format_internal_mock = mocker.patch(
        f"{ADVS_COMM_MOD_STR}._format_ranges", return_value=internal_return
    )
    formated_range: str = format_ranges(platform, range_str, "")
    assert format_internal_mock.call_args.args == (platform, range_str)
    assert formated_range == expected


@pytest.mark.skims_test_group("unittesting")
def test_get_advisories_community(mocker: MockerFixture) -> None:
    mocker.patch("builtins.print")
    get_advs_mock = mocker.patch(
        f"{ADVS_COMM_MOD_STR}.get_platform_advisories"
    )
    get_advisories_community([], "sample-dir_name")
    assert get_advs_mock.call_count == len(PLATFORMS)


@pytest.mark.skims_test_group("unittesting")
def test_get_platform_advisories(mocker: MockerFixture) -> None:
    advisories: list[Advisory] = []
    tmp_dirname: str = "skims/test/data/sca_scheduler/test_sca_adv"
    platform: str = "npm"
    affected_range: str = ">=1.0.0 <=1.6.3"
    description = (
        "A prototype pollution vulnerability allows an attacker to cause "
        "a denial of service and may also lead to remote code execution."
    )
    expected: list[Advisory] = [
        Advisory(
            id="CVE-2021-25943",
            package_manager=platform,
            package_name="101",
            severity="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
            source=URL_ADVISORIES_COMMUNITY,
            vulnerable_version=affected_range,
            cwe_ids=["CWE-1035", "CWE-937"],
        )
    ]
    format_ranges_mock = mocker.patch(
        f"{ADVS_COMM_MOD_STR}.format_ranges",
        return_value=affected_range,
    )
    get_platform_advisories(advisories, tmp_dirname, platform)
    assert format_ranges_mock.call_args.args == (
        platform,
        affected_range,
        description,
    )
    assert advisories == expected


@pytest.mark.skims_test_group("unittesting")
def test_get_platform_advisories_error(mocker: MockerFixture) -> None:
    advisories: list[Advisory] = []
    tmp_dirname: str = "skims/test/data/sca_scheduler/test_sca_adv"
    platform: str = "npm"
    glob_mock = mocker.patch(
        f"{ADVS_COMM_MOD_STR}.yaml.safe_load",
        side_effect=yaml.YAMLError(),
    )
    print_mock = mocker.patch("builtins.print")
    get_platform_advisories(advisories, tmp_dirname, platform)
    assert glob_mock.call_count == 1
    assert isinstance(print_mock.call_args.args[0], yaml.YAMLError)
