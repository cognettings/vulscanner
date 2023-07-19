# type: ignore

# pylint: disable=invalid-name,missing-kwoa
"""
Format toe input component with port and protocol.

Execution Time:     2022-01-27 at 21:26:57 UTC
Finalization Time:  2022-01-27 at 22:11:23 UTC

Execution Time:     2022-01-28 at 15:55:42 UTC
Finalization Time:  2022-01-28 at 15:58:25 UTC
"""

from aioextensions import (
    collect,
    run,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    RepeatedToeInput,
)
from custom_types import (  # pylint: disable=import-error
    Group,
)
from custom_utils.datetime import (
    get_iso_date,
)
from dataloaders import (
    get_new_context,
)
from db_model import (
    toe_inputs as toe_inputs_model,
)
from db_model.roots.types import (
    RootItem,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
    ToeInput,
    ToeInputState,
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
from toe.inputs import (
    domain as toe_inputs_domain,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER_CONSOLE = logging.getLogger("console")


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
)
async def add_input(
    current_toe_input: ToeInput,
    new_root_id: str,
    new_component: str,
) -> None:
    new_toe_input = ToeInput(
        component=new_component,
        entry_point=current_toe_input.entry_point,
        group_name=current_toe_input.group_name,
        state=ToeInputState(
            attacked_at=current_toe_input.state.attacked_at,
            attacked_by=current_toe_input.state.attacked_by,
            be_present=current_toe_input.state.be_present,
            be_present_until=current_toe_input.state.be_present_until,
            first_attack_at=current_toe_input.state.first_attack_at,
            has_vulnerabilities=current_toe_input.state.has_vulnerabilities,
            modified_by="machine@fluidattacks.com",
            modified_date=get_iso_date(),
            seen_at=current_toe_input.state.seen_at,
            seen_first_time_by=current_toe_input.state.seen_first_time_by,
            unreliable_root_id=new_root_id,
        ),
        unreliable_root_id=new_root_id,
    )
    await toe_inputs_model.add(toe_input=new_toe_input)


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
)
async def remove_input(
    current_toe_input: ToeInput,
) -> None:
    await toe_inputs_model.remove(
        entry_point=current_toe_input.entry_point,
        component=current_toe_input.component,
        group_name=current_toe_input.group_name,
    )


async def process_input(
    current_toe_input: ToeInput,
    group_roots: tuple[RootItem, ...],
    group: Group,
) -> None:
    root, component = toe_inputs_domain.get_unreliable_component_legacy(
        current_toe_input.component, group_roots, group
    )
    new_component = ""
    if component is not None:
        new_component = component
    new_root_id = ""
    if root is not None:
        new_root_id = root.id

    if (
        new_root_id != current_toe_input.state.unreliable_root_id
        or current_toe_input.component != new_component
    ):
        with suppress(RepeatedToeInput):
            await add_input(current_toe_input, new_root_id, new_component)
        await remove_input(current_toe_input)


async def main() -> None:
    loaders = get_new_context()
    group_names = tuple(
        group["project_name"]
        for group in await groups_domain.get_all(attributes=["project_name"])
    )
    LOGGER_CONSOLE.info("Getting groups")
    groups: list[Group] = await loaders.group.load_many(group_names)
    LOGGER_CONSOLE.info("Getting roots")
    groups_roots = await loaders.group_roots.load_many(group_names)
    LOGGER_CONSOLE.info("Getting inputs")
    groups_toe_input_connections = await loaders.group_toe_inputs.load_many(
        [
            GroupToeInputsRequest(group_name=group_name)
            for group_name in group_names
        ]
    )
    groups_len = len(groups)
    for (
        index,
        group_toe_input_connection,
        group_roots,
        group,
        group_name,
    ) in zip(
        range(groups_len),
        groups_toe_input_connections,
        groups_roots,
        groups,
        group_names,
    ):
        await collect(
            tuple(
                process_input(toe_input, group_roots, group)
                for toe_input in [
                    edge.node for edge in group_toe_input_connection.edges
                ]
            )
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
