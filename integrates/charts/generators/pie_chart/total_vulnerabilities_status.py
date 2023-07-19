from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.pie_chart import (
    vulnerabilities_with_undefined_treatment as generator,
)
from charts.generators.pie_chart.utils import (
    PortfoliosGroupsInfo,
    slice_groups,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    GroupUnreliableIndicators,
)
from decimal import (
    Decimal,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_group(
    loaders: Dataloaders,
    group_name: str,
) -> PortfoliosGroupsInfo:
    indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group_name)
    )
    open_vulns = indicators.open_vulnerabilities or 0
    closed_vulns = indicators.closed_vulnerabilities or 0
    return PortfoliosGroupsInfo(
        group_name=group_name,
        value=Decimal(open_vulns + closed_vulns),
    )


async def get_data_groups(
    loaders: Dataloaders,
    group_names: tuple[str, ...],
) -> list[PortfoliosGroupsInfo]:
    groups_data = await collect(
        [get_data_group(loaders, group_name) for group_name in group_names],
        workers=32,
    )
    total_vulnerabilities = sum(group.value for group in groups_data)

    return slice_groups(groups_data, Decimal(total_vulnerabilities))


if __name__ == "__main__":
    run(
        generator.generate_all(headers=["Group name", "Total vulnerabilities"])
    )
