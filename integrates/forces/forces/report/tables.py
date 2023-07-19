from collections import (
    Counter,
)
from forces.model import (
    Finding,
    ForcesConfig,
    KindEnum,
    ReportSummary,
    Vulnerability,
    VulnerabilityState,
)
from forces.report.styles import (
    get_exploitability_measure,
    style_report,
    style_summary,
)
from operator import (
    attrgetter,
)
from rich.box import (
    MINIMAL,
)
from rich.table import (
    Table,
)


def format_vuln_table(
    config: ForcesConfig, vulns: tuple[Vulnerability, ...]
) -> Table:
    """Helper method to create the nested vulns table

    Args:
        `config (ForcesConfig)`: Valid Forces config
        `vulns (tuple[Vulnerability, ...])`: Finding vulnerabilities

    Returns:
        `Table`: A vuln table that gets nested within the respective Finding
        table
    """
    vuln_table = Table(
        show_header=False,
        highlight=True,
        box=MINIMAL,
        border_style="gold1",
    )
    vuln_table.add_column("Vuln attr", style="cyan")
    vuln_table.add_column(
        "Vuln attr values", style="honeydew2", overflow="fold"
    )
    for vuln in vulns:
        vuln_table.add_row("type", style_report("type", vuln.type))
        vuln_table.add_row("where", style_report("where", vuln.where))
        vuln_table.add_row("specific", style_report("specific", vuln.specific))
        vuln_table.add_row(
            "state",
            style_report("state", vuln.state),
        )
        vuln_table.add_row(
            "severity",
            style_report("severity", str(vuln.severity)),
            end_section=not config.strict,
        )
        if config.strict:
            vuln_table.add_row(
                "compliance",
                style_report(
                    "compliance",
                    "Compliant" if vuln.compliance else "No, breaks build",
                ),
                end_section=True,
            )
    return vuln_table


def format_finding_table(
    config: ForcesConfig,
    finding: Finding,
    filtered_vulns: tuple[Vulnerability, ...],
    table: Table,
) -> Table:
    """Helper method to create and append the Finding tables to the Group
    Report

    Args:
        `config (ForcesConfig)`: Valid Forces config
        `finding (Finding)`: A tuple containing a Finding's data
        `filtered_vulns (tuple[Vulnerability, ...])`: The filtered vulns
        of this Finding according to the configured verbosity
        `table (Table)`: The Group Report table to be appended

    Returns:
        `Table`: The Group Report table with the Finding info appended to it
    """
    finding_summary: Counter = Counter(
        [vuln.state for vuln in finding.vulnerabilities]
    )
    table.add_row("title", style_report("title", finding.title))
    table.add_row("URL", finding.url)
    table.add_row("state", style_report("state", finding.status))
    table.add_row(
        "exploit",
        style_report(
            "exploit", get_exploitability_measure(finding.exploitability)
        ),
    )
    table.add_row("severity", style_report("severity", str(finding.severity)))
    vuln_state = VulnerabilityState.VULNERABLE
    table.add_row(
        vuln_state,
        style_report(vuln_state, str(finding_summary[vuln_state])),
    )
    vulns_data: Table = format_vuln_table(config, filtered_vulns)
    table.add_row("locations", vulns_data, end_section=True)

    return table


def format_summary_report(summary: ReportSummary, kind: KindEnum) -> Table:
    """Helper method to create the findings summary table from the report's
    summary data

    Args:
        `summary (ReportSummary)`: A tuple with the raw summary data
        `kind (KindEnum)`: The kind of vulnerabilities forces should focus on
        to

    Returns:
        `Table`: The summary table that gets outputted after the Findings table
    """
    summary_table = Table(
        title="Summary",
        show_header=False,
        highlight=True,
        box=MINIMAL,
        border_style="blue",
        width=35,
        caption=(
            f"Total: {summary.total} vulnerabilities\n"
            f"Elapsed time: {summary.elapsed_time}"
        ),
    )
    # vulnerable, safe and accepted
    summary_table.add_column("Vuln state", style="cyan")
    state = VulnerabilityState.VULNERABLE
    if kind == KindEnum.ALL:
        # DAST, SAST and total vulns for each
        summary_table.add_column("Vuln type", style="magenta1")
        summary_table.add_column("Value")
        put_state_label: bool = True
        for vuln_sum in ("DAST", "SAST", "total"):
            summary_table.add_row(
                state if put_state_label else None,
                vuln_sum,
                style_summary(
                    state,
                    attrgetter(f"{state.value}.{vuln_sum.lower()}")(summary),
                ),
                end_section=vuln_sum == "total",
            )
            put_state_label = False
    else:
        summary_table.add_column("Value")
        summary_table.add_row(
            state,
            style_summary(
                state,
                attrgetter(f"{state.value}.total")(summary),
            ),
            end_section=True,
        )
    return summary_table
