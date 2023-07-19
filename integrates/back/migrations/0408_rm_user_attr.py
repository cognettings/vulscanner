# pylint: disable=invalid-name
"""
update user metadata by removing deprecated attrs
Start Time:        2023-06-28 at 04:02:28 UTC
Finalization Time: 2023-06-28 at 04:02:35 UTC
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
from custom_exceptions import (
    ErrorLoadingStakeholders,
)
from db_model import (
    TABLE,
)
from db_model.stakeholders.constants import (
    ALL_STAKEHOLDERS_INDEX_METADATA,
)
from dynamodb import (
    keys,
    operations,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)
LOGGER_CONSOLE = logging.getLogger("console")


async def _update_metadata(
    *,
    email: str,
) -> None:
    email = email.lower().strip()
    gsi_2_index = TABLE.indexes["gsi_2"]
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={
            "email": email,
        },
    )
    gsi_2_key = keys.build_key(
        facet=ALL_STAKEHOLDERS_INDEX_METADATA,
        values={
            "all": "all",
            "email": email,
        },
    )
    item = {
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        "email": email,
        "access_token": None,
        "last_api_token_use_date": None,
    }

    await operations.update_item(
        item=item,
        key=primary_key,
        table=TABLE,
    )


async def process_user(user: Item, progress: float) -> None:
    if "access_token" in user or "last_api_token_use_date" in user:
        email = str(user.get("email")) or str(user["pk"]).split("#")[1]
        await _update_metadata(email=email.lower().strip())

        LOGGER_CONSOLE.info(
            "User updated",
            extra={
                "extra": {
                    "user email": email,
                    "progress": round(progress, 2),
                }
            },
        )


async def _get_all_stakeholders() -> tuple[Item, ...]:
    primary_key = keys.build_key(
        facet=ALL_STAKEHOLDERS_INDEX_METADATA,
        values={"all": "all"},
    )
    index = TABLE.indexes["gsi_2"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(ALL_STAKEHOLDERS_INDEX_METADATA,),
        table=TABLE,
        index=index,
    )

    if not response.items:
        raise ErrorLoadingStakeholders()
    return response.items


async def main() -> None:
    all_stakeholders = await _get_all_stakeholders()
    LOGGER_CONSOLE.info(
        "Active users",
        extra={"extra": {"users_len": len(all_stakeholders)}},
    )
    await collect(
        tuple(
            process_user(
                user=stakeholder, progress=count / len(all_stakeholders)
            )
            for count, stakeholder in enumerate(all_stakeholders)
        ),
        workers=32,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Start Time:        %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    LOGGER_CONSOLE.info("\n%s\n%s", execution_time, finalization_time)
