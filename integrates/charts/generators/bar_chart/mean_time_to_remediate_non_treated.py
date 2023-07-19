from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.bar_chart.utils import (
    Remediate,
    sum_mttr_many_groups,
)
from charts.generators.bar_chart.utils_mean_time_to_remediate import (
    format_data_non_cvssf,
    generate_all,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    date,
)
from decimal import (
    Decimal,
)
from groups.domain import (
    get_mean_remediate_non_treated_severity,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    group: str, loaders: Dataloaders, min_date: date | None = None
) -> Remediate:
    critical, high, medium, low = await collect(
        [
            get_mean_remediate_non_treated_severity(
                loaders, group, Decimal("9.0"), Decimal("10.0"), min_date
            ),
            get_mean_remediate_non_treated_severity(
                loaders, group, Decimal("7.0"), Decimal("8.9"), min_date
            ),
            get_mean_remediate_non_treated_severity(
                loaders, group, Decimal("4.0"), Decimal("6.9"), min_date
            ),
            get_mean_remediate_non_treated_severity(
                loaders, group, Decimal("0.1"), Decimal("3.9"), min_date
            ),
        ]
    )

    return Remediate(
        critical_severity=critical,
        high_severity=high,
        medium_severity=medium,
        low_severity=low,
    )


async def get_data_many_groups(
    groups: tuple[str, ...],
    loaders: Dataloaders,
    min_date: date | None = None,
) -> Remediate:
    groups_data = await collect(
        tuple(
            get_data_one_group(group=group, loaders=loaders, min_date=min_date)
            for group in groups
        ),
        workers=32,
    )

    return sum_mttr_many_groups(groups_data=groups_data)


if __name__ == "__main__":
    run(
        generate_all(
            format_data=format_data_non_cvssf,
            get_data_one_group=get_data_one_group,
            get_data_many_groups=get_data_many_groups,
            alternative="Mean time to remediate non treated in days",
        )
    )
