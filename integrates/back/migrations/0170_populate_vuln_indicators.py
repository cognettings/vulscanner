# type: ignore

# pylint: disable=invalid-name
"""
Populate the vulnerability indicators.

Execution Time: 2022-01-24 at 14:11:40 UTC
Finalization Time: 2022-01-24 at 23:48:47 UTC
"""

from aioextensions import (
    collect,
    run,
)
from aiohttp import (
    ClientConnectorError,
)
from botocore.exceptions import (
    HTTPClientError,
)
from custom_exceptions import (
    IndicatorAlreadyUpdated,
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
)
from db_model import (
    vulnerabilities as vulns_model,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityUnreliableIndicatorsToUpdate,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from groups.dal import (  # pylint: disable=import-error
    get_all as get_all_groups,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
import time
from unreliable_indicators.enums import (
    EntityAttr,
)
from vulnerabilities import (
    domain as vulns_domain,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


def _format_datetime_iso_format(
    optional_datetime: datetime | None,
) -> str | None:
    unreliable_datetime = None
    if optional_datetime:
        unreliable_datetime = datetime_utils.get_as_utc_iso_format(
            optional_datetime
        )
    return unreliable_datetime


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
)
async def populate_indicators_by_vuln(
    loaders: Dataloaders,
    vulnerability: Vulnerability,
) -> None:
    indicators = {}

    indicators[EntityAttr.efficacy] = vulns_domain.get_efficacy(
        loaders, vulnerability
    )
    indicators[
        EntityAttr.last_reattack_date
    ] = vulns_domain.get_last_reattack_date(loaders, vulnerability)
    indicators[
        EntityAttr.last_reattack_requester
    ] = vulns_domain.get_reattack_requester(loaders, vulnerability)
    indicators[
        EntityAttr.last_requested_reattack_date
    ] = vulns_domain.get_last_requested_reattack_date(loaders, vulnerability)
    indicators[EntityAttr.reattack_cycles] = vulns_domain.get_reattack_cycles(
        loaders, vulnerability
    )
    indicators[
        EntityAttr.treatment_changes
    ] = vulns_domain.get_treatment_changes(loaders, vulnerability)
    indicators[EntityAttr.report_date] = vulns_utils.get_report_date(
        loaders, vulnerability
    )
    indicators[EntityAttr.source] = vulns_utils.get_source(
        loaders, vulnerability
    )

    result = dict(zip(indicators.keys(), await collect(indicators.values())))
    current_indicators = vulnerability.unreliable_indicators
    if (
        result.get(EntityAttr.efficacy),
        result.get(EntityAttr.last_reattack_date),
        result.get(EntityAttr.last_reattack_requester),
        result.get(EntityAttr.last_requested_reattack_date),
        result.get(EntityAttr.reattack_cycles),
        result.get(EntityAttr.treatment_changes),
        _format_datetime_iso_format(result.get(EntityAttr.report_date)),
        result.get(EntityAttr.source),
    ) != (
        current_indicators.unreliable_efficacy,
        current_indicators.unreliable_last_reattack_date,
        current_indicators.unreliable_last_reattack_requester,
        current_indicators.unreliable_last_requested_reattack_date,
        current_indicators.unreliable_reattack_cycles,
        current_indicators.unreliable_treatment_changes,
        current_indicators.unreliable_report_date,
        current_indicators.unreliable_source,
    ):
        indicators = VulnerabilityUnreliableIndicatorsToUpdate(
            unreliable_efficacy=result.get(EntityAttr.efficacy),
            unreliable_last_reattack_date=result.get(
                EntityAttr.last_reattack_date
            ),
            unreliable_last_reattack_requester=result.get(
                EntityAttr.last_reattack_requester
            ),
            unreliable_last_requested_reattack_date=result.get(
                EntityAttr.last_requested_reattack_date
            ),
            unreliable_reattack_cycles=result.get(EntityAttr.reattack_cycles),
            unreliable_treatment_changes=result.get(
                EntityAttr.treatment_changes
            ),
            unreliable_report_date=_format_datetime_iso_format(
                result.get(EntityAttr.report_date)
            ),
            unreliable_source=result.get(EntityAttr.source),
        )
        await vulns_model.update_unreliable_indicators(
            current_value=vulnerability,
            indicators=indicators,
        )


@retry_on_exceptions(
    exceptions=(
        IndicatorAlreadyUpdated,
        ClientConnectorError,
    ),
)
async def populate_indicators_by_finding(finding: Finding) -> None:
    loaders = get_new_context()
    vulnerabilities = await loaders.finding_vulnerabilities_all.load(
        finding.id
    )
    await collect(
        tuple(
            populate_indicators_by_vuln(
                loaders=loaders, vulnerability=vulnerability
            )
            for vulnerability in vulnerabilities
        ),
        workers=200,
    )


@retry_on_exceptions(
    exceptions=(HTTPClientError,),
    sleep_seconds=10,
)
async def populate_indicators_by_group(
    loaders: Dataloaders, group_name: str, progress: float
) -> None:
    group_drafts_and_findings = await loaders.group_drafts_and_findings.load(
        group_name
    )
    group_removed_findings: tuple[
        Finding, ...
    ] = await loaders.group_removed_findings.load(group_name)
    all_findings = group_drafts_and_findings + group_removed_findings
    await collect(
        tuple(
            populate_indicators_by_finding(finding=finding)
            for finding in all_findings
        ),
        workers=5,
    )
    LOGGER_CONSOLE.info(
        "Group updated",
        extra={
            "extra": {
                "group_name": group_name,
                "progress": str(progress),
            }
        },
    )


async def main() -> None:
    groups = await get_all_groups(data_attr="project_name")
    loaders = get_new_context()
    groups_len = len(groups)
    await collect(
        tuple(
            populate_indicators_by_group(
                loaders=loaders,
                group_name=group["project_name"],
                progress=count / groups_len,
            )
            for count, group in enumerate(groups)
        ),
        workers=4,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
