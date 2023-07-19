# pylint: disable=invalid-name
"""
Populate the advisor data in new fields in vulnerability.

Start Time:    2023-06-16 at 16:56:18 UTC
Finalization Time: 2023-06-16 at 17:15:47 UTC

"""

from aioextensions import (
    collect,
    run,
)
from custom_exceptions import (
    GroupNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    Source,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityAdvisory,
)
from db_model.vulnerabilities.update import (
    update_historic_entry,
)
import logging
import logging.config
from organizations.domain import (
    get_all_group_names,
)
import re
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_vulnerability_where(vulnerability: Vulnerability) -> bool:
    pattern = r"^(.*?)\s*\(([^)]*) v(.[\d.]+)[^)]*\)\s*\[(.*?)\]$"
    match = re.search(pattern, vulnerability.state.where)
    if not match:
        return False

    result = (
        match.group(1),
        match.group(2),
        match.group(3),
        match.group(4).split(","),
    )

    vulnerability_advisory = vulnerability.state._replace(
        advisories=VulnerabilityAdvisory(
            package=result[1],
            vulnerable_version=result[2],
            cve=result[3],
        )
    )
    await update_historic_entry(
        current_value=vulnerability,
        finding_id=vulnerability.finding_id,
        entry=vulnerability_advisory,
        vulnerability_id=vulnerability.id,
        force_update=True,
    )
    return True


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    group = await loaders.group.load(group_name)
    if not group:
        raise GroupNotFound()
    group_findings = await loaders.group_findings_all.load(group_name)
    findings_filtered = [
        finding
        for finding in group_findings
        if finding.state.status
        and any(finding.title.startswith(code) for code in ["011", "393"])
    ]

    if not findings_filtered:
        return
    group_vulns = await loaders.finding_vulnerabilities_all.load_many_chained(
        [finding.id for finding in findings_filtered]
    )
    machine_vulns = [
        vuln for vuln in group_vulns if vuln.state.source == Source.MACHINE
    ]

    await collect(
        tuple(process_vulnerability_where(vuln) for vuln in machine_vulns),
        workers=16,
    )
    print(f"Group processed {group_name} {str(round(progress, 2))}")


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(await get_all_group_names(loaders=loaders))
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
        workers=8,
    )


if __name__ == "__main__":
    execution_time = time.strftime("Start Time:    %Y-%m-%d at %H:%M:%S UTC")
    print(execution_time)
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
