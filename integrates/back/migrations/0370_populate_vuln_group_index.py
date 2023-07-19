# pylint: disable=invalid-name
# type: ignore
"""
Populate the group index in vulnerabilities.

Execution Time:    2023-03-23 at 16:18:42 UTC-5
Finalization Time: 2023-03-23 at 17:06:51 UTC-5
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from botocore.exceptions import (
    HTTPClientError,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from db_model.vulnerabilities.utils import (
    get_group_index_key,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from itertools import (
    chain,
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
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
    sleep_seconds=10,
)
async def process_vuln(vulnerability: Vulnerability) -> None:
    key_structure = TABLE.primary_key
    gsi_5_index = TABLE.indexes["gsi_5"]
    vulnerability_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={
            "finding_id": vulnerability.finding_id,
            "id": vulnerability.id,
        },
    )
    group_index_key = get_group_index_key(vulnerability)
    vulnerability_item = {
        gsi_5_index.primary_key.partition_key: group_index_key.partition_key,
        gsi_5_index.primary_key.sort_key: group_index_key.sort_key,
    }
    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists(),
        item=vulnerability_item,
        key=vulnerability_key,
        table=TABLE,
    )


@retry_on_exceptions(
    exceptions=(HTTPClientError,),
    sleep_seconds=10,
)
async def process_group(
    loaders: Dataloaders, group_name: str, progress: float
) -> None:
    all_findings: list[Finding] = await loaders.group_drafts_and_findings.load(
        group_name
    )
    all_group_vulnerabilities = tuple(
        chain.from_iterable(
            await loaders.finding_vulnerabilities_all.load_many(
                {finding.id for finding in all_findings}
            )
        )
    )
    await collect(
        (
            process_vuln(vulnerability=vulnerability)
            for vulnerability in all_group_vulnerabilities
        ),
        workers=200,
    )
    LOGGER_CONSOLE.info(
        "Group updated",
        extra={
            "extra": {
                "group_name": group_name,
                "progress": str(round(progress, 2)),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(await get_all_group_names(loaders=loaders))
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
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
