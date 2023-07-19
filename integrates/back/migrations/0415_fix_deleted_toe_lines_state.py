# pylint: disable=invalid-name
"""
The state of some toe lines were deleted by mistake so the last
historic state will be used to restore these toe lines states

Execution Time:    2023-07-12 at 01:17:52 UTC
Finalization Time: 2023-07-12 at 15:43:12 UTC

Execution Time:    2023-07-12 at 20:53:55 UTC
Finalization Time: 2023-07-12 at 23:05:12 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from class_types.types import (
    Item,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from organizations.domain import (
    get_all_group_names,
)
import time

KEY_STRUCTURE = TABLE.primary_key


async def process_toe_lines(item: Item) -> None:
    group_name = item["group_name"]
    root_id = item["root_id"]
    filename = item["filename"]
    primary_key = keys.build_key(
        facet=TABLE.facets["toe_lines_historic_metadata"],
        values={
            "filename": filename,
            "group_name": group_name,
            "root_id": root_id,
        },
    )
    historic_state = await operations.query(
        condition_expression=(
            Key(KEY_STRUCTURE.partition_key).eq(primary_key.partition_key)
            & Key(KEY_STRUCTURE.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["toe_lines_historic_metadata"],),
        table=TABLE,
        forward=False,
        limit=1,
    )

    if not historic_state.items:
        print(
            f"[Warning] The toeline of group {group_name}, root id {root_id} "
            f"and filename {filename} does not have a historic state"
        )
        return

    metadata_key = keys.build_key(
        facet=TABLE.facets["toe_lines_metadata"],
        values={
            "filename": filename,
            "group_name": group_name,
            "root_id": root_id,
        },
    )
    metadata_item: Item = {}
    if "modified_by" not in item["state"] and historic_state.items:
        metadata_item["state"] = historic_state.items[0]["state"]

    if metadata_item:
        await operations.update_item(
            item=metadata_item,
            key=metadata_key,
            table=TABLE,
        )


async def process_group(
    group_name: str,
    progress: float,
) -> None:
    response = await operations.query(
        condition_expression=(
            Key(KEY_STRUCTURE.partition_key).eq(f"GROUP#{group_name}")
            & Key(KEY_STRUCTURE.sort_key).begins_with("LINES#")
        ),
        facets=(TABLE.facets["toe_lines_metadata"],),
        index=None,
        table=TABLE,
    )
    await collect(
        tuple(process_toe_lines(item) for item in response.items), workers=100
    )
    print(f"Group processed {group_name} {str(round(progress, 2))}")


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(await get_all_group_names(loaders), reverse=True)
    print(f"{group_names=}")
    print(f"{len(group_names)=}")
    await collect(
        tuple(
            process_group(
                group_name=group,
                progress=count / len(group_names),
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
    print(f"{execution_time}\n{finalization_time}")
