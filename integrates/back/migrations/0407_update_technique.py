# pylint: disable=invalid-name
"""
Update the 'technique' field for some vulnerabilities.

CLOUD -> CSPM or SAST depending the case.
SAST with skims_technique = apk -> DAST.

Execution Time:    2023-06-27 at 21:20:09 UTC
Finalization Time: 2023-06-27 at 21:34:37 UTC

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
    Vulnerability,
    VulnerabilityMetadataToUpdate,
)
from organizations.domain import (
    get_all_group_names,
)
import time


def get_technique(vuln: Vulnerability) -> VulnerabilityTechnique:
    convert_to = VulnerabilityTechnique.CSPM
    if vuln.skims_method and (
        "terraform" in vuln.skims_method
        or "cloudformation" in vuln.skims_method
    ):
        convert_to = VulnerabilityTechnique.SAST
    return convert_to


async def process_group(
    loaders: Dataloaders,
    group_name: str,
) -> None:
    group_findings = await loaders.group_findings.load(group_name)

    vulns = await loaders.finding_vulnerabilities.load_many_chained(
        [fin.id for fin in group_findings]
    )

    machine_cloud_vulns = [
        vuln
        for vuln in vulns
        if (
            vuln.hacker_email == "machine@fluidattacks.com"
            or vuln.state.source == Source.MACHINE
        )
        and vuln.technique == VulnerabilityTechnique.CLOUD
    ]

    machine_apk_vulns = [
        vuln
        for vuln in vulns
        if (
            vuln.hacker_email == "machine@fluidattacks.com"
            or vuln.state.source == Source.MACHINE
        )
        and vuln.technique == VulnerabilityTechnique.SAST
        and vuln.skims_technique
        and vuln.skims_technique.lower() == "apk"
    ]

    if machine_cloud_vulns:
        await collect(
            tuple(
                vulns_model.update_metadata(
                    finding_id=vuln.finding_id,
                    vulnerability_id=vuln.id,
                    metadata=VulnerabilityMetadataToUpdate(
                        technique=get_technique(vuln)
                    ),
                )
                for vuln in machine_cloud_vulns
            ),
            workers=25,
        )

    if machine_apk_vulns:
        await collect(
            tuple(
                vulns_model.update_metadata(
                    finding_id=vuln.finding_id,
                    vulnerability_id=vuln.id,
                    metadata=VulnerabilityMetadataToUpdate(
                        technique=VulnerabilityTechnique.DAST
                    ),
                )
                for vuln in machine_apk_vulns
            ),
            workers=25,
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
