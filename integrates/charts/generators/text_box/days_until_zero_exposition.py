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
from custom_utils.findings import (
    get_group_findings,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from decimal import (
    Decimal,
    ROUND_CEILING,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group_name: str, loaders: Dataloaders) -> Decimal:
    group_findings = await get_group_findings(
        group_name=group_name, loaders=loaders
    )
    findings_ids: tuple[str, ...] = tuple(
        finding.id for finding in group_findings
    )
    finding_vulns = (
        await loaders.finding_vulnerabilities_released_nzr.load_many(
            findings_ids
        )
    )

    counter: Decimal = Decimal("0.0")
    for finding, vulnerabilities in zip(group_findings, finding_vulns):
        for vulnerability in vulnerabilities:
            if (
                vulnerability.state.status
                == VulnerabilityStateStatus.VULNERABLE
            ):
                if finding.min_time_to_remediate:
                    counter += Decimal(finding.min_time_to_remediate)
                else:
                    counter += Decimal("60.0")

    minutes_days: Decimal = Decimal("24.0") * Decimal("60.0")

    return Decimal(counter / minutes_days).quantize(Decimal("0.001"))


async def get_data_many_groups(
    groups: tuple[str, ...], loaders: Dataloaders
) -> Decimal:
    groups_data: tuple[Decimal, ...] = await collect(
        tuple(get_data_one_group(group, loaders) for group in groups),
        workers=32,
    )

    return Decimal(sum(group for group in groups_data))


def format_data(days: Decimal) -> dict:
    return {
        "fontSizeRatio": 0.5,
        "text": days.to_integral_exact(rounding=ROUND_CEILING),
    }


def format_csv_data(days: Decimal) -> utils.CsvData:
    return utils.CsvData(
        headers=["Days until zero exposure"],
        rows=[[str(days.to_integral_exact(rounding=ROUND_CEILING))]],
    )


async def generate_all() -> None:
    days: Decimal
    loaders: Dataloaders = get_new_context()
    async for group in utils.iterate_groups():
        days = await get_data_one_group(group, loaders)
        utils.json_dump(
            document=format_data(
                days=days,
            ),
            entity="group",
            subject=group,
            csv_document=format_csv_data(days=days),
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        days = await get_data_many_groups(org_groups, loaders)
        utils.json_dump(
            document=format_data(
                days=days,
            ),
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(days=days),
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            days = await get_data_many_groups(tuple(groups), loaders)
            utils.json_dump(
                document=format_data(
                    days=days,
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(days=days),
            )


if __name__ == "__main__":
    run(generate_all())
