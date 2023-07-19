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


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter[str]:
    loaders = get_new_context()
    findings = await get_group_findings(group_name=group, loaders=loaders)
    vulnerabilities = (
        await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
            [finding.id for finding in findings]
        )
    )

    return Counter(
        tuple(
            vulnerability.technique if vulnerability.technique else "MPT"
            for vulnerability in vulnerabilities
        )
    )


async def get_data_many_groups(groups: tuple[str, ...]) -> Counter[str]:
    return sum(
        await collect(
            tuple(get_data_one_group(group=group) for group in groups),
            workers=32,
        ),
        Counter(),
    )


def format_data(data: Counter[str]) -> dict:
    return dict(
        data=dict(
            columns=[
                ["MPT", data["MPT"]],
                ["SCR", data["SCR"]],
                ["SAST", data["SAST"]],
                ["DAST", data["DAST"]],
                ["SCA", data["SCA"]],
                ["RE", data["RE"]],
                ["CSPM", data["CSPM"]],
            ],
            type="pie",
            colors=dict(
                MPT=RISK.more_agressive,
                SCR=RISK.optional_agressive,
                SAST=RISK.agressive,
                DAST=RISK.neutral,
                SCA=RISK.passive,
                RE=RISK.optional_passive,
                CSPM=RISK.more_passive,
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
            get_data_one_group=get_data_one_group,
            get_data_many_groups=get_data_many_groups,
            format_document=format_data,
            header=["Report Technique", "Occurrences"],
        )
    )
