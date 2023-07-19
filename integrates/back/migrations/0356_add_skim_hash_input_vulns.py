# pylint: disable=invalid-name
# type: ignore
"""
Modify hash to machine vulnerabilities of input type.

This was because skims was using the url with trailing slashes to calculate
the hashes, and this was causing cycles of closing and opening the same vuln,
this was fixed on the skims logic.

On integrates, the vuln is stored without the trailing slashes, so
the hash in some vulns was updated to match the fix performed in skims to avoid
repetition of the issue.

Execution Time:    2023-01-19 at 00:34:46 UTC
Finalization Time: 2023-01-19 at 00:43:43 UTC
"""
from aioextensions import (
    collect,
    run,
)
import csv
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    VulnerabilityMetadataToUpdate,
)
from db_model.vulnerabilities.update import (
    update_metadata,
)
from organizations import (
    domain as orgs_domain,
)
import time
from vulnerabilities.domain.utils import (
    get_hash_from_machine_vuln,
)


async def process_group(group: str) -> None:
    print(f"Processing {group}")
    loaders: Dataloaders = get_new_context()

    findings: dict[str, Finding] = {
        fin.id: fin
        for fin in (await loaders.group_drafts_and_findings.load(group))
    }
    vulns = await loaders.finding_vulnerabilities.load_many_chained(
        [fin.id for fin in findings.values()]
    )
    vulns = [
        vuln
        for vuln in vulns
        if vuln.type == VulnerabilityType.INPUTS
        and vuln.state.status == VulnerabilityStateStatus.VULNERABLE
        and vuln.skims_method is not None
        and vuln.hacker_email
        in ("kamado@fluidattacks.com", "machine@fluidattacks.com")
    ]
    futures = []
    rows = []
    for vuln in vulns:
        new_hash = await get_hash_from_machine_vuln(loaders, vuln)
        if vuln.hash is not None and vuln.hash == new_hash:
            continue
        futures.append(
            update_metadata(
                vulnerability_id=vuln.id,
                finding_id=vuln.finding_id,
                metadata=VulnerabilityMetadataToUpdate(hash=new_hash),
            )
        )
        rows.append(
            [
                vuln.group_name,
                vuln.finding_id,
                vuln.id,
                "UPDATE" if vuln.hash else "ADD",
            ]
        )
    await collect(futures, workers=50)
    with open("add_skim_hash.csv", "a+", encoding="utf-8") as handler:
        writer = csv.writer(handler)
        writer.writerows(rows)


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = sorted(
        await orgs_domain.get_all_active_group_names(loaders=loaders)
    )
    await collect([process_group(group) for group in groups], workers=10)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
