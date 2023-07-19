# type: ignore

# pylint: disable=invalid-name
"""
Fix the attacked lines since the last migration from the services repo does not
take into account the loc.

Execution Time:     2022-02-18 at 15:25:41 UTC
Finalization Time:  2022-02-18 at 15:29:33 UTC

Execution Time:     2022-04-21 at 19:53:58 UTC
Finalization Time:  2022-04-21 at 19:58:39 UTC
"""

from aioextensions import (
    collect,
    run,
)
from custom_exceptions import (
    ToeLinesAlreadyUpdated,
)
from custom_utils import (
    datetime as datetime_utils,
)
from dataloaders import (
    get_new_context,
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
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER_CONSOLE = logging.getLogger("console")


@retry_on_exceptions(
    exceptions=(UnavailabilityError, ToeLinesAlreadyUpdated),
)
async def process_group_lines(
    current_toe_lines: ToeLines,
) -> None:
    if current_toe_lines.state.attacked_lines > current_toe_lines.state.loc:
        new_attacked_lines = current_toe_lines.state.loc
        await toe_lines_model.update_state(
            current_value=current_toe_lines,
            new_state=current_toe_lines.state._replace(
                attacked_lines=new_attacked_lines,
                modified_by="machine@fluidattacks.com",
                modified_date=datetime_utils.get_utc_now(),
            ),
        )


async def main() -> None:
    loaders = get_new_context()
    group_names = tuple(
        group["project_name"]
        for group in await groups_domain.get_all(attributes=["project_name"])
    )
    LOGGER_CONSOLE.info("Getting lines", extra={"extra": {}})
    groups_toe_lines_connections = await loaders.group_toe_lines.load_many(
        [
            GroupToeLinesRequest(group_name=group_name)
            for group_name in group_names
        ]
    )
    groups_len = len(group_names)
    for (
        index,
        group_toe_lines_connection,
        group_name,
    ) in zip(
        range(groups_len),
        groups_toe_lines_connections,
        group_names,
    ):
        await collect(
            tuple(
                process_group_lines(toe_lines)
                for toe_lines in [
                    edge.node for edge in group_toe_lines_connection.edges
                ]
            ),
            workers=1000,
        )
        LOGGER_CONSOLE.info(
            "Group updated",
            extra={
                "extra": {
                    "group_name": group_name,
                    "progress": str(index / groups_len),
                }
            },
        )


if __name__ == "__main__":
    run(main())
