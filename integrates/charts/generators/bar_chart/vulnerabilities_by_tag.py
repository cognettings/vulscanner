from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts import (
    utils,
)
from charts.generators.bar_chart.utils import (
    format_vulnerabilities_by_data,
)
from collections import (
    Counter,
)
from custom_utils.findings import (
    get_group_findings,
)
from dataloaders import (
    get_new_context,
)
from itertools import (
    chain,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter[str]:
    context = get_new_context()
    group_findings = await get_group_findings(
        group_name=group, loaders=context
    )
    finding_ids = [finding.id for finding in group_findings]

    vulnerabilities = (
        await context.finding_vulnerabilities_released_nzr.load_many_chained(
            finding_ids
        )
    )

    return Counter(
        filter(
            None,
            chain.from_iterable(map(lambda x: x.tags or [], vulnerabilities)),
        )
    )


async def get_data_many_groups(groups: tuple[str, ...]) -> Counter[str]:
    groups_data = await collect(map(get_data_one_group, groups), workers=32)

    return sum(groups_data, Counter())


async def generate_all() -> None:
    column: str = "Tag"
    async for group in utils.iterate_groups():
        json_document, csv_document = format_vulnerabilities_by_data(
            counters=await get_data_one_group(group),
            column=column,
            axis_rotated=True,
        )
        utils.json_dump(
            document=json_document,
            entity="group",
            subject=group,
            csv_document=csv_document,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        json_document, csv_document = format_vulnerabilities_by_data(
            counters=await get_data_many_groups(org_groups),
            column=column,
            axis_rotated=True,
        )
        utils.json_dump(
            document=json_document,
            entity="organization",
            subject=org_id,
            csv_document=csv_document,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            json_document, csv_document = format_vulnerabilities_by_data(
                counters=await get_data_many_groups(groups),
                column=column,
                axis_rotated=True,
            )
            utils.json_dump(
                document=json_document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=csv_document,
            )


if __name__ == "__main__":
    run(generate_all())
