from aioextensions import (
    collect,
)
from batch.dal import (
    delete_action,
)
from batch.types import (
    BatchProcessing,
)
from custom_exceptions import (
    RepeatedToeInput,
    ToeInputAlreadyUpdated,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
    RootRequest,
    URLRoot,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
    ToeInput,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from toe.inputs import (
    domain as toe_inputs_domain,
)
from toe.inputs.types import (
    ToeInputAttributesToUpdate,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


toe_inputs_remove = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_inputs_domain.remove)
toe_inputs_update = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_inputs_domain.update)


def get_non_present_toe_inputs_to_update(
    root: GitRoot | URLRoot,
    root_toe_inputs: tuple[ToeInput, ...],
) -> tuple[tuple[ToeInput, ToeInputAttributesToUpdate], ...]:
    LOGGER.info(
        "Getting non present toe inputs to update",
        extra={
            "extra": {
                "repo_nickname": root.state.nickname,
            }
        },
    )
    return tuple(
        (
            toe_input,
            ToeInputAttributesToUpdate(be_present=False),
        )
        for toe_input in root_toe_inputs
        if root.state.status == RootStatus.INACTIVE
        and toe_input.state.be_present
        and toe_input.state.seen_at is not None
    )


def get_toe_inputs_to_remove(
    root: GitRoot | URLRoot,
    root_toe_inputs: tuple[ToeInput, ...],
) -> tuple[ToeInput, ...]:
    LOGGER.info(
        "Getting toe inputs to remove",
        extra={
            "extra": {
                "repo_nickname": root.state.nickname,
            }
        },
    )
    return tuple(
        toe_input
        for toe_input in root_toe_inputs
        if root.state.status == RootStatus.INACTIVE
        and toe_input.state.seen_at is None
    )


def get_present_toe_inputs_to_update(
    root: GitRoot | URLRoot,
    root_toe_inputs: tuple[ToeInput, ...],
) -> tuple[tuple[ToeInput, ToeInputAttributesToUpdate], ...]:
    LOGGER.info(
        "Getting present toe inputs to update",
        extra={
            "extra": {
                "repo_nickname": root.state.nickname,
            }
        },
    )
    return tuple(
        (
            toe_input,
            ToeInputAttributesToUpdate(be_present=True),
        )
        for toe_input in root_toe_inputs
        if root.state.status == RootStatus.ACTIVE
        and not toe_input.state.be_present
    )


async def refresh_active_root_toe_inputs(
    loaders: Dataloaders,
    group_name: str,
    root: GitRoot | URLRoot,
) -> None:
    LOGGER.info(
        "Refreshing active toe inputs",
        extra={
            "extra": {
                "repo_nickname": root.state.nickname,
            }
        },
    )
    group_toe_inputs = await loaders.group_toe_inputs.load_nodes(
        GroupToeInputsRequest(group_name=group_name)
    )
    root_toe_inputs = tuple(
        toe_input
        for toe_input in group_toe_inputs
        if toe_input.state.unreliable_root_id == root.id
    )
    present_toe_inputs_to_update = get_present_toe_inputs_to_update(
        root, root_toe_inputs
    )
    await collect(
        tuple(
            toe_inputs_update(
                current_value=current_value,
                attributes=attrs_to_update,
                modified_by="machine@fluidattacks.com",
                is_moving_toe_input=True,
            )
            for current_value, attrs_to_update in (
                present_toe_inputs_to_update
            )
        ),
    )
    LOGGER.info(
        "Finish refreshing active toe inputs",
        extra={
            "extra": {
                "repo_nickname": root.state.nickname,
            }
        },
    )


async def refresh_inactive_root_toe_inputs(
    loaders: Dataloaders,
    group_name: str,
    root: GitRoot | URLRoot,
) -> None:
    LOGGER.info(
        "Refreshing inactive toe inputs",
        extra={
            "extra": {
                "repo_nickname": root.state.nickname,
            }
        },
    )
    group_toe_inputs = await loaders.group_toe_inputs.load_nodes(
        GroupToeInputsRequest(group_name=group_name)
    )
    root_toe_inputs = tuple(
        toe_input
        for toe_input in group_toe_inputs
        if toe_input.state.unreliable_root_id == root.id
    )
    non_present_toe_inputs_to_update = get_non_present_toe_inputs_to_update(
        root, root_toe_inputs
    )
    await collect(
        tuple(
            toe_inputs_update(
                current_value=current_value,
                attributes=attrs_to_update,
                modified_by="machine@fluidattacks.com",
                is_moving_toe_input=True,
            )
            for current_value, attrs_to_update in (
                non_present_toe_inputs_to_update
            )
        ),
    )
    toe_inputs_to_remove = get_toe_inputs_to_remove(root, root_toe_inputs)
    await collect(
        tuple(
            toe_inputs_remove(toe_input) for toe_input in toe_inputs_to_remove
        ),
    )
    LOGGER.info(
        "Finish refreshing inactive toe inputs",
        extra={
            "extra": {
                "repo_nickname": root.state.nickname,
            }
        },
    )


@retry_on_exceptions(
    exceptions=(
        RepeatedToeInput,
        ToeInputAlreadyUpdated,
    ),
)
async def refresh_root_toe_inputs(
    group_name: str, optional_repo_nickname: str | None
) -> None:
    loaders = get_new_context()
    roots = await loaders.group_roots.load(group_name)
    # There are roots with the same nickname
    # then it is going to take the last modified root
    sorted_roots = sorted(
        roots,
        key=lambda root: root.state.modified_date,
    )
    active_roots = {
        root.state.nickname: root
        for root in sorted_roots
        if isinstance(root, (GitRoot, URLRoot))
        and root.state.status == RootStatus.ACTIVE
    }
    # Deactivate all the toe inputs for all the inactive roots
    # with the same nickname
    inactive_roots = tuple(
        root
        for root in sorted_roots
        if isinstance(root, (GitRoot, URLRoot))
        and root.state.status == RootStatus.INACTIVE
        and root.state.nickname not in active_roots
    )
    active_roots_to_proccess = tuple(
        root
        for root in active_roots.values()
        if not optional_repo_nickname
        or root.state.nickname == optional_repo_nickname
    )
    for root in active_roots_to_proccess:
        await refresh_active_root_toe_inputs(loaders, group_name, root)
    inactive_roots_to_proccess = tuple(
        root_repo
        for root_repo in inactive_roots
        if not optional_repo_nickname
        or root_repo.state.nickname == optional_repo_nickname
    )
    for root in inactive_roots_to_proccess:
        await refresh_inactive_root_toe_inputs(loaders, group_name, root)


async def refresh_toe_inputs(*, item: BatchProcessing) -> None:
    group_name: str = item.entity
    optional_repo_nickname: str | None = (
        None if item.additional_info == "*" else item.additional_info
    )
    await refresh_root_toe_inputs(group_name, optional_repo_nickname)
    await delete_action(
        action_name=item.action_name,
        additional_info=item.additional_info,
        entity=item.entity,
        subject=item.subject,
        time=item.time,
    )


async def refresh_toe_inputs_simple_args(
    group_name: str, url_root_id: str
) -> None:
    loaders = get_new_context()
    url_root = await loaders.root.load(RootRequest(group_name, url_root_id))
    if not url_root or not isinstance(url_root, URLRoot):
        return

    if url_root.state.status == RootStatus.ACTIVE:
        await refresh_active_root_toe_inputs(loaders, group_name, url_root)
    else:
        await refresh_inactive_root_toe_inputs(loaders, group_name, url_root)
