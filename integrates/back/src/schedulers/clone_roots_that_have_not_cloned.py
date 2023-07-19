from aioextensions import (
    collect,
)
from custom_exceptions import (
    CredentialNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
import pytz
from roots.utils import (
    queue_sync_root_async,
    update_root_cloning_status,
)
from settings.logger import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


async def process_group(loaders: Dataloaders, group_name: str) -> None:
    all_roots: tuple[GitRoot, ...] = tuple(
        root
        for root in await loaders.group_roots.load(group_name)
        if isinstance(root, GitRoot)
        and root.state.status == RootStatus.ACTIVE
        and root.cloning.status
        in (
            GitCloningStatus.QUEUED,
            GitCloningStatus.CLONING,
            GitCloningStatus.OK,
        )
        and (
            datetime.utcnow().replace(tzinfo=pytz.UTC)
            - root.cloning.modified_date.replace(tzinfo=pytz.UTC)
        ).days
        >= 3
    )
    if all_roots:
        print(f"Queueing {len(all_roots)} for {group_name}")
        await collect(
            [queue_sync_root_async(group_name, root.id) for root in all_roots]
        )

        await collect(
            tuple(
                update_root_cloning_status(
                    loaders=loaders,
                    group_name=group_name,
                    root_id=root.id,
                    status=GitCloningStatus.QUEUED,
                    message="Cloning queued...",
                )
                for root in all_roots
            )
        )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = sorted(
        await orgs_domain.get_all_active_group_names(loaders=loaders)
    )
    try:
        await collect(
            [process_group(loaders, group) for group in groups], workers=10
        )
    except CredentialNotFound as exc:
        LOGGER.exception(exc, extra={"groups": groups})
