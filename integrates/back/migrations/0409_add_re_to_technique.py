# pylint: disable=invalid-name
"""
Update the 'technique' field for some vulnerabilities.

MPT with type = LINES -> SCR.
MPT with type INPUTS and specific to set to an exec -> RE.

Execution Time:    2023-06-28 at 20:13:00 UTC
Finalization Time: 2023-06-28 at 20:33:52 UTC

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
from vulnerabilities.domain.utils import (
    is_executable,
)


def get_technique(vuln: Vulnerability) -> VulnerabilityTechnique:
    convert_to = VulnerabilityTechnique.MPT
    if vuln.type == VulnerabilityType.LINES:
        convert_to = VulnerabilityTechnique.SCR
    elif vuln.type == VulnerabilityType.INPUTS and is_executable(
        vuln.state.specific
    ):
        convert_to = VulnerabilityTechnique.RE
    return convert_to


async def process_group(
    loaders: Dataloaders,
    group_name: str,
) -> None:
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
    ]

    if non_machine_vulns:
        await collect(
            tuple(
                vulns_model.update_metadata(
                    finding_id=vuln.finding_id,
                    vulnerability_id=vuln.id,
                    metadata=VulnerabilityMetadataToUpdate(
                        technique=get_technique(vuln)
                    ),
                )
                for vuln in non_machine_vulns
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
