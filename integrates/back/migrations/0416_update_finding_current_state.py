# pylint: disable=invalid-name
"""
Update the current state of the findings in every group.
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
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
    FindingState,
)
import logging
import logging.config
from organizations.domain import (
    get_all_group_names,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def _update_to(finding: Finding, new_status: FindingStateStatus) -> None:
    new_state: FindingState = FindingState(
        status=new_status,
        modified_by=finding.state.modified_by,
        modified_date=finding.state.modified_date,
        source=finding.state.source,
        rejection=finding.state.rejection,
        justification=finding.state.justification,
    )

    await findings_model.update_state(
        current_value=finding.state,
        group_name=finding.group_name,
        finding_id=finding.id,
        state=new_state,
    )


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    count: int,
    total: int,
) -> None:
    group_findings = await loaders.group_findings.load(group_name)
    if not group_findings:
        return

    to_deleted = [
        FindingStateStatus.DELETED,
        FindingStateStatus.REJECTED,
    ]
    to_masked = [
        FindingStateStatus.MASKED,
    ]

    start = time.time()
    await collect(
        tuple(
            _update_to(finding, FindingStateStatus.DELETED)
            if finding.state.status in to_deleted
            else _update_to(finding, FindingStateStatus.MASKED)
            if finding.state.status in to_masked
            else _update_to(finding, FindingStateStatus.CREATED)
            for finding in group_findings
        ),
    )
    end = time.time()

    LOGGER_CONSOLE.info(
        "[%s] %s processed in %s (Findings: %s)",
        f"{count / total * 100:.2f} %",
        group_name,
        f"{(end - start) * 1000:.2f} ms",
        len(group_findings),
    )


async def get_groups(loaders: Dataloaders) -> list[str]:
    groups = sorted(await get_all_group_names(loaders))

    # According to the time of the day, it will skip some groups
    letters = ["abcdefg", "hijklmn", "opqrst", "uvwxyz"]
    hour: int = int(time.strftime("%H"))
    if 10 <= hour < 17:
        letters.pop(0)
    elif 17 <= hour < 20:
        letters.pop(1)
    elif 20 <= hour < 23:
        letters.pop(2)
    else:
        letters.pop(3)

    forbidden_letters = "".join(letters)
    LOGGER_CONSOLE.info("At %s...", hour)

    groups = [g for g in groups if g[0].lower() not in forbidden_letters]

    return groups


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = await get_groups(loaders=loaders)

    LOGGER_CONSOLE.info("Processing %s groups...", len(group_names))
    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group,
                count=count + 1,
                total=len(group_names),
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
    LOGGER_CONSOLE.info("\n%s\n%s", execution_time, finalization_time)
