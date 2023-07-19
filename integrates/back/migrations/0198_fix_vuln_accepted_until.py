# type: ignore

# pylint: disable=invalid-name,unexpected-keyword-arg,missing-kwoa
"""
Search inside vulns' historic treatment for ACCEPTED states with
"accepted_until" date inferior to "modified_date", according to validations
at mutation "update_vulnerabilities_treatment".

Swap these found dates and update vuln's historic.

Execution Time:     2022-02-28 at 17:19:07 UTC
Finalization Time:  2022-02-28 at 20:15:08 UTC
"""

from aioextensions import (
    collect,
    run,
)
from custom_utils import (
    datetime as datetime_utils,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import db_model.vulnerabilities as vulns_model
from db_model.vulnerabilities.enums import (
    VulnerabilityTreatmentStatus,
)
from decimal import (
    Decimal,
)
import groups.domain as groups_domain
import logging
import logging.config
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_vuln(
    *,
    loaders: Dataloaders,
    finding_id: str,
    vuln_id: str,
) -> None:
    historic_treatment = await loaders.vulnerability_historic_treatment.load(
        vuln_id
    )
    is_to_be_updated = False
    fixed_historic = []
    for treatment in historic_treatment:
        accepted_until = treatment.accepted_until
        modified_date = treatment.modified_date
        if (
            treatment.status == VulnerabilityTreatmentStatus.ACCEPTED
            and treatment.accepted_until
        ):
            acceptance_days = Decimal(
                (
                    datetime_utils.get_datetime_from_iso_str(accepted_until)
                    - datetime_utils.get_datetime_from_iso_str(modified_date)
                ).days
            )
            if acceptance_days < 0:
                accepted_until = treatment.modified_date
                modified_date = treatment.accepted_until
                is_to_be_updated = True
        fixed_historic.append(
            treatment._replace(
                accepted_until=accepted_until,
                modified_date=modified_date,
            )
        )
    if is_to_be_updated:
        await vulns_model.update_historic(
            finding_id=finding_id,
            historic=fixed_historic,
            vulnerability_id=vuln_id,
        )


async def process_finding(
    *,
    loaders: Dataloaders,
    finding_id: str,
) -> None:
    vulns = await loaders.finding_vulnerabilities.load(finding_id)
    await collect(
        tuple(
            process_vuln(
                loaders=loaders,
                finding_id=finding_id,
                vuln_id=vuln_id,
            )
            for vuln_id in [vuln.id for vuln in vulns]
        ),
        workers=4,
    )


async def process_group(
    *,
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    findings = await loaders.group_findings.load(group_name)
    await collect(
        tuple(
            process_finding(
                loaders=loaders,
                finding_id=finding_id,
            )
            for finding_id in [finding.id for finding in findings]
        ),
        workers=4,
    )
    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(await groups_domain.get_active_groups())
    group_names_len = len(group_names)
    LOGGER_CONSOLE.info(
        "All groups",
        extra={
            "extra": {
                "group_names_len": group_names_len,
            }
        },
    )
    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group_name,
                progress=count / group_names_len,
            )
            for count, group_name in enumerate(group_names)
        ),
        workers=8,
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
