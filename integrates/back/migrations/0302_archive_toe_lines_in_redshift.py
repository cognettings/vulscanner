# pylint: disable=invalid-name,import-error
"""
From deleted groups, send TOE lines to redshift for analytics purposes and
remove them from dynamodb.

Execution Time:    2022-10-19 at 02:10:35 UTC
Finalization Time: 2022-10-19 at 17:18:51 UTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    toe_lines as toe_lines_model,
)
from db_model.toe_lines.get import (  # type: ignore
    get_toe_lines_items_by_group,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
from redshift import (
    toe_lines as redshift_toe_lines,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def _process_group(
    group_name: str,
    progress: float,
) -> None:
    items = await get_toe_lines_items_by_group(group_name)
    if items:
        await redshift_toe_lines.insert_batch_metadata(items=items)
        await toe_lines_model.remove_items(items=items)  # type: ignore
    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "len(items)": len(items),
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    deleted_groups = await orgs_domain.get_all_deleted_groups(loaders)
    deleted_group_names = sorted([group.name for group in deleted_groups])
    LOGGER_CONSOLE.info(
        "Deleted groups",
        extra={"extra": {"groups_len": len(deleted_group_names)}},
    )
    await collect(
        tuple(
            _process_group(
                group_name=group_name,
                progress=count / len(deleted_group_names),
            )
            for count, group_name in enumerate(deleted_group_names)
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
