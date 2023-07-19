from aioextensions import (
    collect,
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
    bugsnag as bugsnag_utils,
    datetime as datetime_utils,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timedelta,
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
from schedulers.common import (
    info,
)

MAX_DAYS_SINCE_ATTACKED = 90

bugsnag_utils.start_scheduler_session()


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
    ),
    sleep_seconds=20,
    max_attempts=10,
)
async def update_toe_lines(
    current_value: ToeLines,
    sorts_risk_level: int,
    sorts_priority_factor: int,
    sorts_risk_level_date: datetime | None,
) -> None:
    await toe_lines_model.update_state(
        current_value=current_value,
        new_state=current_value.state._replace(
            modified_date=datetime_utils.get_utc_now(),
            sorts_risk_level=sorts_risk_level,
            sorts_priority_factor=sorts_priority_factor,
            sorts_risk_level_date=sorts_risk_level_date,
        ),
    )


async def update_priority_factor(group_toe_lines: list[ToeLines]) -> None:
    updates = []
    for toe_line in group_toe_lines:
        if toe_line.state.sorts_risk_level != -1:
            days_since_attacked = (
                datetime_utils.get_utc_now() - toe_line.state.attacked_at
                if toe_line.state.attacked_at is not None
                else timedelta(days=90)
            )
            sorts_priority_factor = (
                2 * toe_line.state.sorts_risk_level
                + min(days_since_attacked.days, MAX_DAYS_SINCE_ATTACKED)
            ) / (MAX_DAYS_SINCE_ATTACKED + 200)
            updates.append(
                update_toe_lines(
                    toe_line,
                    toe_line.state.sorts_risk_level,
                    int(sorts_priority_factor * 100),
                    toe_line.state.sorts_risk_level_date,
                ),
            )

    info(
        f"Updating {len(updates)} toe lines Priority Factors "
        f"of {len(group_toe_lines)} total present toe lines"
    )

    await collect(tuple(updates))


async def process_group(group_name: str) -> None:
    loaders: Dataloaders = get_new_context()
    info(f"Processing group {group_name}")

    group_toe_lines = await loaders.group_toe_lines.load_nodes(
        GroupToeLinesRequest(group_name=group_name, be_present=True)
    )

    try:
        await update_priority_factor(group_toe_lines)
    except (
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
    ) as exc:
        info(
            f"Group {group_name} could not be updated",
            extra={"extra": {"error": exc}},
        )
    else:
        info(f"ToeLines's Priority Factors for {group_name} updated")


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(await orgs_domain.get_all_active_group_names(loaders))

    await collect(
        tuple(process_group(group_name) for group_name in group_names),
        workers=1,
    )
