# pylint: disable=invalid-name
"""
Add the gsi_hash_index for all vulnerabilities with source MACHINE

Start Time:    2023-05-30 at 14:37:58 UTC
Finalization Time: 2023-05-30 at 15:03:46 UTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    vulnerabilities as vulns_model,
)
from db_model.enums import (
    Source,
)
from db_model.vulnerabilities.types import (
    VulnerabilityMetadataToUpdate,
)
from organizations import (
    domain as orgs_domain,
)
import time


async def process_group(loaders: Dataloaders, group: str) -> None:
    print(f"Processing {group}")
    group_findings = await loaders.group_findings.load(group)

    findings_vulns = await loaders.finding_vulnerabilities.load_many_chained(
        [fin.id for fin in group_findings]
    )

    machine_vulns_to_update = [
        vuln
        for vuln in findings_vulns
        if (
            vuln.hacker_email == "machine@fluidattacks.com"
            or vuln.state.source == Source.MACHINE
        )
        and vuln.hash is not None
    ]

    await collect(
        (
            vulns_model.update_metadata(
                vulnerability_id=vuln.id,
                finding_id=vuln.finding_id,
                metadata=VulnerabilityMetadataToUpdate(
                    hash=vuln.hash, root_id=vuln.root_id
                ),
            )
            for vuln in machine_vulns_to_update
        ),
        workers=100,
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = sorted(
        await orgs_domain.get_all_active_group_names(loaders=loaders)
    )
    await collect(
        [process_group(loaders, group) for group in groups], workers=15
    )


if __name__ == "__main__":
    execution_time = time.strftime("Start Time:    %Y-%m-%d at %H:%M:%S UTC")
    print(execution_time)
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
