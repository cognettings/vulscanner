# pylint: disable=invalid-name
# type: ignore
"""
If a finding was created by an analyst, but has machine vulnerabilities,
pass ownership of the finding to machine

Execution Time:    2023-04-05 at 22:34:07 UTC
Finalization Time: 2023-04-05 at 22:42:41 UTCw
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
from db_model import (
    findings as findings_model,
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
    if finding.creation.modified_by == "machine@fluidattacks.com":
        return
    vulns: list[Vulnerability] = await loaders.finding_vulnerabilities.load(
        finding.id
    )
    vulns = [
        vuln for vuln in vulns if vuln.created_by == "machine@fluidattacks.com"
    ]
    if not vulns:
        return
    print(f"{group_name} -> {finding.id}: {finding.title}")
    await findings_model.update_historic_state(
        group_name=group_name,
        finding_id=finding.id,
        historic_state=[
            (
                (await loaders.finding_historic_state.load(finding.id))[0]
            )._replace(modified_by="machine@fluidattacks.com")
        ],
    )

    vulns = [
        vuln
        for vuln in vulns
        if vuln.state.status in (VulnerabilityStateStatus.SAFE,)
        and vuln.state.modified_by == "machine@fluidattacks.com"
        and vuln.state.modified_date.replace(tzinfo=pytz.UTC)
        > datetime(2023, 3, 31).replace(tzinfo=pytz.UTC)
    ]
    await collect([process_vuln(loaders, vuln) for vuln in vulns], workers=10)


async def process_group(group: str) -> None:
    print(f"Processing {group}")
    loaders: Dataloaders = get_new_context()

    findings: dict[str, Finding] = {
        fin.id: fin
        for fin in (await loaders.group_drafts_and_findings.load(group))
    }

    await collect(
        [
            process_finding(loaders, group, finding)
            for finding in findings.values()
        ],
        workers=3,
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
