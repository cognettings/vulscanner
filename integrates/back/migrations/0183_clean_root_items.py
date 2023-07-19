# type: ignore

# pylint: disable=invalid-name
"""
This migration removes the items previously used to store the current states
of a root as they have been replaced by a single item strategy.

Execution Time: 2022-02-15 at 20:21:54 UTC
Finalization Time: 2022-02-15 at 20:26:37 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from collections import (
    defaultdict,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    historics,
    operations,
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
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


index = TABLE.indexes["inverted_index"]
key_structure = index.primary_key


async def process_root(root_id: str, items: list[dict[str, Any]]) -> None:
    metadata = historics.get_metadata(
        item_id=root_id, key_structure=key_structure, raw_items=items
    )
    root_key = PrimaryKey(
        partition_key=metadata["pk"], sort_key=metadata["sk"]
    )
    state = historics.get_optional_latest(
        item_id=root_id,
        key_structure=key_structure,
        historic_suffix="STATE",
        raw_items=items,
    )
    cloning = historics.get_optional_latest(
        item_id=root_id,
        key_structure=key_structure,
        historic_suffix="CLON",
        raw_items=items,
    )

    if state:
        await operations.update_item(
            key=root_key,
            item={"state.pk": None, "state.sk": None},
            table=TABLE,
        )
        await operations.delete_item(
            key=PrimaryKey(partition_key=state["pk"], sort_key=state["sk"]),
            table=TABLE,
        )

    if cloning:
        await operations.update_item(
            key=root_key,
            item={"cloning.pk": None, "cloning.sk": None},
            table=TABLE,
        )
        await operations.delete_item(
            key=PrimaryKey(
                partition_key=cloning["pk"], sort_key=cloning["sk"]
            ),
            table=TABLE,
        )


async def process_group(group_name: str, progress: float) -> None:
    response = await operations.query(
        condition_expression=(
            Key("sk").eq(f"GROUP#{group_name}")
            & Key("pk").begins_with("ROOT#")
        ),
        facets=(
            TABLE.facets["git_root_historic_cloning"],
            TABLE.facets["git_root_metadata"],
            TABLE.facets["git_root_historic_state"],
            TABLE.facets["ip_root_metadata"],
            TABLE.facets["ip_root_historic_state"],
            TABLE.facets["url_root_metadata"],
            TABLE.facets["url_root_historic_state"],
        ),
        index=index,
        table=TABLE,
    )
    root_items = defaultdict(list)
    for item in response.items:
        root_id = "#".join(item[key_structure.sort_key].split("#")[:2])
        root_items[root_id].append(item)

    await collect(
        tuple(
            process_root(root_id, items)
            for root_id, items in root_items.items()
        ),
        workers=10,
    )

    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "roots": len(root_items),
                "progress": str(progress),
            }
        },
    )


async def get_group_names() -> list[str]:
    return sorted(
        group["project_name"] for group in await groups_dal.get_all()
    )


async def main() -> None:
    groups = await get_group_names()

    await collect(
        tuple(
            process_group(group_name, count / len(groups))
            for count, group_name in enumerate(groups)
        ),
        workers=10,
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
