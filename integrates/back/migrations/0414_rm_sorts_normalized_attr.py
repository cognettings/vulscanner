# pylint: disable=invalid-name
"""
Remove the sorts_risk_level_normalized attribute.
This attr is the normalized version of the sorts_risk_level used for analytics
but now the sorts_priority_factor will be used,
calculating its normalized version only when it is needed

Execution Time:    2023-07-07 at 19:40:00 UTC
Finalization Time: 2023-07-10 at 23:17:51 UTC

Execution Time:    2023-07-14 at 17:06:06 UTC
Finalization Time: 2023-07-14 at 17:49:59 UTC
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


async def process_toe_lines(item: Item) -> None:
    metadata_key = keys.build_key(
        facet=TABLE.facets["toe_lines_metadata"],
        values={
            "filename": item["filename"],
            "group_name": item["group_name"],
            "root_id": item["root_id"],
        },
    )
    metadata_item: Item = {}
    if item["state"].get("sorts_risk_level_normalized") is not None:
        metadata_item["state.sorts_risk_level_normalized"] = None

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
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(f"GROUP#{group_name}")
            & Key(key_structure.sort_key).begins_with("LINES#")
        ),
        facets=(TABLE.facets["toe_lines_metadata"],),
        index=None,
        table=TABLE,
    )
    await collect(
        tuple(process_toe_lines(item) for item in response.items), workers=15
    )
    print(f"Group processed {group_name} {str(round(progress, 2))}")


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(await get_all_group_names(loaders))
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
