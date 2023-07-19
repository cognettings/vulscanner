# pylint: disable=invalid-name
# type: ignore
"""
Remove `severity` attribute on vulnerabilities that have it. This map holds
the floating point weights of the severity vector, but now we'll use the
CVSS:3.1 vector string.

Execution Time:    2023-04-13 at 00:23:47 UTC
Finalization Time: 2023-04-13 at 01:00:26 UTC
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
from dynamodb.types import (
    PrimaryKey,
)
from organizations.domain import (
    get_all_group_names,
)
import time


async def get_finding_vulnerabilities_items(
    finding_id: str,
) -> tuple[Item, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"finding_id": finding_id},
    )
    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        filter_expression=Attr("severity").exists(),
        facets=(TABLE.facets["vulnerability_metadata"],),
        table=TABLE,
        index=index,
    )

    return response.items


async def process_vulnerability_item(item: Item) -> None:
    primary_key = PrimaryKey(partition_key=item["pk"], sort_key=item["sk"])
    key_structure = TABLE.primary_key
    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists(),
        item={"severity": None},
        key=primary_key,
        table=TABLE,
    )


async def process_finding(finding: Finding) -> None:
    items = await get_finding_vulnerabilities_items(finding_id=finding.id)
    if not items:
        return

    await collect(
        tuple(process_vulnerability_item(item) for item in items),
        workers=4,
    )


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    group_findings = await loaders.group_drafts_and_findings_all.load(
        group_name
    )
    if not group_findings:
        return

    await collect(
        tuple(process_finding(finding=finding) for finding in group_findings),
        workers=4,
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
                loaders=loaders,
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
