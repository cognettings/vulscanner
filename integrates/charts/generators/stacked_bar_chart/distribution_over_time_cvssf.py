from aioextensions import (
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.stacked_bar_chart.distribution_over_time import (
    generate_all,
    get_document_formatted,
)
from charts.generators.stacked_bar_chart.util_class import (
    RiskOverTime,
)
from dataloaders import (
    Dataloaders,
)


@alru_cache(maxsize=None, typed=True)
async def get_group_document(
    group: str,
    loaders: Dataloaders,
) -> RiskOverTime:
    group_indicators = await loaders.group_unreliable_indicators.load(group)

    return get_document_formatted(
        group_over_time=[
            elements[-12:]
            for elements in group_indicators.remediated_over_time_cvssf or []
        ],
        group_over_time_monthly=(
            group_indicators.remediated_over_time_month_cvssf
        ),
        group_over_time_yearly=(
            group_indicators.remediated_over_time_year_cvssf
        ),
        weekly_data_size=len(
            group_indicators.remediated_over_time_cvssf[0]
            if group_indicators.remediated_over_time_cvssf
            else []
        ),
        monthly_data_size=len(
            group_indicators.remediated_over_time_month_cvssf[0]
            if group_indicators.remediated_over_time_month_cvssf
            else []
        ),
    )


if __name__ == "__main__":
    run(generate_all("CVSSF", get_group_document))
