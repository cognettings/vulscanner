from .constants import (
    PATCH_SRC,
)
from boto3.dynamodb.conditions import (
    Key,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    PrimaryKey,
)


async def remove(
    *, platform: str, pkg_name: str, advisory_id: str, source: str = PATCH_SRC
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["advisories"],
        values={
            "platform": platform,
            "pkg_name": pkg_name,
            "id": advisory_id,
            "src": source,
        },
    )
    await operations.delete_item(key=primary_key, table=TABLE)
    print(f"Removed ( {platform}#{pkg_name}  {advisory_id}#{source} )")


async def batch_remove(
    *, platform: str, pkg_name: str, advisory_id: str, source: str = PATCH_SRC
) -> None:
    facet = TABLE.facets["advisories"]
    primary_key = keys.build_key(
        facet=facet,
        values={
            "platform": platform,
            "pkg_name": pkg_name,
            "id": advisory_id,
            "src": source,
        },
    )
    key_structure = TABLE.primary_key
    condition_expression = Key(key_structure.partition_key).eq(
        primary_key.partition_key
    ) & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
    response = await operations.query(
        condition_expression=condition_expression,
        facets=(facet,),
        table=TABLE,
    )
    await operations.batch_delete_item(
        keys=tuple(
            PrimaryKey(
                partition_key=item["pk"],
                sort_key=item["sk"],
            )
            for item in response.items
        ),
        table=TABLE,
    )
    print(f"Removed ( {platform}#{pkg_name}  {advisory_id}#{source} )")
