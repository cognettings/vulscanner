# pylint: disable=invalid-name
"""
Update the indicators of the findings in every group.

Execution Time:     2023-07-13 at 20:04:56 UTC
Finalization Time:  2023-07-13 at 20:17:06 UTC
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
    FindingTreatmentSummary,
    FindingUnreliableIndicatorsToUpdate,
)
from findings import (
    domain as findings_domain,
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
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    _format_unreliable_status,
    update_unreliable_indicators_by_deps,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def update_old_indicators(findings: list[str]) -> None:
    return await update_unreliable_indicators_by_deps(
        EntityDependency.remove_vulnerability, finding_ids=findings
    )


async def process_finding(loaders: Dataloaders, finding: Finding) -> None:
    status = await findings_domain.get_status(loaders, finding.id)
    open_vulns = await findings_domain.get_open_vulnerabilities_len(
        loaders, finding.id
    )
    closed_vulns = await findings_domain.get_closed_vulnerabilities_len(
        loaders, finding.id
    )
    submitted_vulns = await findings_domain.get_submitted_vulnerabilities(
        loaders, finding.id
    )
    rejected_vulns = await findings_domain.get_rejected_vulnerabilities(
        loaders, finding.id
    )
    max_open_severity_score = (
        await findings_domain.get_max_open_severity_score(loaders, finding.id)
    )
    newest_report_date = (
        await findings_domain.get_newest_vulnerability_report_date(
            loaders, finding.id
        )
    )
    oldest_report_date = (
        await findings_domain.get_oldest_vulnerability_report_date(
            loaders, finding.id
        )
    )
    treatment_summary = await findings_domain.get_treatment_summary(
        loaders, finding.id
    )

    await findings_model.update_unreliable_indicators(
        current_value=finding.unreliable_indicators,
        group_name=finding.group_name,
        finding_id=finding.id,
        indicators=FindingUnreliableIndicatorsToUpdate(
            unreliable_newest_vulnerability_report_date=newest_report_date,
            unreliable_status=_format_unreliable_status(status),
            open_vulnerabilities=open_vulns,
            closed_vulnerabilities=closed_vulns,
            submitted_vulnerabilities=submitted_vulns,
            rejected_vulnerabilities=rejected_vulns,
            max_open_severity_score=max_open_severity_score,
            oldest_vulnerability_report_date=oldest_report_date,
            treatment_summary=FindingTreatmentSummary(
                untreated=treatment_summary.untreated,
                in_progress=treatment_summary.in_progress,
                accepted=treatment_summary.accepted,
                accepted_undefined=treatment_summary.accepted_undefined,
            ),
            newest_vulnerability_report_date=newest_report_date,
        ),
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

    start = time.time()
    await collect(
        tuple(
            process_finding(loaders=loaders, finding=finding)
            for finding in group_findings
        ),
    )
    await update_old_indicators([finding.id for finding in group_findings])
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
    minutes: int = int(time.strftime("%M"))
    if hour % 2 == 0:
        letters.pop(0 if minutes < 30 else 1)
    else:
        letters.pop(2 if minutes < 30 else 3)

    forbidden_letters = "".join(letters)
    LOGGER_CONSOLE.info("At %s:%s...", hour, minutes)

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
