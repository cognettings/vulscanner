# pylint: disable=invalid-name
"""
Populate the 'technique' field for all vulnerabilities.
This field indicates the technique
for each vulnerability based on specific rules.

Vulnerabilities discovered by hackers (not Machine)
should be labeled as 'MPT' (Manual Penetration Testing).

The current type 'LINES' should populate `technique`
to one of the following types: 'SAST' | 'SCA' | 'CLOUD'.

The current type 'INPUTS' should populate `technique`
to one of the following types: 'CLOUD' | 'DAST'.
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
from db_model import (
    vulnerabilities as vulns_model,
)
from db_model.enums import (
    Source,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityTechnique,
    VulnerabilityType,
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
    if vuln.type == VulnerabilityType.LINES:
        convert_to = VulnerabilityTechnique.SAST
        if vuln.skims_technique and vuln.skims_technique.lower() == "sca":
            convert_to = VulnerabilityTechnique.SCA
        elif vuln.skims_method and (
            "terraform" in vuln.skims_method
            or "cloudformation" in vuln.skims_method
        ):
            convert_to = VulnerabilityTechnique.CLOUD
    else:
        convert_to = VulnerabilityTechnique.DAST
        if vuln.skims_method and "aws" in vuln.skims_method:
            convert_to = VulnerabilityTechnique.CLOUD

    return convert_to


async def process_group(
    loaders: Dataloaders,
    group_name: str,
) -> None:
    csv_vulns = []
    group_findings = await loaders.group_findings.load(group_name)

    vulns = await loaders.finding_vulnerabilities.load_many_chained(
        [fin.id for fin in group_findings]
    )

    non_machine_vulns = [
        vuln
        for vuln in vulns
        if not (
            vuln.hacker_email == "machine@fluidattacks.com"
            or vuln.state.source == Source.MACHINE
        )
        and not vuln.technique
    ]

    machine_vulns = [
        vuln
        for vuln in vulns
        if (
            vuln.hacker_email == "machine@fluidattacks.com"
            or vuln.state.source == Source.MACHINE
        )
        and not vuln.technique
    ]

    if machine_vulns:
        await collect(
            vulns_model.update_metadata(
                finding_id=vuln.finding_id,
                vulnerability_id=vuln.id,
                metadata=VulnerabilityMetadataToUpdate(
                    technique=get_technique(vuln)
                ),
            )
            for vuln in machine_vulns
        )

        csv_vulns.extend(
            [
                [
                    vuln.group_name,
                    vuln.id,
                    "Machine",
                    vuln.technique,
                    get_technique(vuln),
                ]
                for vuln in machine_vulns
            ]
        )

    if non_machine_vulns:
        await collect(
            vulns_model.update_metadata(
                finding_id=vuln.finding_id,
                vulnerability_id=vuln.id,
                metadata=VulnerabilityMetadataToUpdate(
                    technique=VulnerabilityTechnique.MPT
                ),
            )
            for vuln in non_machine_vulns
        )
        csv_vulns.extend(
            [
                [
                    vuln.group_name,
                    vuln.id,
                    vuln.hacker_email,
                    vuln.technique,
                    VulnerabilityTechnique.MPT,
                ]
                for vuln in non_machine_vulns
            ]
        )

    with open("vulns_modified.csv", "a+", encoding="utf-8") as handler:
        writer = csv.writer(handler)
        writer.writerows(csv_vulns)

    print(f"Group processed {group_name}")


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = sorted(await get_all_group_names(loaders))
    await collect(
        [process_group(loaders, group) for group in groups], workers=15
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
