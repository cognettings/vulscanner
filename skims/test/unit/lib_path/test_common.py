from lib.sca.common import (
    DependencyType,
    format_pkg_dep,
    get_conan_dep_info,
)
import pytest


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "dep_info, expected",
    [
        ("nlohmann_json/3.10.5", ("nlohmann_json", "3.10.5")),
        ("poco/[>1.0,<1.9]", ("poco", ">1.0 <1.9")),
        ("pkg/[>1.0 <1.8]@user/stable", ("pkg", ">1.0 <1.8")),
        (
            "pkg2/[~3.1.5, loose=False, include_prerelease=True]",
            ("pkg2", "~3.1.5"),
        ),
        ("openssl/1.1.1o", ("openssl", "1.1.1o")),
        ('"pkg4/[>1 <2.0 || ^3.2]"', ("pkg4", ">1 <2.0 || ^3.2")),
    ],
)
def test_get_conan_dep_info(dep_info: str, expected: tuple[str, str]) -> None:
    assert get_conan_dep_info(dep_info) == expected


@pytest.mark.skims_test_group("unittesting")
def test_format_pkg_dep() -> None:
    pkg_name = "pkg1"
    version = "1.0.0"
    product_line = 14
    version_line = 15
    column = 8
    expected_output: DependencyType = (
        {"column": column, "line": product_line, "item": pkg_name},
        {"column": column, "line": version_line, "item": version},
    )
    assert (
        format_pkg_dep(pkg_name, version, product_line, version_line, column)
        == expected_output
    )
