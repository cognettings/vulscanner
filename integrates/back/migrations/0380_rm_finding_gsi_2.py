# pylint: disable=invalid-name
"""
Remove `pk_2` and 'sk_2' on findings that have it.

Execution Time:    2023-04-14 at 14:26:33 UTC
Finalization Time: 2023-04-14 at 14:35:03 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
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
from dynamodb import (
    keys,
    operations,
)
from organizations.domain import (
    get_all_group_names,
)
import time


async def process_finding(finding: Finding) -> None:
    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": finding.group_name, "id": finding.id},
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item={
            "pk_2": None,
            "sk_2": None,
        },
        key=metadata_key,
        table=TABLE,
    )


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    count: int,
) -> None:
    group_findings = await loaders.group_findings_all.load(group_name)
    if not group_findings:
        return

    await collect(
        tuple(process_finding(finding=finding) for finding in group_findings),
    )
    print(f"Group processed {group_name} {count}")


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(await get_all_group_names(loaders))
    print(f"{group_names=}")
    print(f"{len(group_names)=}")
    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group,
                count=count + 1,
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
