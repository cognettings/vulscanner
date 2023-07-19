# type: ignore

# pylint: disable=invalid-name
"""
This migration fixes inconsistencies for finding historic dates introduced at
move_root batch action.

First, the approval date not being consistent with vulns report date. Second,
dates being too close on time.

https://gitlab.com/fluidattacks/product/-/issues/6299

Execution Time:    2022-04-13 at 17:40:04 UTC
Finalization Time: 2022-04-13 at 17:43:11 UTC
"""

from aioextensions import (
    collect,
    run,
)
from custom_utils import (
    datetime as datetime_utils,
    vulnerabilities as vulns_utils,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model import (
    findings as findings_model,
)
from db_model.findings.types import (
    Finding,
    FindingState,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
import logging
from settings import (
    LOGGING,
)
import time
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


def adjust_historic_dates(
    historic: tuple[FindingState, ...],
) -> tuple[bool, tuple[FindingState, ...]]:
    has_historic_changed = False
    new_historic = list(historic[:1])
    comparison_date = historic[0].modified_date

    for entry in historic[1:]:
        current_date = entry.modified_date
        elapsed = current_date - comparison_date
        if current_date > comparison_date and elapsed.seconds >= 1:
            comparison_date = entry.modified_date
        else:
            comparison_date = comparison_date + timedelta(seconds=1)
            has_historic_changed = True
        new_historic.append(entry._replace(modified_date=comparison_date))

    return has_historic_changed, tuple(new_historic)


def get_oldest_vulnerability_report_date(
    vulns: tuple[Vulnerability, ...],
) -> datetime:
    report_dates = vulns_utils.get_report_dates(vulns)
    return min(report_dates)


def replace_finding_historic_dates(
    *,
    historic_state: tuple[FindingState, ...],
    vulns_oldest_report_date: datetime,
) -> tuple[FindingState, ...]:
    base_date = vulns_oldest_report_date - timedelta(
        seconds=len(historic_state)
    )
    return tuple(
        state._replace(
            modified_date=datetime_utils.get_as_utc_iso_format(base_date),
        )
        for state in historic_state
    )


async def process_finding(
    *,
    loaders: Dataloaders,
    finding: Finding,
) -> None:
    historic_state = await loaders.finding_historic_state.load(finding.id)

    has_report_date_changed = False
    vulns = await loaders.finding_vulnerabilities_released_nzr.load(finding.id)
    if vulns:
        vulns_oldest_report_date = get_oldest_vulnerability_report_date(
            tuple(vulns)
        )
        finding_approval_date = finding.approval.modified_date
        if vulns_oldest_report_date < finding_approval_date:
            historic_state = replace_finding_historic_dates(
                historic_state=historic_state,
                vulns_oldest_report_date=vulns_oldest_report_date,
            )
            has_report_date_changed = True

    has_historic_changed, new_historic_state = adjust_historic_dates(
        historic_state
    )

    if has_report_date_changed or has_historic_changed:
        await findings_model.update_historic_state(
            group_name=finding.group_name,
            finding_id=finding.id,
            historic_state=new_historic_state,
        )
    await update_unreliable_indicators_by_deps(
        EntityDependency.move_root,
        finding_ids=[finding.id],
        vulnerability_ids=[],
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    finding_ids: list[str] = []  # Masked
    findings = await loaders.finding.load_many(finding_ids)
    await collect(
        process_finding(
            loaders=loaders,
            finding=finding,
        )
        for finding in findings
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
