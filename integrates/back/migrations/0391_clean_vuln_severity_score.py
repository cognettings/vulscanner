# pylint: disable=invalid-name
"""
Some vulns are populated with an incomplete severity_score map attribute,
so delete it.

Execution Time:    2023-04-25 at 18:32:50 UTC
Finalization Time: 2023-04-25 at 18:53:24 UTC
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
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from dynamodb import (
    keys,
    operations,
)
from organizations.domain import (
    get_all_group_names,
)
import time


async def process_vulnerability(vuln: Vulnerability) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={
            "id": vuln.id,
            "finding_id": vuln.finding_id,
        },
    )
    key_structure = TABLE.primary_key
    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists(),
        item={"severity_score": None},
        key=primary_key,
        table=TABLE,
    )
    print(f"{vuln.group_name=} {vuln.id=} {vuln.severity_score=}")


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    group_findings = await loaders.group_findings_all.load(group_name)
    if not group_findings:
        return
    group_vulns = await loaders.finding_vulnerabilities_all.load_many_chained(
        [finding.id for finding in group_findings]
    )
    vulns_filtered = [
        vuln
        for vuln in group_vulns
        if vuln.severity_score and not vuln.severity_score.cvss_v3
    ]
    if not vulns_filtered:
        return

    await collect(
        tuple(process_vulnerability(vuln) for vuln in vulns_filtered),
        workers=8,
    )
    print(
        f"Group processed {group_name} {len(vulns_filtered)=} "
        f"{str(round(progress, 2))}"
    )


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
        workers=8,
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
