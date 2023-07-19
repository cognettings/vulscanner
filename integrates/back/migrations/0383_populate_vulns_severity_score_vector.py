# pylint: disable=invalid-name
"""
Populate field cvss_v3 in map severity_score for all vulnerabilities.
This field contains the CVSS 3.1 vector string and it will be taken from
the parent finding in case the cvss_v3 field is empty.
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
from db_model.findings.types import (
    Finding,
)
from db_model.types import (
    SeverityScore,
)
from db_model.vulnerabilities.types import (
    VulnerabilityMetadataToUpdate,
)
from organizations.domain import (
    get_all_group_names,
)
import time


async def process_finding(
    loaders: Dataloaders,
    finding: Finding,
) -> None:
    if not finding.severity_score or finding.severity_score == SeverityScore():
        return

    vulns = await loaders.finding_vulnerabilities_all.load(finding.id)
    vulns_to_update = [
        vuln
        for vuln in vulns
        if not vuln.severity_score or not vuln.severity_score.cvss_v3
    ]
    if not vulns_to_update:
        return

    await collect(
        tuple(
            vulns_model.update_metadata(
                finding_id=finding.id,
                vulnerability_id=vuln.id,
                metadata=VulnerabilityMetadataToUpdate(
                    severity_score=finding.severity_score
                ),
            )
            for vuln in vulns_to_update
        ),
        workers=8,
    )
    print(f"{finding.id=} {len(vulns_to_update)=}")


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    group_findings = await loaders.group_findings_all.load(group_name)
    if not group_findings:
        return

    await collect(
        tuple(process_finding(loaders, finding) for finding in group_findings),
        workers=4,
    )
    print(f"Group processed {group_name} {str(round(progress, 2))}")


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(await get_all_group_names(loaders))
    print(f"{group_names=}")
    print(f"{len(group_names)=}")
    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group,
                progress=count / len(group_names),
            )
            for count, group in enumerate(group_names)
        ),
        workers=4,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
