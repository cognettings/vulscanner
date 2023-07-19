# pylint: disable=invalid-name
"""
Populate the finding indicator with the vulnerability drafts information.

Execution Time:    2023-05-03 at 18:54:39 UTC
Finalization Time: 2023-05-03 at 19:06:34 UTC
Execution Time:    2023-05-04 at 19:20:37 UTC
Finalization Time: 2023-05-04 at 19:30:35 UTC
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
    findings as findings_model,
)
from db_model.findings.types import (
    Finding,
    FindingUnreliableIndicatorsToUpdate,
)
from findings import (
    domain as findings_domain,
)
from organizations.domain import (
    get_all_group_names,
)
import time


async def process_finding(loaders: Dataloaders, finding: Finding) -> None:
    rejected_vulnerabilities = (
        await findings_domain.get_rejected_vulnerabilities(loaders, finding.id)
    )
    submitted_vulnerabilities = (
        await findings_domain.get_submitted_vulnerabilities(
            loaders, finding.id
        )
    )
    await findings_model.update_unreliable_indicators(
        current_value=finding.unreliable_indicators,
        group_name=finding.group_name,
        finding_id=finding.id,
        indicators=FindingUnreliableIndicatorsToUpdate(
            unreliable_rejected_vulnerabilities=rejected_vulnerabilities,
            unreliable_submitted_vulnerabilities=submitted_vulnerabilities,
        ),
    )


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    group_findings = await loaders.group_findings_all.load(group_name)
    if not group_findings:
        return

    await collect(
        tuple(
            process_finding(loaders=loaders, finding=finding)
            for finding in group_findings
        ),
        workers=500,
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
        workers=1,
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
