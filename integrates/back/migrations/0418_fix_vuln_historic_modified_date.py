# pylint: disable=invalid-name
"""
Fix offset-naive datetime in vulnerability historic state.

Execution Time:    2023-07-17 at 19:42:37 UTC
Finalization Time: 2023-07-17 at 23:09:19 UTC
"""
from aioextensions import (
    collect,
    run,
)
from botocore.exceptions import (
    ConnectTimeoutError,
    ReadTimeoutError,
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
)
from decorators import (
    retry_on_exceptions,
)
from itertools import (
    chain,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
import pytz
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


def _is_timezone_aware(_datetime: datetime) -> bool:
    return (
        _datetime.tzinfo is not None
        and _datetime.tzinfo.utcoffset(_datetime) is not None
    )


def _make_timezone_aware(naive_datetime: datetime) -> datetime:
    return pytz.timezone("UTC").localize(naive_datetime, is_dst=False)


@retry_on_exceptions(
    exceptions=(ReadTimeoutError, ConnectTimeoutError),
    sleep_seconds=3,
)
async def _process_vuln(
    loaders: Dataloaders,
    vuln: Vulnerability,
) -> None:
    historic_state = await loaders.vulnerability_historic_state.load(vuln.id)

    are_timezone_aware = [
        _is_timezone_aware(entry.modified_date) for entry in historic_state
    ]
    fixed_historic_state = tuple(
        entry
        if is_tz_aware
        else entry._replace(
            modified_date=_make_timezone_aware(entry.modified_date)
        )
        for entry, is_tz_aware in zip(historic_state, are_timezone_aware)
    )

    if not all(are_timezone_aware):
        await vulns_model.update_historic(
            current_value=vuln, historic=fixed_historic_state
        )


async def _get_finding_vulnerabilities(
    loaders: Dataloaders, finding: Finding
) -> list[Vulnerability]:
    return await loaders.finding_vulnerabilities_all.load(finding.id)


@retry_on_exceptions(
    exceptions=(ReadTimeoutError, ConnectTimeoutError),
    sleep_seconds=3,
)
async def _process_group(
    loaders: Dataloaders,
    group_name: str,
) -> None:
    findings = await loaders.group_findings_all.load(group_name)
    group_vulns = list(
        chain.from_iterable(
            await collect(
                tuple(
                    _get_finding_vulnerabilities(
                        loaders=loaders,
                        finding=finding,
                    )
                    for finding in findings
                ),
                workers=500,
            )
        )
    )
    await collect(
        tuple(
            _process_vuln(loaders=loaders, vuln=vuln) for vuln in group_vulns
        ),
        workers=500,
    )
    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "findings": len(findings),
                "vulnerabilities": len(group_vulns),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    all_group_names = sorted(
        await orgs_domain.get_all_group_names(loaders=loaders)
    )
    count = 0
    LOGGER_CONSOLE.info(
        "All groups",
        extra={
            "extra": {
                "len": len(all_group_names),
            }
        },
    )
    for group_name in all_group_names:
        count += 1
        LOGGER_CONSOLE.info(
            "Group processed",
            extra={
                "extra": {
                    "group_name": group_name,
                    "count": count,
                }
            },
        )
        await _process_group(loaders, group_name)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
