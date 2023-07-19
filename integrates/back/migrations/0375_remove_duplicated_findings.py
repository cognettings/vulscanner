# pylint: disable=invalid-name
# type: ignore
"""
Remove duplicate findings and revert vulnerabilities that
were closed by machine

Execution Time:    2023-04-10 at 15:45:44 UTC
Finalization Time: 2023-04-10 at 15:57:00 UTC
"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
)
from db_model.vulnerabilities.update import (
    update_historic_entry,
)
from findings.domain.core import (
    remove_finding,
)
from organizations import (
    domain as orgs_domain,
)
import pytz
import time


async def process_vuln(
    loaders: Dataloaders, vulnerability: Vulnerability
) -> None:
    states: list[
        VulnerabilityState
    ] = await loaders.vulnerability_historic_state.load(vulnerability.id)
    if len(states) > 1:
        await update_historic_entry(
            current_value=vulnerability,
            finding_id=vulnerability.finding_id,
            entry=states[-2]._replace(modified_date=datetime.utcnow()),
            vulnerability_id=vulnerability.id,
        )


async def process_finding(
    loaders: Dataloaders, group_name: str, finding: Finding
) -> None:
    vulns: list[Vulnerability] = await loaders.finding_vulnerabilities.load(
        finding.id
    )
    vulns = [
        vuln for vuln in vulns if vuln.created_by == "machine@fluidattacks.com"
    ]
    if not vulns:
        return

    vulns = [
        vuln
        for vuln in vulns
        if vuln.state.status in (VulnerabilityStateStatus.SAFE,)
        and vuln.state.modified_by == "machine@fluidattacks.com"
        and vuln.state.modified_date.replace(tzinfo=pytz.UTC)
        > datetime(2023, 3, 30).replace(tzinfo=pytz.UTC)
    ]
    if vulns:
        print(f"{group_name} -> {finding.id}: {finding.title}")
        await collect(
            [process_vuln(loaders, vuln) for vuln in vulns], workers=10
        )


async def process_group(group: str) -> None:
    print(f"Processing {group}")
    loaders: Dataloaders = get_new_context()

    findings: dict[str, Finding] = {
        fin.id: fin
        for fin in (await loaders.group_drafts_and_findings.load(group))
    }

    same_type_of_findings: dict[str, list[Finding]] = {}
    for finding in findings.values():
        if "022" in finding.title:
            print(finding.id)
        if finding.creation.modified_by != "machine@fluidattacks.com":
            continue
        criteria_number = finding.title.split(".")[0]
        if criteria_number in same_type_of_findings:
            same_type_of_findings[criteria_number] = [
                *(same_type_of_findings[criteria_number]),
                finding,
            ]
        else:
            same_type_of_findings[criteria_number] = [finding]

    for repeat_findings in same_type_of_findings.values():
        if len(repeat_findings) < 2:
            continue
        repeat_findings = list(
            sorted(
                repeat_findings,
                key=lambda x: x.creation.modified_date.timestamp(),
            )
        )
        await process_finding(loaders, group, repeat_findings[0])
        await collect(
            [
                remove_finding(
                    loaders,
                    "machine@fluidattacks.com",
                    x.id,
                    StateRemovalJustification.DUPLICATED,
                    Source.MACHINE,
                )
                for x in repeat_findings[1:]
            ]
        )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = sorted(
        await orgs_domain.get_all_active_group_names(loaders=loaders)
    )
    await collect(
        [process_group(group) for group in reversed(groups)], workers=10
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
