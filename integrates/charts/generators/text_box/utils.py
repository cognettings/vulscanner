from aioextensions import (
    collect,
)
from charts.utils import (
    CsvData,
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from collections.abc import (
    Awaitable,
    Callable,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    UnsanitizedInputFound,
)
from custom_utils.validations import (
    validate_sanitized_csv_input,
)
from typing_extensions import (
    TypedDict,
)

ForcesReport = TypedDict("ForcesReport", {"fontSizeRatio": float, "text": str})


def format_csv_data(*, header: str, value: str) -> CsvData:
    headers_row: list[str] = [""]
    with suppress(UnsanitizedInputFound):
        validate_sanitized_csv_input(header)
        headers_row = [header]

    rows: list[list[str]] = [[""]]
    with suppress(UnsanitizedInputFound):
        validate_sanitized_csv_input(value)
        rows = [[value]]

    return CsvData(headers=headers_row, rows=rows)


def format_document(vulns_count: int) -> dict:
    return {
        "fontSizeRatio": 0.5,
        "text": vulns_count,
    }


async def get_data_many_groups(
    groups: tuple[str, ...],
    generate_one: Callable[[str], Awaitable[int]],
) -> int:
    groups_vulns = await collect(map(generate_one, groups), workers=32)

    return sum(groups_vulns)


async def generate_all(
    *,
    get_data_one_group: Callable[[str], Awaitable[int]],
    header: str,
) -> None:
    async for group in iterate_groups():
        document = format_document(
            vulns_count=await get_data_one_group(group),
        )
        json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(
                header=header, value=str(document["text"])
            ),
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        document = format_document(
            vulns_count=await get_data_many_groups(
                org_groups, get_data_one_group
            ),
        )
        json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(
                header=header, value=str(document["text"])
            ),
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            document = format_document(
                vulns_count=await get_data_many_groups(
                    groups, get_data_one_group
                ),
            )
            json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(
                    header=header, value=str(document["text"])
                ),
            )
