from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.common.colors import (
    RISK,
)
from charts.generators.pie_chart.utils import (
    generate_all,
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
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter[VulnerabilityStateStatus]:
    loaders = get_new_context()
    findings = await get_group_findings(group_name=group, loaders=loaders)
    vulnerabilities = (
        await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
            [finding.id for finding in findings]
        )
    )

    return Counter(
        tuple(
            vulnerability.state.status
            for vulnerability in vulnerabilities
            if vulnerability.treatment and vulnerability.treatment.assigned
        )
    )


async def get_data_many_groups(
    groups: tuple[str, ...]
) -> Counter[VulnerabilityStateStatus]:
    groups_data = await collect(
        tuple(get_data_one_group(group=group) for group in groups),
        workers=32,
    )

    return sum(groups_data, Counter())


def format_data(data: Counter[VulnerabilityStateStatus]) -> dict:
    return dict(
        data=dict(
            columns=[
                ["Open", data[VulnerabilityStateStatus.VULNERABLE]],
                ["Closed", data[VulnerabilityStateStatus.SAFE]],
            ],
            type="pie",
            colors=dict(
                Open=RISK.more_agressive,
                Closed=RISK.more_passive,
            ),
        ),
        legend=dict(
            position="right",
        ),
        pie=dict(
            label=dict(
                show=True,
            ),
        ),
    )


if __name__ == "__main__":
    run(
        generate_all(
            format_document=format_data,
            get_data_one_group=get_data_one_group,
            get_data_many_groups=get_data_many_groups,
            header=["Status of assigned vulnerabilities", "Number"],
        )
    )
