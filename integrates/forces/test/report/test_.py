from datetime import (
    datetime,
)
from decimal import (
    Decimal,
)
from forces.apis.integrates.api import (
    get_findings,
    get_vulnerabilities,
)
from forces.model import (
    Finding,
    FindingStatus,
    ForcesConfig,
    KindEnum,
    Vulnerability,
    VulnerabilityState,
    VulnerabilityType,
)
from forces.report.data import (
    compile_raw_report,
    get_group_findings_info,
    parse_finding,
    parse_location,
)
from forces.report.filters import (
    filter_repo,
)
from forces.report.styles import (
    style_report,
    style_summary,
)
from forces.report.tables import (
    format_finding_table,
)
from forces.utils.strict_mode import (
    get_policy_compliance,
)
import pytest
from rich.table import (
    Table,
)
from typing import (
    Any,
)
from zoneinfo import (
    ZoneInfo,
)


@pytest.mark.asyncio
async def test_get_group_findings_info(
    test_org: str,
    test_group: str,
    test_token: str,
) -> None:
    findings_dict_1 = await get_group_findings_info(
        organization=test_org, group=test_group, api_token=test_token
    )
    for find in findings_dict_1.values():
        assert find.identifier
        assert find.title
        assert find.status
        assert find.url
        assert find.exploitability


@pytest.mark.asyncio
async def test_parse_finding(
    test_org: str,
    test_group: str,
    test_token: str,
) -> None:
    result: tuple[dict[str, Any], ...] = await get_findings(
        test_group, api_token=test_token
    )
    for finding_dict in result:
        parsed_finding = parse_finding(
            finding_dict=finding_dict, organization=test_org, group=test_group
        )

        assert parsed_finding.identifier == finding_dict["id"]
        assert parsed_finding.title == finding_dict["title"]
        assert (
            parsed_finding.status
            == FindingStatus[str(finding_dict["status"]).upper()]
        )
        assert parsed_finding.exploitability == float(
            finding_dict.get("severity", {}).get("exploitability", 0)
        )
        assert parsed_finding.severity == Decimal(
            str(finding_dict["severityScore"])
        )
        assert parsed_finding.url == (
            f"https://app.fluidattacks.com/orgs/{test_org}/groups/"
            f"{test_group}/vulns/{finding_dict['id']}"
        )
        assert parsed_finding.vulnerabilities == []


@pytest.mark.asyncio
async def test_parse_location(
    test_config: ForcesConfig,
    test_token: str,
) -> None:
    result: tuple[dict[str, Any], ...] = await get_vulnerabilities(
        test_config, api_token=test_token
    )
    dummy_exploitability = 5.0
    for vuln_dict in result:
        parsed_location = parse_location(
            vuln_dict=vuln_dict,
            config=test_config,
            exploitability=dummy_exploitability,
        )

        assert parsed_location.type == (
            VulnerabilityType.SAST
            if vuln_dict["vulnerabilityType"] == "lines"
            else VulnerabilityType.DAST
        )
        assert parsed_location.where == str(vuln_dict["where"])
        assert parsed_location.specific == str(vuln_dict["specific"])
        assert (
            parsed_location.state
            == VulnerabilityState[str(vuln_dict["state"])]
        )
        assert parsed_location.severity == Decimal(
            str(vuln_dict["severityTemporalScore"])
        )
        assert parsed_location.report_date == datetime.fromisoformat(
            str(vuln_dict["reportDate"])
        ).replace(tzinfo=ZoneInfo("America/Bogota"))
        assert parsed_location.exploitability == dummy_exploitability
        assert parsed_location.root_nickname == vuln_dict.get("rootNickname")
        assert parsed_location.compliance == get_policy_compliance(
            config=test_config,
            report_date=datetime.fromisoformat(
                str(vuln_dict["reportDate"])
            ).replace(tzinfo=ZoneInfo("America/Bogota")),
            severity=Decimal(str(vuln_dict["severityTemporalScore"])),
            state=VulnerabilityState[str(vuln_dict["state"])],
        )


