from aioextensions import (
    collect,
)
from collections.abc import (
    Iterable,
)
from custom_exceptions import (
    CredentialNotFound,
    RootAlreadyCloning,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsRequest,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.events.types import (
    Event,
)
from db_model.roots.types import (
    GitRoot,
)
import logging
import logging.config
import pytz
from roots import (
    utils as roots_utils,
)
from settings.logger import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


def filter_active_roots_with_credentials(
    roots: tuple[GitRoot, ...],
) -> tuple[GitRoot, ...]:
    valid_roots = tuple(
        root
        for root in roots
        if root.state.credential_id is not None
        # The https public repositories can be cloned without credentials
        or root.state.url.startswith("http")
    )
    if roots and not valid_roots:
        raise CredentialNotFound()

    if len(roots) != len(valid_roots):
        LOGGER.warning(
            "The group does not have root credentials",
            extra={"extra": {"group_name": roots[0].group_name}},
        )
    return valid_roots


async def filter_roots_unsolved_events(
    roots: tuple[GitRoot, ...], loaders: Dataloaders, group_name: str
) -> tuple[GitRoot, ...]:
    unsolved_events_by_root: dict[
        str, tuple[Event, ...]
    ] = await roots_utils.get_unsolved_events_by_root(loaders, group_name)
    roots_with_unsolved_events: tuple[str, ...] = tuple(
        root.id for root in roots if root.id in unsolved_events_by_root
    )
    await collect(
        [
            roots_utils.update_root_cloning_status(
                loaders=loaders,
                group_name=group_name,
                root_id=root_id,
                status=GitCloningStatus.FAILED,
                message="Git root has unsolved events",
            )
            for root_id in roots_with_unsolved_events
        ]
    )

    return tuple(
        root for root in roots if root.id not in roots_with_unsolved_events
    )


async def filter_roots_already_in_queue(
    roots: Iterable[GitRoot],
) -> tuple[GitRoot, ...]:
    valid_roots = tuple(
        root
        for root in roots
        if root.cloning.status
        not in (GitCloningStatus.CLONING, GitCloningStatus.QUEUED)
        or (
            root.cloning.status == GitCloningStatus.CLONING
            and (
                datetime.now(tz=pytz.UTC)
                - root.cloning.modified_date.replace(tzinfo=pytz.UTC)
            ).total_seconds()
            / 60
            > 60
        )
    )
    if not valid_roots:
        raise RootAlreadyCloning()

    return valid_roots


async def filter_roots_working_creds(  # pylint: disable=too-many-arguments
    roots: Iterable[GitRoot],
    loaders: Dataloaders,
    group_name: str,
    organization_id: str,
    force: bool,
    queue_with_vpn: bool | None,
) -> tuple[GitRoot, ...]:
    roots_credentials: list[
        Credentials | None
    ] = await loaders.credentials.load_many(
        [
            CredentialsRequest(
                id=root.state.credential_id,
                organization_id=organization_id,
            )
            for root in roots
            if root.state.credential_id is not None
        ]
    )
    roots_credentials = [
        next(
            (
                cred
                for cred in roots_credentials
                if cred and root.state.credential_id == cred.id
            ),
            None,
        )
        for root in roots
    ]
    roots_last_commits = await collect(
        (
            roots_utils.get_commit_last_sucessful_clone(
                loaders=loaders, root=root
            )
            for root in roots
        ),
        workers=15,
    )

    last_root_commits_in_s3: tuple[
        tuple[GitRoot, str | None, str | None, bool], ...
    ] = tuple(
        zip(
            roots,
            roots_last_commits,
            tuple(
                await collect(
                    roots_utils.ls_remote_root(root, credential, loaders)
                    for root, credential in zip(roots, roots_credentials)
                )
            ),
            tuple(
                await collect(
                    roots_utils.is_in_s3(group_name, root.state.nickname)
                    for root in roots
                )
            ),
        )
    )

    roots_with_issues: tuple[tuple[GitRoot, str | None], ...] = tuple(
        (root, last_commit)
        for root, last_commit, commit, _ in last_root_commits_in_s3
        if commit is None and not root.state.use_vpn
    )
    await collect(
        [
            roots_utils.update_root_cloning_status(
                loaders=loaders,
                group_name=group_name,
                root_id=root.id,
                status=GitCloningStatus.FAILED,
                message="Invalid credentials",
                commit=last_commit,
            )
            for root, last_commit in roots_with_issues
        ]
    )

    unchanged_roots: tuple[tuple[GitRoot, str | None], ...] = tuple(
        (root, last_commit)
        for (
            root,
            last_commit,
            commit,
            has_mirror_in_s3,
        ) in last_root_commits_in_s3
        if (
            commit is not None
            and commit == last_commit
            and has_mirror_in_s3
            and force is False
        )
    )
    await collect(
        [
            roots_utils.update_root_cloning_status(
                loaders=loaders,
                group_name=group_name,
                root_id=root.id,
                status=GitCloningStatus.OK,
                message=(
                    "The repository was not cloned as"
                    " no new changes were detected"
                ),
                commit=last_commit,
            )
            for root, last_commit in unchanged_roots
        ]
    )

    valid_roots = tuple(
        root
        for (
            root,
            last_commit,
            commit,
            has_mirror_in_s3,
        ) in last_root_commits_in_s3
        if (
            commit is not None
            and (
                commit != last_commit or not has_mirror_in_s3 or force is True
            )
        )
        or (queue_with_vpn and root.state.use_vpn)
    )

    return valid_roots
