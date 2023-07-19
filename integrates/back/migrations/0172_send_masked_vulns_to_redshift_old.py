# type: ignore

# pylint: disable=invalid-name
"""
Search for vulns in previous table "FI_vulnerabilities"
that belong to already removed groups. These vulns were not
part of the vuln migration to single table.

Store them in redshift.

Execution Time:     2022-01-27 at 20:00:40 UTC
Finalization Time:  2022-01-28 at 02:49:27 UTC

Execution Time:     2022-01-28 at 20:43:20 UTC
Finalization Time:  2022-01-28 at 21:51:09 UTC

"""

from aioextensions import (
    collect,
    run,
)
from aiohttp import (
    ClientConnectorError,
)
from aiohttp.client_exceptions import (
    ClientPayloadError,
    ServerTimeoutError,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from botocore.exceptions import (
    ClientError,
    HTTPClientError,
)
from class_types.types import (
    Item,
)
from custom_exceptions import (
    UnavailabilityError as CustomUnavailabilityError,
)
from custom_utils.vulnerabilities import (
    format_vulnerability,
    format_vulnerability_state,
    format_vulnerability_treatment,
    format_vulnerability_verification,
    format_vulnerability_zero_risk,
    get_optional,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from db_model.vulnerabilities.utils import (
    adjust_historic_dates,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from groups import (
    dal as groups_dal,
)
from itertools import (
    chain,
)
import logging
import logging.config
from redshift.vulnerabilities import (  # pylint: disable=import-error
    insert_batch_metadata,
    insert_batch_state,
    insert_batch_treatment,
    insert_batch_verification,
    insert_batch_zero_risk,
)
from settings import (
    LOGGING,
)
import time
from vulnerabilities import (
    dal as vulns_dal,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def send_vulns_to_redshift(
    *,
    vulns_metadata: tuple[Vulnerability, ...],
    vulns_state: tuple[tuple[VulnerabilityState, ...], ...],
    vulns_treatment: tuple[tuple[VulnerabilityTreatment, ...], ...],
    vulns_verification: tuple[tuple[VulnerabilityVerification, ...], ...],
    vulns_zero_risk: tuple[tuple[VulnerabilityZeroRisk, ...], ...],
) -> None:
    vulns_id = tuple(vuln.id for vuln in vulns_metadata)
    await insert_batch_metadata(
        vulnerabilities=vulns_metadata,
    )
    await collect(
        (
            insert_batch_state(
                vulnerability_ids=vulns_id,
                historics=vulns_state,
            ),
            insert_batch_treatment(
                vulnerability_ids=vulns_id,
                historics=vulns_treatment,
            ),
            insert_batch_verification(
                vulnerability_ids=vulns_id,
                historics=vulns_verification,
            ),
            insert_batch_zero_risk(
                vulnerability_ids=vulns_id,
                historics=vulns_zero_risk,
            ),
        )
    )


def _check_vuln_item_state(vuln: Item) -> bool:
    last_state: dict[str, str] = vuln["historic_state"][-1]
    state_status = str(last_state["state"]).upper()
    if state_status != "DELETED":
        return True

    modified_by = last_state.get("analyst") or last_state.get("hacker") or ""
    if (
        state_status == "DELETED"
        and "@fluid" not in modified_by
        and "@kernelship" not in modified_by
    ):
        return True

    return False


def _filter_out_deleted_vulns(
    vulns: list[Item],
) -> list[Item]:
    return [vuln for vuln in vulns if _check_vuln_item_state(vuln)]


async def _get_vulnerabilities_by_finding(finding_id: str) -> list[Item]:
    items: list[Item] = await vulns_dal.get_by_finding(finding_id=finding_id)
    return items


def _format_metadata(
    vulns_items: list[Item],
) -> tuple[Vulnerability, ...]:
    return tuple(format_vulnerability(item=item) for item in vulns_items)


def _format_state(
    vulns_items: list[Item],
) -> tuple[tuple[VulnerabilityState, ...], ...]:
    return tuple(
        adjust_historic_dates(
            tuple(
                format_vulnerability_state(state)
                for state in vulnerability["historic_state"]
            )
        )
        for vulnerability in vulns_items
    )


def _format_treatment(
    vulns_items: list[Item],
) -> tuple[tuple[VulnerabilityTreatment, ...], ...]:
    return tuple(
        adjust_historic_dates(
            tuple(
                format_vulnerability_treatment(
                    treatment, vulnerability["historic_state"][0]["date"]
                )
                for treatment in get_optional(
                    "historic_treatment", vulnerability, tuple()
                )
            )
        )
        for vulnerability in vulns_items
    )


def _format_verification(
    vulns_items: list[Item],
) -> tuple[tuple[VulnerabilityVerification, ...], ...]:
    return tuple(
        adjust_historic_dates(
            tuple(
                format_vulnerability_verification(verification)
                for verification in get_optional(
                    "historic_verification", vulnerability, tuple()
                )
            )
        )
        for vulnerability in vulns_items
    )


def _format_zero_risk(
    vulns_items: list[Item],
) -> tuple[tuple[VulnerabilityZeroRisk, ...], ...]:
    return tuple(
        adjust_historic_dates(
            tuple(
                format_vulnerability_zero_risk(zero_risk)
                for zero_risk in get_optional(
                    "historic_zero_risk", vulnerability, tuple()
                )
            )
        )
        for vulnerability in vulns_items
    )


@retry_on_exceptions(
    exceptions=(
        ClientError,
        ClientPayloadError,
        CustomUnavailabilityError,
        UnavailabilityError,
    ),
    sleep_seconds=10,
)
async def process_finding(
    *,
    finding: Finding,
) -> list[Item]:
    # Only vulns for released findings will be stored
    if finding.state.status not in {
        FindingStateStatus.APPROVED,
        FindingStateStatus.DELETED,
    }:
        return []

    # Retrieve vulns as dict from old table
    vulns_items = await _get_vulnerabilities_by_finding(finding_id=finding.id)
    if not vulns_items:
        return []

    # Only deleted vulns by external users will be stored
    vulns_items_to_store = _filter_out_deleted_vulns(vulns_items)
    if not vulns_items_to_store:
        return []

    return vulns_items_to_store


@retry_on_exceptions(
    exceptions=(
        ClientConnectorError,
        ClientError,
        CustomUnavailabilityError,
        HTTPClientError,
        ServerTimeoutError,
        UnavailabilityError,
    ),
    sleep_seconds=10,
)
async def process_group(
    *,
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    group_findings = await loaders.group_findings.load(group_name)
    group_removed_findings = await loaders.group_removed_findings.load(
        group_name
    )
    all_findings = group_findings + group_removed_findings
    vulns_items_to_store: list[Item] = list(
        chain.from_iterable(
            await collect(
                tuple(
                    process_finding(finding=finding)
                    for finding in all_findings
                ),
                workers=64,
            )
        )
    )
    try:
        # Format vulns as typed
        vulns_metadata = _format_metadata(vulns_items_to_store)
        vulns_state = _format_state(vulns_items_to_store)
        vulns_treatment = _format_treatment(vulns_items_to_store)
        vulns_verification = _format_verification(vulns_items_to_store)
        vulns_zero_risk = _format_zero_risk(vulns_items_to_store)
    except IndexError as ex:
        LOGGER_CONSOLE.error(
            "Formatting error at vulns",
            extra={
                "extra": {
                    "group_name": group_name,
                    "ex": ex,
                }
            },
        )
        return

    await send_vulns_to_redshift(
        vulns_metadata=vulns_metadata,
        vulns_state=vulns_state,
        vulns_treatment=vulns_treatment,
        vulns_verification=vulns_verification,
        vulns_zero_risk=vulns_zero_risk,
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


async def get_removed_groups() -> list[str]:
    filtering_exp = Attr("project_status").eq("DELETED") | Attr(
        "project_status"
    ).eq("FINISHED")
    return sorted(
        [
            group["project_name"]
            for group in await groups_dal.get_all(filtering_exp=filtering_exp)
        ]
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    removed_groups = await get_removed_groups()
    removed_groups_len = len(removed_groups)
    LOGGER_CONSOLE.info(
        "Removed groups",
        extra={
            "extra": {
                "removed_groups_len": removed_groups_len,
            }
        },
    )
    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group_name,
                progress=count / removed_groups_len,
            )
            for count, group_name in enumerate(removed_groups)
        ),
        workers=32,
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
