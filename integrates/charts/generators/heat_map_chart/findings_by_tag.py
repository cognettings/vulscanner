from aioextensions import (
    collect,
    run,
)
from charts import (
    utils,
)
from charts.generators.heat_map_chart.common import (
    format_csv_data,
)
from collections import (
    Counter,
)
from collections.abc import (
    Iterable,
)
from custom_utils.findings import (
    get_group_findings,
)
from dataloaders import (
    get_new_context,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from itertools import (
    chain,
)
from typing import (
    NamedTuple,
)

FindingsTags = NamedTuple(
    "FindingsTags",
    [
        ("counter", Counter[str]),
        ("counter_finding", Counter[str]),
        ("findings", list[str]),
        ("tags", set[str]),
    ],
)


async def get_data_finding(
    finding_title: str, vulnerabilities: Iterable[Vulnerability]
) -> FindingsTags:
    title = finding_title.split(".")[0]
    tags: list[str] = list(
        filter(
            None,
            chain.from_iterable(map(lambda x: x.tags or [], vulnerabilities)),
        )
    )

    return FindingsTags(
        counter=Counter(tags),
        counter_finding=Counter([f"{title}/{tag}" for tag in tags]),
        findings=[title] if tags else [],
        tags=set(tags),
    )


async def get_data(group: str) -> FindingsTags:
    loaders = get_new_context()
    group_findings = await get_group_findings(
        group_name=group, loaders=loaders
    )
    finding_ids = [finding.id for finding in group_findings]
    findings = [finding.title for finding in group_findings]

    vulnerabilities = (
        await loaders.finding_vulnerabilities_released_nzr.load_many(
            finding_ids
        )
    )

    findings_data = await collect(
        tuple(
            get_data_finding(finding_title, vulns)
            for finding_title, vulns in zip(findings, vulnerabilities)
        ),
        workers=32,
    )
    all_tags = [finding_data.tags for finding_data in findings_data]

    return FindingsTags(
        counter=sum(
            [finding_data.counter for finding_data in findings_data], Counter()
        ),
        counter_finding=sum(
            [finding_data.counter_finding for finding_data in findings_data],
            Counter(),
        ),
        findings=[
            finding_data.findings[0]
            for finding_data in findings_data
            if finding_data.findings
        ],
        tags=set.union(*all_tags) if all_tags else set(),
    )


def format_data(data: FindingsTags) -> dict:
    max_value: list[tuple[str, int]] = data.counter_finding.most_common(1)
    tags: set[str] = {tag for tag, _ in data.counter.most_common()[:10]}
    findings: set[str] = {
        finding
        for finding in data.findings
        for tag in tags
        if data.counter_finding[f"{finding}/{tag}"] > 0
    }

    return dict(
        x=findings,
        grid_values=[
            {
                "value": data.counter_finding[f"{finding}/{tag}"],
                "x": finding,
                "y": tag,
            }
            for finding in findings
            for tag in tags
        ],
        y=tags,
        max_value=max_value[0][1] if max_value else 1,
        tick_rotate=utils.TICK_ROTATION,
    )


async def generate_all() -> None:
    data: FindingsTags
    async for group in utils.iterate_groups():
        data = await get_data(group)
        document = format_data(data=data)
        utils.json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(
                categories=document["x"],
                values=document["y"],
                counters=data.counter_finding,
                header="Type code",
            ),
        )


if __name__ == "__main__":
    run(generate_all())
