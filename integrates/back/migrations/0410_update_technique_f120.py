# pylint: disable=invalid-name
"""
Update the 'technique' field of machine vulnerabilities of F120.

Execution Time:    2023-07-05 at 17:56:47 UTC
Finalization Time: 2023-07-05 at 18:00:57 UTC

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
from db_model.vulnerabilities.enums import (
    VulnerabilityTechnique,
)
from db_model.vulnerabilities.types import (
    VulnerabilityMetadataToUpdate,
)
from organizations.domain import (
    get_all_group_names,
)
import time


async def process_group(
    loaders: Dataloaders,
    group_name: str,
) -> None:
    findings = await loaders.group_findings.load(group_name)
    findings_numb = [
        finding for finding in findings if finding.title.startswith("120")
    ]
    findings_vulns = await loaders.finding_vulnerabilities.load_many_chained(
        [finding.id for finding in findings_numb]
    )

    f120_machine_vulns = [
        vuln
        for vuln in findings_vulns
        if (
            vuln.hacker_email == "machine@fluidattacks.com"
            or vuln.state.source == Source.MACHINE
        )
    ]

    if f120_machine_vulns:
        await collect(
            tuple(
                vulns_model.update_metadata(
                    finding_id=vuln.finding_id,
                    vulnerability_id=vuln.id,
                    metadata=VulnerabilityMetadataToUpdate(
                        technique=VulnerabilityTechnique.SCA
                    ),
                )
                for vuln in f120_machine_vulns
            ),
            workers=20,
        )

    print(f"Group processed {group_name}")


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = sorted(await get_all_group_names(loaders))
    await collect(
        [process_group(loaders, group) for group in groups], workers=8
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
