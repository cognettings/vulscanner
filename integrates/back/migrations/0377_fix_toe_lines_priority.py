# pylint: disable=invalid-name
# type: ignore
"""
Assign default priority to toe_lines that are out of Sorts' scope

Execution Time:    2023-04-11 at 17:55:14 UTC
Finalization Time: 2023-04-11 at 18:24:27 UTC
"""

from aioextensions import (
    collect,
    run,
)
from aiohttp import (
    ClientConnectorError,
)
from aiohttp.client_exceptions import (
    ClientPayloadError,
    ServerTimeoutError,
)
from botocore.exceptions import (
    ClientError,
    ConnectTimeoutError,
    HTTPClientError,
    ReadTimeoutError,
)
from custom_exceptions import (
    ToeLinesAlreadyUpdated,
)
from custom_utils import (
    datetime as datetime_utils,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model import (
    toe_lines as toe_lines_model,
)
from db_model.toe_lines.types import (
    GroupToeLinesRequest,
    ToeLines,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from organizations import (
    domain as orgs_domain,
)
import time


@retry_on_exceptions(
    exceptions=(
        ClientConnectorError,
        ClientError,
        ClientPayloadError,
        ConnectionResetError,
        ConnectTimeoutError,
        UnavailabilityError,
        HTTPClientError,
        ReadTimeoutError,
        ServerTimeoutError,
        ToeLinesAlreadyUpdated,
    ),
    sleep_seconds=20,
    max_attempts=10,
)
async def update_toe_lines(
    current_value: ToeLines,
    sorts_risk_level: int,
    sorts_risk_level_normalized: int,
    sorts_risk_level_date: datetime,
) -> None:
    await toe_lines_model.update_state(
        current_value=current_value,
        new_state=current_value.state._replace(
            modified_date=datetime_utils.get_utc_now(),
            sorts_risk_level=sorts_risk_level,
            sorts_risk_level_normalized=sorts_risk_level_normalized,
            sorts_risk_level_date=sorts_risk_level_date,
        ),
    )


async def update_toe_lines_priority(
    group_toe_lines: list[ToeLines],
) -> None:
    toe_correction_count = 0
    toes_to_fix = []

    for toe_line in group_toe_lines:
        toe_line_date = (
            toe_line.state.sorts_risk_level_date.replace(tzinfo=None)
            if toe_line.state.sorts_risk_level_date is not None
            else None
        )
        if (
            toe_line_date == datetime(1970, 1, 1)
            and toe_line.state.sorts_risk_level != -1
        ):
            toes_to_fix.append(toe_line)
            toe_correction_count += 1

    print(f"A total of {toe_correction_count} toe lines will be fixed")

    await collect(
        [
            update_toe_lines(toe_line, int(-1), int(-1), datetime(1970, 1, 1))
            for toe_line in toes_to_fix
        ],
        workers=16,
    )


async def process_group(group_name: str) -> None:
    loaders: Dataloaders = get_new_context()
    print(f"Processing toe lines fix for group {group_name}")

    group_toe_lines = await loaders.group_toe_lines.load_nodes(
        GroupToeLinesRequest(group_name=group_name, be_present=True)
    )
    await update_toe_lines_priority(group_toe_lines)

    print(f"Priority fix for group {group_name} completed")


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = await orgs_domain.get_all_active_group_names(loaders)

    await collect(
        tuple(process_group(group_name) for group_name in group_names),
        workers=1,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
