import pytest
from pytest_mock import (
    MockerFixture,
)
from semantic_version import (
    base,
    NpmSpec,
    Version,
)
from semver_match_tools.semver_match import (
    check_extremes_intersection,
    check_multiple_ranges,
    check_ranges_intersection,
    coerce,
    coerce_range,
    get_min_and_max_ver,
    semver_match,
)
from unittest.mock import (
    Mock,
)

STR_MDL_SEMVER_MATCH: str = "semver_match_tools.semver_match"


@pytest.fixture(name="mock_coerce_range")
def fixture_coerce_range(mocker: MockerFixture) -> Mock:
    return mocker.patch(
        f"{STR_MDL_SEMVER_MATCH}.coerce_range",
        side_effect=lambda version: version,
    )


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "min_spec, max_spec, expected",
    [
        (
            base.Range(">=", Version("1.0.0")),
            base.Range("<", Version("2.0.0")),
            True,
        ),
        (
            base.Range(">", Version("1.0.0")),
            base.Range("=<", Version("1.0.0")),
            False,
        ),
        (
            base.Range(">=", Version("1.0.0")),
            base.Range("<=", Version("1.0.0")),
            True,
        ),
        (
            base.Range(">=", Version("1.0.0")),
            None,
            True,
        ),
        (
            base.Range(">", Version("1.0.0")),
            base.Range("<", Version("0.5.0")),
            False,
        ),
    ],
)
def test_check_extremes_intersection(
    min_spec: base.Range,
    max_spec: base.Range | None,
    expected: bool,
) -> None:
    result = check_extremes_intersection(min_spec, max_spec)
    assert result == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "clause_range, expected_min, expected_max",
    [
        (
            NpmSpec(">=1.0.0 <=1.6.3").clause,
            base.Range(">=", Version("1.0.0")),
            base.Range("<=", Version("1.6.3")),
        ),
        (
            NpmSpec("1.0.*").clause,
            base.Range(">=", Version("1.0.0")),
            base.Range("<", Version("1.1.0")),
        ),
        (
            NpmSpec(">1.6.3").clause,
            base.Range(">", Version("1.6.3")),
            None,
        ),
        (
            NpmSpec("~2.0.0").clause,
            base.Range(">=", Version("2.0.0")),
            base.Range("<", Version("2.1.0")),
        ),
        (
            NpmSpec("^1.0.0").clause,
            base.Range(">=", Version("1.0.0")),
            base.Range("<", Version("2.0.0")),
        ),
    ],
)
def test_get_min_and_max_ver(
    clause_range: base.AllOf,
    expected_min: base.Range,
    expected_max: base.Range | None,
) -> None:
    min_ver, max_ver = get_min_and_max_ver(clause_range)
    assert min_ver.operator == expected_min.operator
    assert min_ver.target == expected_min.target
    if expected_max and max_ver:
        assert max_ver.operator == expected_max.operator
        assert max_ver.target == expected_max.target


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "ver_clause, extremes_ver, const_clause, extremes_const, check_resp",
    [
        (
            NpmSpec(">=1.0.0 <=1.6.3").clause,
            (
                base.Range(">=", Version("1.0.0")),
                base.Range("<=", Version("1.6.3")),
            ),
            NpmSpec("1.0.*").clause,
            (
                base.Range(">=", Version("1.0.0")),
                base.Range("<", Version("1.1.0")),
            ),
            True,
        ),
        (
            NpmSpec(">1.6.3").clause,
            (base.Range(">", Version("1.6.3")), None),
            NpmSpec(">1.0.0").clause,
            (base.Range(">", Version("1.0.0")), None),
            True,
        ),
        (
            NpmSpec("~2.0.0").clause,
            (
                base.Range(">=", Version("2.0.0")),
                base.Range("<", Version("2.1.0")),
            ),
            NpmSpec("^1.0.0").clause,
            (
                base.Range(">=", Version("1.0.0")),
                base.Range("<", Version("2.0.0")),
            ),
            False,
        ),
    ],
)
def test_check_ranges_intersection(  # pylint: disable=too-many-arguments
    mocker: MockerFixture,
    ver_clause: base.AllOf,
    extremes_ver: tuple[base.Range, base.Range | None],
    const_clause: base.AllOf,
    extremes_const: tuple[base.Range, base.Range | None],
    check_resp: bool,
) -> None:
    mock_get_min_and_max_ver = mocker.patch(
        f"{STR_MDL_SEMVER_MATCH}.get_min_and_max_ver",
        side_effect=[extremes_ver, extremes_const],
    )
    mock_extremes_intersection = mocker.patch(
        f"{STR_MDL_SEMVER_MATCH}.check_extremes_intersection",
        return_value=check_resp,
    )
    result = check_ranges_intersection(ver_clause, const_clause)
    assert mock_get_min_and_max_ver.call_count == 2
    assert result == mock_extremes_intersection.return_value


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "constraint, expected",
    [
        ("v1.2.3", "1.2.3"),
        ("=1.2.3.4", "=1.2.3"),
        ("1.2", "1.2.0"),
        (">1.2", ">1.2.0"),
        ("<11.22.33-alpha+beta", "<11.22.33-alpha+beta"),
        ("~2", "~2.*.*"),
    ],
)
def test_coerce(constraint: str, expected: str) -> None:
    assert coerce(constraint) == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "range_str, expected",
    [
        (
            ">=1.0.0  ||  <2.0.0||   >=3.0.0-alpha.1   <4.0.0",
            ">=1.0.0||>=0.0.0 <2.0.0||>=3.0.0-alpha.1 <4.0.0",
        ),
        (">=1.0.0   <2.0.0", ">=1.0.0 <2.0.0"),
    ],
)
def test_coerce_range(
    mocker: MockerFixture, range_str: str, expected: str
) -> None:
    mocker.patch(
        f"{STR_MDL_SEMVER_MATCH}.coerce", side_effect=lambda token: token
    )
    assert coerce_range(range_str) == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "version_str, range_str, intersection_response",
    [
        ("~1.0.0", ">=1.0.0 <2.0.0", [True]),
        (
            "~5.0.0||^6.0.0",
            ">=0.0.0 <0.5.0||>2.0.0 <2.5.0",
            [False, False, False, False],
        ),
        ("4.0.*", ">=5.0.0 <5.5.0||>6.0.0 <8.5.0", [False, False]),
        (
            ">=2.0.6 <3.0.0||=3.0.6",
            "1.0.*||>2.0.0 <=2.0.5||^3.0.4",
            [False, False, False, False, False, True],
        ),
    ],
)
def test_check_multiple_ranges(
    mocker: MockerFixture,
    version_str: str,
    range_str: str,
    intersection_response: list[bool],
) -> None:
    version = NpmSpec(version_str).clause
    range_specs = NpmSpec(range_str).clause
    mock_ranges_intersection = mocker.patch(
        f"{STR_MDL_SEMVER_MATCH}.check_ranges_intersection",
        side_effect=intersection_response,
    )
    result = check_multiple_ranges(version, range_specs)
    expected = True in intersection_response
    assert mock_ranges_intersection.call_count == len(intersection_response)
    assert result == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "dep_version, vulnerable_version",
    [
        ("=2.0.0a", ">2.0.0 <2.5.0"),
        ("3.0.0-a", ">2.0.0 <2.5.0&&>2.7.0 <=2.8.0"),
    ],
)
def test_semver_match_error(
    mocker: MockerFixture,
    mock_coerce_range: Mock,
    dep_version: str,
    vulnerable_version: str,
) -> None:
    mock_log_blocking = mocker.patch(f"{STR_MDL_SEMVER_MATCH}.log_blocking")
    result = semver_match(dep_version, vulnerable_version)
    assert result is False
    assert mock_coerce_range.call_count == 2
    assert mock_log_blocking.call_args.args == (
        "error",
        "Semver match %s to %s: Invalid semver version",
        dep_version,
        vulnerable_version,
    )


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "version, is_single_version, expected",
    [
        ("=2.0.0", True, False),
        ("~3.0.0", False, False),
        ("2.4.0", True, True),
        ("^2.1.0", False, True),
    ],
)
def test_semver_match(
    mocker: MockerFixture,
    mock_coerce_range: Mock,
    version: str,
    is_single_version: bool,
    expected: bool,
) -> None:
    constraint = ">2.0.0 <2.5.0"
    mock_check_multiple_ranges = mocker.patch(
        f"{STR_MDL_SEMVER_MATCH}.check_multiple_ranges", return_value=expected
    )
    result = semver_match(version, constraint)
    assert mock_coerce_range.call_args_list == [
        ((version,),),
        ((constraint,),),
    ]
    if not is_single_version:
        assert mock_check_multiple_ranges.called
    assert result == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "dep_ver, vuln_ver, expected",
    [
        ("^1.0.0", "<0.0", False),
        ("^7.0.0", "=6.12.2", False),
        ("^7.0.0", "=6.12.2 || =6.9.1", False),
        ("~2.2.3", ">=3.0.0 <=4.0.0", False),
        ("=2.2", ">=2.3.0 <=2.4.0", False),
        ("~0.8.0", ">=0 <=1.8.6", True),
        ("1.8.0", ">=0 <=0.3.0 || >=1.0.1 <=1.8.6", True),
        ("^2.1.0", ">=0 <11.0.5 || >=11.1.0 <11.1.0", True),
        ("2.1.0", "~2", True),
    ],
)
def test_semver_match_full(
    dep_ver: str,
    vuln_ver: str,
    expected: bool,
) -> None:
    result = semver_match(dep_ver, vuln_ver)
    assert result == expected