@pytest.mark.asyncio
async def test_compile_report(
    test_config: ForcesConfig,
    test_token: str,
    test_finding: str,
) -> None:
    report = await compile_raw_report(
        config=test_config,
        api_token=test_token,
    )
    find: Finding = next(
        find for find in report.findings if find.identifier == test_finding
    )
    assert len(find.vulnerabilities) == 1

    identifiers: set[str] = {find.identifier for find in report.findings}
    assert len(identifiers) == len(report.findings)

    assert report.summary.vulnerable.total == 26
    assert report.summary.group_compliance is False
    assert (
        report.summary.total
        == sum(len(finding.vulnerabilities) for finding in report.findings)
        == 26
    )


@pytest.mark.asyncio
async def test_compile_report_with_preview(
    test_config: ForcesConfig,
    test_token: str,
    test_finding: str,
) -> None:
    report = await compile_raw_report(
        config=test_config._replace(feature_preview=True),
        api_token=test_token,
    )
    find: Finding = next(
        find for find in report.findings if find.identifier == test_finding
    )
    assert len(find.vulnerabilities) == 1

    identifiers: set[str] = {find.identifier for find in report.findings}
    assert len(identifiers) == len(report.findings)

    assert report.summary.vulnerable.total == 26
    assert report.summary.group_compliance is False
    assert report.summary.total == 26


def test_style_summary() -> None:
    assert style_summary(VulnerabilityState.ACCEPTED, 1) == "1"
    assert style_summary(VulnerabilityState.VULNERABLE, 0) == "[green]0[/]"
    assert style_summary(VulnerabilityState.VULNERABLE, 9) == "[yellow3]9[/]"
    assert style_summary(VulnerabilityState.VULNERABLE, 17) == "[orange3]17[/]"
    assert style_summary(VulnerabilityState.VULNERABLE, 25) == "[red]25[/]"
    assert style_summary(VulnerabilityState.SAFE, 15) == "[green]15[/]"


def test_style_report() -> None:
    assert style_report("tittle", "some_value") == "some_value"
    assert style_report("title", "some_value") == "[yellow]some_value[/]"
    assert style_report("state", "vulnerable") == "[red]vulnerable[/]"
    assert style_report("state", "vulnerablee") == "vulnerablee"


def test_filter_repo() -> None:
    vuln: Vulnerability = Vulnerability(
        type=VulnerabilityType.DAST,
        where="somewhere",
        specific="port 21",
        state=VulnerabilityState.VULNERABLE,
        severity=Decimal("6.0"),
        report_date=datetime.now(tz=ZoneInfo("America/Bogota")),
        exploitability=4.5,
        root_nickname=None,
        compliance=True,
    )
    assert filter_repo(
        vuln=vuln,
        repo_name="root_test",
        kind=KindEnum.DYNAMIC,
    )
    assert filter_repo(
        vuln=vuln,
        kind=KindEnum.DYNAMIC,
    )


def test_happy_path_format_finding_table() -> None:
    config = ForcesConfig(organization="test_org", group="test_group")
    vuln1 = Vulnerability(
        type=VulnerabilityType.DAST,
        where="test_location",
        specific="test_specific",
        state=VulnerabilityState.VULNERABLE,
        severity=Decimal("7.5"),
        report_date=datetime.now(),
        root_nickname=None,
        exploitability=0.97,
        compliance=True,
    )
    vuln2 = Vulnerability(
        type=VulnerabilityType.SAST,
        where="test_location2",
        specific="test_specific2",
        state=VulnerabilityState.SAFE,
        severity=Decimal("5.0"),
        report_date=datetime.now(),
        root_nickname=None,
        exploitability=0.91,
        compliance=True,
    )
    finding = Finding(
        identifier="test_id",
        title="test_title",
        status=FindingStatus.VULNERABLE,
        exploitability=0.97,
        severity=Decimal("7.5"),
        url="https://test.com",
        vulnerabilities=[vuln1, vuln2],
    )
    filtered_vulns = (vuln1, vuln2)
    table = Table()
    result_table = format_finding_table(config, finding, filtered_vulns, table)
    assert len(result_table.rows) == 7
    # pylint: disable=protected-access
    assert result_table.columns[0]._cells[0] == "title"
    assert result_table.columns[0]._cells[1] == "URL"
    assert result_table.columns[0]._cells[2] == "state"
    assert result_table.columns[0]._cells[3] == "exploit"
    assert result_table.columns[0]._cells[4] == "severity"
    assert result_table.columns[0]._cells[5] == "vulnerable"
