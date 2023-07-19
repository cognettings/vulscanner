from custom_exceptions import (
    CredentialNotFound,
    ErrorUpdatingCredential,
    GroupNotFound,
    InvalidParameter,
    RootAlreadyCloning,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.enums import (
    GroupService,
)
from organizations import (
    domain as orgs_domain,
)
from roots import (
    domain as roots_domain,
)
from typing import (
    NamedTuple,
)


class QuequeResult(NamedTuple):
    success: bool
    group: str
    message: str | None = None


async def _queue_sync_git_roots(
    *,
    loaders: Dataloaders,
    group_name: str,
) -> QuequeResult:
    success = False
    message: str | None = None
    try:
        result = await roots_domain.queue_sync_git_roots(
            loaders=loaders,
            group_name=group_name,
            queue_with_vpn=None,
        )
        if result is not None:
            success = result.success
    except (
        InvalidParameter,
        CredentialNotFound,
        RootAlreadyCloning,
        GroupNotFound,
        ErrorUpdatingCredential,
    ) as exc:
        message = str(exc)

    return QuequeResult(success, group_name, message)


async def clone_groups_roots() -> None:
    loaders: Dataloaders = get_new_context()
    groups = await orgs_domain.get_all_active_groups(loaders)
    machine_groups: list[str] = [
        group.name
        for group in groups
        if group.state.has_machine is True
        and group.state.service == GroupService.WHITE
    ]
    for group in machine_groups:
        await _queue_sync_git_roots(
            loaders=loaders,
            group_name=group,
        )


async def main() -> None:
    await clone_groups_roots()
