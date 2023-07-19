from collections.abc import (
    Callable,
)
from custom_exceptions import (
    InvalidRange,
)
from custom_utils.vulnerabilities import (
    as_range,
    format_vulnerabilities,
    get_closing_date,
    get_opening_date,
    get_ranges,
    get_treatment_from_org_finding_policy,
    group_specific,
    is_range,
    range_to_list,
    sort_vulnerabilities,
    ungroup_specific,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


def test_as_range() -> None:
    range_to_stringify = [1, 2, 3, 4, 5]
    test_data = as_range(range_to_stringify)
    expected_output = "1-5"
    assert test_data == expected_output


async def test_format_vulnerabilities(
    mock_vulnerabilities_finding: Callable,
    mock_vulnerabilitie_roots: Callable,
) -> None:
    finding_id = "422286126"
    finding_vulns = mock_vulnerabilities_finding(finding_id)
    vulns_roots = [
        mock_vulnerabilitie_roots(vuln.root_id)
        if vuln.root_id
        else vuln.root_id
        for vuln in finding_vulns
    ]
    test_data = format_vulnerabilities(finding_vulns, vulns_roots)
    expected_output = {
        "ports": [],
        "lines": [
            {
                "path": "universe/path/to/file3.ext",
                "line": "345",
                "state": "submitted",
                "source": "analyst",
                "tool": {"name": "tool-1", "impact": "direct"},
                "commit_hash": "e17059d1e17059d1e17059d1e17059d1e17059d1",
                "repo_nickname": "universe",
            },
            {
                "path": "test/data/lib_path/f060/csharp.cs",
                "line": "12",
                "state": "open",
                "source": "analyst",
                "tool": {"name": "tool-2", "impact": "indirect"},
                "commit_hash": "ea871eee64cfd5ce293411efaf4d3b446d04eb4a",
                "cvss_v3": (
                    "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:P/"
                    "RL:O/RC:C"
                ),
                "cwe_ids": ["CWE-1035", "CWE-770", "CWE-937"],
            },
            {
                "path": "universe/path/to/file3.ext",
                "line": "347",
                "state": "rejected",
                "source": "analyst",
                "tool": {"name": "tool-1", "impact": "direct"},
                "commit_hash": "e17059d1e17059d1e17059d1e17059d1e17059d1",
                "repo_nickname": "universe",
            },
        ],
        "inputs": [
            {
                "url": "https://example.com",
                "field": "phone",
                "state": "open",
                "source": "analyst",
                "tool": {"name": "tool-2", "impact": "indirect"},
                "cvss_v3": (
                    "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:P/"
                    "RL:O/RC:C"
                ),
                "cwe_ids": ["CWE-1035", "CWE-770", "CWE-937"],
            }
        ],
    }

    assert test_data == expected_output


def test_get_vuln_closing_date(
    mock_vulnerability: Callable,
) -> None:
    closed_vulnerability = Vulnerability(
        created_by="test@test.com",
        created_date=datetime.fromisoformat("2019-01-08T21:01:26+00:00"),
        finding_id="422286126",
        group_name="unittesting",
        organization_name="okada",
        hacker_email="test@test.com",
        id="80d6a69f-a376-46be-98cd-2fdedcffdcc0",
        state=VulnerabilityState(
            modified_by="test@test.com",
            modified_date=datetime.fromisoformat("2019-01-08T21:01:26+00:00"),
            source=Source.ASM,
            specific="phone",
            status=VulnerabilityStateStatus.SAFE,
            where="https://example.com",
        ),
        type=VulnerabilityType.INPUTS,
        unreliable_indicators=VulnerabilityUnreliableIndicators(
            unreliable_source=Source.ASM,
        ),
    )
    test_data = get_closing_date(closed_vulnerability)
    closing_date = datetime(2019, 1, 8).date()
    assert test_data == closing_date
    vulnerability_id = "80d6a69f-a376-46be-98cd-2fdedcffdcc0"
    open_vulnerability = mock_vulnerability(vulnerability_id)

    assert open_vulnerability
    test_data = get_closing_date(open_vulnerability)
    assert test_data is None


def test_get_vuln_opening_date(
    mock_vulnerability: Callable,
) -> None:
    test_vuln = Vulnerability(
        created_by="test@test.com",
        created_date=datetime.fromisoformat("2019-01-08T21:01:26+00:00"),
        finding_id="",
        group_name="",
        organization_name="",
        hacker_email="",
        id="",
        type=VulnerabilityType.LINES,
        state=VulnerabilityState(
            modified_by="",
            modified_date=datetime.fromisoformat("2019-01-08T21:01:26+00:00"),
            source=Source.ASM,
            specific="",
            status=VulnerabilityStateStatus.VULNERABLE,
            where="",
        ),
        unreliable_indicators=VulnerabilityUnreliableIndicators(
            unreliable_source=Source.ASM,
            unreliable_treatment_changes=0,
            unreliable_report_date=datetime.fromisoformat(
                "2019-01-08T21:01:26+00:00"
            ),
        ),
    )
    result_date = get_opening_date(test_vuln)
    assert result_date == datetime(2019, 1, 8).date()

    min_date = datetime(2021, 1, 1).date()
    result_date = get_opening_date(vuln=test_vuln, min_date=min_date)
    assert result_date is None

    vulnerability_id = "80d6a69f-a376-46be-98cd-2fdedcffdcc0"
    open_vulnerability = mock_vulnerability(vulnerability_id)
    assert open_vulnerability
    result_date = get_opening_date(open_vulnerability)
    expected_output = datetime(2020, 9, 9).date()
    assert result_date == expected_output


def test_get_ranges() -> None:
    working_list = [1, 2, 3, 7, 9, 10, 11, 12, 13, 19]
    test_data = get_ranges(working_list)
    expected_output = "1-3,7,9-13,19"
    assert test_data == expected_output


@pytest.mark.parametrize(
    ["modified_date", "user_email"],
    [
        [
            datetime.fromisoformat("2020-01-01T20:07:57+00:00"),
            "unittesting@fluidattacks.com",
        ]
    ],
)
def test_get_treatment_from_org_finding_policy(
    modified_date: datetime, user_email: str
) -> None:
    result = get_treatment_from_org_finding_policy(
        modified_date=modified_date, user_email=user_email
    )
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(
        isinstance(result[i], VulnerabilityTreatment)
        for i in range(len(result))
    )


def test_group_specific(
    mock_vulnerabilities_finding: Callable,
) -> None:
    finding_id = "422286126"
    finding_vulns = mock_vulnerabilities_finding(finding_id)
    test_data = group_specific(finding_vulns, VulnerabilityType.INPUTS)
    assert isinstance(test_data, list)
    assert len(test_data) == 3
    assert isinstance(test_data[0], Vulnerability)
    assert test_data[0] is not None


def test_is_range() -> None:
    range_value = "100-200"
    no_range_value = "20"
    assert is_range(range_value)
    assert not is_range(no_range_value)


@pytest.mark.parametrize(
    ["range_value", "expected_output", "range_to_raise_exception"],
    [["10-15", ["10", "11", "12", "13", "14", "15"], "13-12"]],
)
def test_range_to_list(
    range_value: str,
    expected_output: list,
    range_to_raise_exception: str,
) -> None:
    result = range_to_list(range_value)
    assert isinstance(result, list)
    assert result == expected_output
    with pytest.raises(InvalidRange):
        assert range_to_list(range_to_raise_exception)


def test_sort_vulnerabilities() -> None:
    vulns = [
        Vulnerability(
            created_by="test@test.com",
            created_date=datetime.fromisoformat("2018-04-08T00:45:11+00:00"),
            finding_id="",
            group_name="",
            organization_name="",
            hacker_email="",
            id="",
            state=VulnerabilityState(
                modified_by="",
                modified_date=datetime.fromisoformat(
                    "2019-01-08T21:01:26+00:00"
                ),
                source=Source.ASM,
                specific="",
                status=VulnerabilityStateStatus.VULNERABLE,
                where=where,
            ),
            type=VulnerabilityType.INPUTS,
            unreliable_indicators=VulnerabilityUnreliableIndicators(
                unreliable_source=Source.ASM,
            ),
        )
        for where in ("abaa", "1abc", "aaaa")
    ]
    expected_output = [
        Vulnerability(
            created_by="test@test.com",
            created_date=datetime.fromisoformat("2018-04-08T00:45:11+00:00"),
            finding_id="",
            group_name="",
            organization_name="",
            hacker_email="",
            id="",
            state=VulnerabilityState(
                modified_by="",
                modified_date=datetime.fromisoformat(
                    "2019-01-08T21:01:26+00:00"
                ),
                source=Source.ASM,
                specific="",
                status=VulnerabilityStateStatus.VULNERABLE,
                where=where,
            ),
            type=VulnerabilityType.INPUTS,
            unreliable_indicators=VulnerabilityUnreliableIndicators(
                unreliable_source=Source.ASM,
            ),
        )
        for where in ("1abc", "aaaa", "abaa")
    ]
    test_data = sort_vulnerabilities(vulns)
    assert test_data == expected_output


def test_ungroup_specific() -> None:
    specific = "13,14,18-20,24-30,40"
    test_data = ungroup_specific(specific)
    expected_output = [
        "13",
        "14",
        "18",
        "19",
        "20",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
        "40",
    ]
    assert isinstance(test_data, list)
    assert test_data == expected_output
