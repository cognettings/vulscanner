# pylint: disable=invalid-name
"""
Update the indicator of finding status

Execution Time:    2023-04-18 at 16:55:04 UTC
Finalization Time: 2023-04-18 at 17:25:11 UTC
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
from unreliable_indicators.operations import (
    _format_unreliable_status,
)


async def process_finding(loaders: Dataloaders, finding: Finding) -> None:
    status = await findings_domain.get_status(loaders, finding.id)
    await findings_model.update_unreliable_indicators(
        current_value=finding.unreliable_indicators,
        group_name=finding.group_name,
        finding_id=finding.id,
        indicators=FindingUnreliableIndicatorsToUpdate(
            unreliable_status=_format_unreliable_status(status)
        ),
    )


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    count: int,
) -> None:
    group_findings = await loaders.group_findings_all.load(group_name)
    if not group_findings:
        return

    await collect(
        tuple(
            process_finding(loaders=loaders, finding=finding)
            for finding in group_findings
        ),
    )
    print(f"Group processed {group_name} {count}")


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
                count=count + 1,
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
