import pytest
from pytest_mock import (
    MockerFixture,
)
from s3.model.types import (
    Advisory,
)
from schedulers.update_sca_table.repositories.advisory_database import (
    append_advisories,
    get_advisory_database,
    get_final_range,
    get_limit,
    get_vulnerabilities_ranges,
    URL_ADVISORY_DATABASE,
)
from test.unit.schedulers.types import (
    UPD_SCA_TABLE_STR,
)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "parameters,expected",
    [
        (("=3.11", ">=3.11 <3.11.1"), "=3.11 || >=3.11 <3.11.1"),
        (
            (">=3.9.0 <3.9.3", ">=3.8.0 <3.8.6"),
            ">=3.9.0 <3.9.3 || >=3.8.0 <3.8.6",
        ),
        (("=3.4.2", "=3.5.6"), "=3.4.2 || =3.5.6"),
    ],
)
def test_get_final_range(parameters: tuple[str, str], expected: str) -> None:
    formated_range: str = get_final_range(*parameters)
    assert formated_range == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "events,db_specific,expected",
    [
        (
            [{"introduced": "1.0.2"}, {"last_affected": "1.2.4"}],
            None,
            " <=1.2.4",
        ),
        (
            [{"introduced": "1.3.5"}, {"fixed": "2.3.6"}],
            None,
            " <2.3.6",
        ),
        ([{"introduced": "1.0.2"}], None, ""),
        (
            [{"introduced": "1.0.2"}],
            {"last_known_affected_version_range": "< 2.3.6"},
            " <2.3.6",
        ),
    ],
)
def test_get_limit(
    events: list[dict[str, str]], db_specific: dict | None, expected: str
) -> None:
    dict_test: dict = {
        "package": {"ecosystem": "npm", "name": "vega"},
        "ranges": [
            {
                "type": "ECOSYSTEM",
                "events": events,
            }
        ],
    }
    if db_specific:
        dict_test["database_specific"] = db_specific
    formated_range: str = get_limit(events, dict_test)
    assert formated_range == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "current_advisories,expected",
    [
        (
            {"http": {"version": ">=0 <0.13.3", "platform": "pub"}},
            [
                Advisory(
                    id="CVE-EXAMPLE-1",
                    package_manager="pub",
                    package_name="http",
                    severity=None,
                    source=URL_ADVISORY_DATABASE,
                    vulnerable_version=">=0 <0.13.3",
                )
            ],
        ),
        ({}, []),
    ],
)
def test_append_advisories(
    current_advisories: dict[str, dict[str, str]], expected: list[Advisory]
) -> None:
    advisories: list[Advisory] = []
    vuln_id: str = "CVE-EXAMPLE-1"
    severity: None = None
    cwe_ids: None = None
    append_advisories(
        advisories, current_advisories, vuln_id, severity, cwe_ids
    )
    assert advisories == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "affected",
    [
        [
            {
                "package": {"ecosystem": "npm", "name": "vega"},
                "ranges": [
                    {
                        "type": "ECOSYSTEM",
                        "events": [
                            {"introduced": "0"},
                            {"fixed": "5.23.0"},
                        ],
                    }
                ],
            }
        ],
        [
            {
                "package": {"ecosystem": "Packagist", "name": "php_pkg"},
                "ranges": [
                    {
                        "type": "ECOSYSTEM",
                        "events": [
                            {"introduced": "1.0.1"},
                            {"last_affected": "2.24.5"},
                        ],
                    }
                ],
            },
            {
                "package": {"ecosystem": "Packagist", "name": "php_pkg"},
                "ranges": [
                    {
                        "type": "ECOSYSTEM",
                        "events": [
                            {"introduced": "3.0.5"},
                            {"fixed": "4.0.8"},
                        ],
                    }
                ],
            },
        ],
    ],
)
def test_get_vulnerabilities_ranges(
    mocker: MockerFixture, affected: list[dict]
) -> None:
    advisories: list[Advisory] = []
    vuln_id: str = "CVE-EXAMPLE"
    severity: None = None
    cwe_ids = None
    len_affected: int = len(affected)
    pkg_info: dict[str, str] = affected[0]["package"]
    final_range_output: str = "final_range_output"
    adv_db_mod_str: str = f"{UPD_SCA_TABLE_STR}.repositories.advisory_database"
    get_limit_mock = mocker.patch(
        f"{adv_db_mod_str}.get_limit", return_value="test_output"
    )
    get_final_range_mock = mocker.patch(
        f"{adv_db_mod_str}.get_final_range", return_value=final_range_output
    )
    append_advs_mock = mocker.patch(f"{adv_db_mod_str}.append_advisories")
    get_vulnerabilities_ranges(
        affected, vuln_id, advisories, severity, cwe_ids
    )
    assert get_limit_mock.call_count == len_affected
    assert get_final_range_mock.call_count == len_affected
    assert append_advs_mock.call_args.args == (
        advisories,
        {
            pkg_info["name"]: {
                "version": " || ".join([final_range_output] * len_affected),
                "platform": pkg_info["ecosystem"].lower(),
            }
        },
        vuln_id,
        severity,
        cwe_ids,
        None,
    )


@pytest.mark.skims_test_group("unittesting")
def test_get_advisory_database(mocker: MockerFixture) -> None:
    advisories: list[Advisory] = []
    tmp_dirname: str = "skims/test/data/sca_scheduler"
    expected: list[dict] = [
        {
            "advisory": "GHSA-2qh6-hhvv-m2ww",
            "affected": [
                {
                    "package": {
                        "ecosystem": "Maven",
                        "name": "org.jenkins-ci.plugins:http_request",
                    },
                    "ranges": [
                        {
                            "type": "ECOSYSTEM",
                            "events": [{"introduced": "0"}, {"fixed": "1.16"}],
                        }
                    ],
                }
            ],
            "severity": "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N",
            "cwe_ids": ["CWE-256", "CWE-668"],
        },
        {
            "advisory": "GHSA-h79p-32mx-fjj9",
            "affected": [
                {
                    "package": {
                        "ecosystem": "Maven",
                        "name": "org.apache.camel:camel-netty",
                    },
                    "ranges": [
                        {
                            "type": "ECOSYSTEM",
                            "events": [
                                {"introduced": "3.0.0"},
                                {"fixed": "3.2.0"},
                            ],
                        }
                    ],
                }
            ],
            "severity": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
            "cwe_ids": ["CWE-502"],
        },
    ]
    mocker.patch("builtins.print")
    get_vulns_mock = mocker.patch(
        (
            f"{UPD_SCA_TABLE_STR}.repositories"
            ".advisory_database.get_vulnerabilities_ranges"
        )
    )
    get_advisory_database(advisories, tmp_dirname)
    assert get_vulns_mock.call_args_list == [
        (
            (
                pkg["affected"],
                pkg["advisory"],
                advisories,
                pkg["severity"],
                pkg["cwe_ids"],
                None,
            ),
        )
        for pkg in expected
    ]
