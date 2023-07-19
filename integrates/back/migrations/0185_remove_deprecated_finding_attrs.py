# type: ignore

# pylint: disable=invalid-name
"""
Remove compromised_attributes and compromised_records attrs from
findings in DynamoDB.

Execution Time:     2022-02-16 at 17:54:58 UTC
Finalization Time:  2022-02-16 at 17:56:29 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from class_types.types import (
    Item,
)
from db_model import (
    TABLE,
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
from dynamodb.types import (
    PrimaryKey,
)
from groups import (
    dal as groups_dal,
)
import logging
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_finding(
    *,
    finding: Item,
) -> None:
    await operations.update_item(
        item={
            "compromised_attributes": None,
            "compromised_records": None,
        },
        key=PrimaryKey(
            partition_key=finding["pk"],
            sort_key=finding["sk"],
        ),
        table=TABLE,
    )


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
    sleep_seconds=10,
)
async def process_group(
    *,
    group_name: str,
    progress: float,
) -> None:
    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name},
    )
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["finding_metadata"],),
        filter_expression=Attr("compromised_attributes").exists()
        | Attr("compromised_records").exists(),
        index=index,
        table=TABLE,
    )
    group_findings: list[Item] = response.items
    await collect(
        tuple(process_finding(finding=finding) for finding in group_findings),
        workers=64,
    )
    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "findings": len(group_findings),
                "progress": str(progress),
            }
        },
    )


async def main() -> None:
    group_names = sorted(await groups_dal.get_active_groups())
    active_groups_len = len(group_names)
    LOGGER_CONSOLE.info(
        "Active groups",
        extra={
            "extra": {
                "groups": active_groups_len,
            }
        },
    )
    await collect(
        tuple(
            process_group(
                group_name=group_name,
                progress=count / active_groups_len,
            )
            for count, group_name in enumerate(group_names)
        ),
        workers=16,
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
