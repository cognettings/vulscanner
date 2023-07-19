# pylint: disable=invalid-name

"""
Search and update safe location with requested verification
Start Time:        2023-06-23 at 03:30:45 UTC
Finalization Time: 2023-06-23 at 04:07:53 UTC
"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityVerification,
)
from db_model.vulnerabilities.update import (
    update_historic_entry,
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

# Constants
LOGGER_CONSOLE = logging.getLogger("console")


async def process_location(vulnerability: Vulnerability) -> None:
    if vulnerability.state.status is not VulnerabilityStateStatus.SAFE:
        return

    if vulnerability.verification is None:
        return

    if (
        vulnerability.verification.status
        is not VulnerabilityVerificationStatus.REQUESTED
    ):
        return

    LOGGER_CONSOLE.info(
        "Location processed",
        extra={
            "extra": {
                "vulnerability": vulnerability.id,
                "modified date": vulnerability.state.modified_date.isoformat(),
                "status": vulnerability.state.status.value,
                "verification": vulnerability.verification.status.value,
            }
        },
    )
    await update_historic_entry(
        current_value=vulnerability,
        finding_id=vulnerability.finding_id,
        vulnerability_id=vulnerability.id,
        entry=VulnerabilityVerification(
            modified_date=vulnerability.state.modified_date,
            status=VulnerabilityVerificationStatus.VERIFIED,
        ),
    )


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    group_findings = await loaders.group_findings_all.load(group_name)
    group_vulns = await loaders.finding_vulnerabilities_all.load_many_chained(
        [finding.id for finding in group_findings]
    )
    await collect(
        tuple(process_location(vuln) for vuln in group_vulns),
        workers=32,
    )
    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group name": group_name,
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(await get_all_group_names(loaders=loaders))
    LOGGER_CONSOLE.info(
        "All groups",
        extra={"extra": {"groups_len": len(group_names)}},
    )
    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group,
                progress=count / len(group_names),
            )
            for count, group in enumerate(group_names)
        ),
        workers=2,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Start Time:        %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    LOGGER_CONSOLE.info("\n%s\n%s", execution_time, finalization_time)
