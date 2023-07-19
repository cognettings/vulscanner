from aioextensions import (
    collect,
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
)
from organizations import (
    domain as orgs_domain,
)
from server_async.enqueue import (
    queue_refresh_toe_lines_async,
)


async def process_group(loaders: Dataloaders, group_name: str) -> None:
    roots = tuple(
        root
        for root in (await loaders.group_roots.load(group_name))
        if root.state.status == RootStatus.ACTIVE and isinstance(root, GitRoot)
    )
    await collect(
        [queue_refresh_toe_lines_async(group_name, root.id) for root in roots]
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = await orgs_domain.get_all_active_group_names(loaders)
    await collect(
        [process_group(loaders, group) for group in group_names], workers=20
    )
