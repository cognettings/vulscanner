from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.stacked_bar_chart.util_class import (
    AssignedFormatted,
)
from charts.generators.stacked_bar_chart.utils import (
    format_stacked_vulnerabilities_data,
    limit_data,
)
from charts.utils import (
    get_portfolios_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    GroupTreatmentSummary,
    GroupUnreliableIndicators,
)
from decimal import (
    Decimal,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    loaders: Dataloaders,
    group_name: str,
) -> AssignedFormatted:
    indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group_name)
    )
    open_vulnerabilities: int = indicators.open_vulnerabilities or 0
    treatment: GroupTreatmentSummary | None = indicators.treatment_summary
    if treatment:
        accepted_vulnerabilities: int = (
            treatment.accepted_undefined + treatment.accepted
        )
    else:
        accepted_vulnerabilities = 0
    remaining_open_vulnerabilities: int = (
        open_vulnerabilities - accepted_vulnerabilities
    )
    return AssignedFormatted(
        name=group_name,
        accepted=Decimal(treatment.accepted if treatment else 0),
        accepted_undefined=Decimal(
            treatment.accepted_undefined if treatment else 0
        ),
        remaining_open_vulnerabilities=Decimal(
            remaining_open_vulnerabilities
            if remaining_open_vulnerabilities >= 0
            else 0
        ),
        open_vulnerabilities=Decimal(open_vulnerabilities),
        closed_vulnerabilities=Decimal(indicators.closed_vulnerabilities or 0),
    )


async def get_data_many_groups(
    loaders: Dataloaders,
    group_names: tuple[str, ...],
) -> list[AssignedFormatted]:
    groups_data = await collect(
        [
            get_data_one_group(loaders, group_name)
            for group_name in group_names
        ],
        workers=32,
    )

    return sorted(
        groups_data,
        key=lambda x: (
            x.open_vulnerabilities
            / (x.closed_vulnerabilities + x.open_vulnerabilities)
            if (x.closed_vulnerabilities + x.open_vulnerabilities) > 0
            else 0
        ),
        reverse=True,
    )


async def generate_all() -> None:
    loaders = get_new_context()
    header = "Group name"
    async for org_id, _, org_group_names in iterate_organizations_and_groups():
        json_document, csv_document = format_stacked_vulnerabilities_data(
            all_data=limit_data(
                await get_data_many_groups(loaders, org_group_names)
            ),
            header=header,
        )
        json_dump(
            document=json_document,
            entity="organization",
            subject=org_id,
            csv_document=csv_document,
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, group_names in await get_portfolios_groups(org_name):
            json_document, csv_document = format_stacked_vulnerabilities_data(
                all_data=limit_data(
                    await get_data_many_groups(loaders, group_names)
                ),
                header=header,
            )
            json_dump(
                document=json_document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=csv_document,
            )


if __name__ == "__main__":
    run(generate_all())
