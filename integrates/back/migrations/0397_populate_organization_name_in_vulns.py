# pylint: disable=invalid-name
"""
Add the organization name into the vulnerability entity.

Start Time:        2023-05-25 at 21:37:44 UTC
Finalization Time: 2023-05-25 at 22:42:13 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    GroupNotFound,
    OrganizationNotFound,
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
from organizations import (
    domain as orgs_domain,
)
import time


async def process_vulnerability(
    vuln: Vulnerability, organization_name: str
) -> None:
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
        item={"organization_name": organization_name},
        key=primary_key,
        table=TABLE,
    )


async def process_group(
    loaders: Dataloaders,
    group_name: str,
) -> None:
    group = await loaders.group.load(group_name)
    if not group:
        raise GroupNotFound()
    organization = await loaders.organization.load(group.organization_id)
    if not organization:
        raise OrganizationNotFound()
    group_findings = await loaders.group_findings_all.load(group_name)
    group_vulns = await loaders.finding_vulnerabilities_all.load_many_chained(
        [finding.id for finding in group_findings]
    )
    await collect(
        tuple(
            process_vulnerability(vuln, organization_name=organization.name)
            for vuln in group_vulns
        ),
        workers=1000,
    )
    print(f"Group processed {group_name}")


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    all_group_names = sorted(
        await orgs_domain.get_all_group_names(loaders=loaders)
    )
    count = 0
    print("all_group_names", len(all_group_names))
    for group_name in all_group_names:
        count += 1
        print("group", group_name, count)
        await process_group(loaders, group_name)


if __name__ == "__main__":
    execution_time = time.strftime("Start Time:    %Y-%m-%d at %H:%M:%S UTC")
    print(execution_time)
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
