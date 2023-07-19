# pylint: disable=invalid-name
# type: ignore
"""
Replace old authors who have machine findings

Execution Time:    2023-01-12 at 11:37:15 UTC
Finalization Time: 2023-01-12 at 12:15:16 UTC
"""
from aioextensions import (
    collect,
    run,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    EmptyHistoric,
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
    FindingMetadataToUpdate,
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

BAD_AUTHORS = (
    "jrestrepo@fluidattacks.com",
    "jrestrepo@kernelship.com",
    "kamado@fluidattacks.com",
    "drestrepo@fluidattacks.com",
)


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
            entry=states[1]._replace(modified_date=datetime.utcnow()),
            vulnerability_id=vulnerability.id,
        )


async def process_finding(
    loaders: Dataloaders, group_name: str, finding: Finding
) -> None:
    print(f"{group_name} -> {finding.id}: {finding.title}")
    with suppress(EmptyHistoric):
        await findings_model.update_historic_state(
            group_name=group_name,
            finding_id=finding.id,
            historic_state=[
                state._replace(modified_by="machine@fluidattacks.com")
                for state in (
                    await loaders.finding_historic_state.load(finding.id)
                )
                if state.modified_by in BAD_AUTHORS
            ],
        )
    if finding.hacker_email in BAD_AUTHORS:
        await findings_model.update_metadata(
            group_name=group_name,
            finding_id=finding.id,
            metadata=FindingMetadataToUpdate(
                hacker_email="machine@fluidattacks.com"
            ),
        )
    vulns: list[Vulnerability] = await loaders.finding_vulnerabilities.load(
        finding.id
    )
    vulns = [
        vuln
        for vuln in vulns
        if vuln.state.status in (VulnerabilityStateStatus.SAFE,)
        and vuln.state.modified_by == "machine@fluidattacks.com"
        and vuln.state.modified_date.replace(tzinfo=pytz.UTC)
        > datetime(2023, 4, 1).replace(tzinfo=pytz.UTC)
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
            if finding.creation.modified_by in BAD_AUTHORS
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
