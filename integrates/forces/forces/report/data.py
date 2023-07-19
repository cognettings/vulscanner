from .filters import (
    filter_kind,
    filter_repo,
)
from datetime import (
    datetime,
)
from decimal import (
    Decimal,
)
from forces.apis.integrates.api import (
    get_findings,
    get_vulnerabilities,
    get_vulnerabilities_fallback,
)
from forces.model import (
    Finding,
    FindingStatus,
    ForcesConfig,
    ForcesData,
    ReportSummary,
    SummaryItem,
    Vulnerability,
    VulnerabilityState,
    VulnerabilityType,
)
from forces.utils.logs import (
    log_to_remote,
)
from forces.utils.strict_mode import (
    get_policy_compliance,
)
from timeit import (
    default_timer as timer,
)
from typing import (
    Any,
)
from zoneinfo import (
    ZoneInfo,
)


def parse_finding(
    finding_dict: dict[str, Any],
    organization: str,
    group: str,
) -> Finding:
    return Finding(
        identifier=str(finding_dict["id"]),
        title=str(finding_dict["title"]),
        status=FindingStatus[str(finding_dict["status"]).upper()],
        exploitability=float(
            finding_dict.get("severity", {}).get("exploitability", 0)
        ),
        severity=Decimal(str(finding_dict["severityScore"])),
        url=(
            f"https://app.fluidattacks.com/orgs/{organization}/groups/"
            f"{group}/vulns/{finding_dict['id']}"
        ),
        vulnerabilities=[],
    )


def parse_location(
    vuln_dict: dict[str, Any],
    config: ForcesConfig,
    exploitability: float,
) -> Vulnerability:
    severity: Decimal = Decimal(str(vuln_dict["severityTemporalScore"]))

    return Vulnerability(
        type=(
            VulnerabilityType.SAST
            if vuln_dict["vulnerabilityType"] == "lines"
            else VulnerabilityType.DAST
        ),
        where=str(vuln_dict["where"]),
        specific=str(vuln_dict["specific"]),
        state=VulnerabilityState[str(vuln_dict["state"])],
        severity=severity,
        report_date=datetime.fromisoformat(
            str(vuln_dict["reportDate"])
        ).replace(tzinfo=ZoneInfo("America/Bogota")),
        exploitability=exploitability,
        root_nickname=vuln_dict.get("rootNickname"),
        compliance=get_policy_compliance(
            config=config,
            report_date=datetime.fromisoformat(
                str(vuln_dict["reportDate"])
            ).replace(tzinfo=ZoneInfo("America/Bogota")),
            severity=severity,
            state=VulnerabilityState[str(vuln_dict["state"])],
        ),
    )


async def get_group_findings_info(
    organization: str,
    group: str,
    **kwargs: str,
) -> dict[str, Finding]:
    """Format the findings of a group into a dictionary

    Args:
        `organization (str)`: Organization name
        `group (str)`: Group name

    Returns:
        `dict[str, Finding]`: A dictionary containing the findings of a group
        with their identifier as key
    """
    findings_dict: dict[str, Finding] = {}
    findings = await get_findings(group, **kwargs)
    for finding_dict in findings:
        try:
            findings_dict[finding_dict["id"]] = parse_finding(
                finding_dict=finding_dict,
                organization=organization,
                group=group,
            )
        except (ArithmeticError, KeyError, TypeError, ValueError) as exc:
            await log_to_remote(exc)
            continue
    return findings_dict


async def compile_raw_report(
    config: ForcesConfig,
    **kwargs: Any,
) -> ForcesData:
    """Parses and compiles the data needed for the Forces Report.

    Args:
        `config (ForcesConfig)`: Valid Forces config

    Returns:
        `ForcesData`: A namedtuple with the findings data and a summary
    """
    _start_time: float = timer()

    _summary_dict: dict[VulnerabilityState, dict[str, int]] = {
        VulnerabilityState.VULNERABLE: {"DAST": 0, "SAST": 0, "total": 0},
        VulnerabilityState.SAFE: {"DAST": 0, "SAST": 0, "total": 0},
        VulnerabilityState.ACCEPTED: {"DAST": 0, "SAST": 0, "total": 0},
    }
    findings_dict = await get_group_findings_info(
        organization=config.organization,
        group=config.group,
        **kwargs,
    )
    group_vulnerabilities: tuple[dict[str, Any], ...] = (
        await get_vulnerabilities_fallback(config, **kwargs)
        if config.feature_preview
        else await get_vulnerabilities(config, **kwargs)
    )
    group_compliance: bool = True

    for vuln_dict in group_vulnerabilities:
        try:
            finding_id: str = str(vuln_dict["findingId"])

            vulnerability = parse_location(
                vuln_dict=vuln_dict,
                config=config,
                exploitability=findings_dict[finding_id].exploitability,
            )

            if not filter_kind(vulnerability, config.kind) or not filter_repo(
                vulnerability, config.kind, config.repository_name
            ):
                continue

            _summary_dict[vulnerability.state]["total"] += 1
            _summary_dict[vulnerability.state]["DAST"] += bool(
                vulnerability.type == VulnerabilityType.DAST
            )
            _summary_dict[vulnerability.state]["SAST"] += bool(
                vulnerability.type == VulnerabilityType.SAST
            )

            findings_dict[finding_id].vulnerabilities.append(vulnerability)
            if not vulnerability.compliance:
                group_compliance = False

        except (ArithmeticError, KeyError, TypeError, ValueError) as exc:
            await log_to_remote(exc)
            continue

    summary = ReportSummary(
        vulnerable=SummaryItem(
            dast=_summary_dict[VulnerabilityState.VULNERABLE]["DAST"],
            sast=_summary_dict[VulnerabilityState.VULNERABLE]["SAST"],
            total=_summary_dict[VulnerabilityState.VULNERABLE]["total"],
        ),
        group_compliance=group_compliance,
        total=_summary_dict[VulnerabilityState.VULNERABLE]["total"],
        elapsed_time=f"{(timer() - _start_time):.4f} seconds",
    )

    return ForcesData(
        findings=tuple(findings_dict.values()),
        summary=summary,
    )
