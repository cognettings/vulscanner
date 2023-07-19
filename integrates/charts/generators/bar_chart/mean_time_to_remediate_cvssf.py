from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.bar_chart import (
    mean_time_to_remediate_non_treated_cvssf as generator,
)
from charts.generators.bar_chart.utils import (
    Remediate,
    sum_mttr_many_groups,
)
from charts.generators.bar_chart.utils_mean_time_to_remediate import (
    generate_all,
)
from collections.abc import (
    Iterable,
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
from groups import (
    domain as groups_domain,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    group: str, loaders: Dataloaders, min_date: date | None = None
) -> Remediate:
    critical, high, medium, low = await collect(
        [
            groups_domain.get_mean_remediate_severity_cvssf(
                loaders, group, Decimal("9"), Decimal("10"), min_date
            ),
            groups_domain.get_mean_remediate_severity_cvssf(
                loaders, group, Decimal("7"), Decimal("8.9"), min_date
            ),
            groups_domain.get_mean_remediate_severity_cvssf(
                loaders, group, Decimal("4"), Decimal("6.9"), min_date
            ),
            groups_domain.get_mean_remediate_severity_cvssf(
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
    groups: Iterable[str],
    loaders: Dataloaders,
    min_date: date | None = None,
) -> Remediate:
    groups_data = await collect(
        tuple(
            get_data_one_group(group=group, loaders=loaders, min_date=min_date)
            for group in groups
        ),
        workers=24,
    )

    return sum_mttr_many_groups(groups_data=groups_data)


if __name__ == "__main__":
    run(
        generate_all(
            format_data=generator.format_data,
            get_data_one_group=get_data_one_group,
            get_data_many_groups=get_data_many_groups,
            alternative="Mean time to remediate (cvssf) in days",
        )
    )
