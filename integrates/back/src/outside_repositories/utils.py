from aioextensions import (
    collect,
    in_thread,
)
import asyncio
from botocore.exceptions import (
    ClientError,
)
from dataloaders import (
    Dataloaders,
)
from db_model.azure_repositories.types import (
    RepositoriesStats,
)
from db_model.credentials.types import (
    Credentials,
)
from db_model.integration_repositories.remove import (
    remove,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
from db_model.integration_repositories.update import (
    update_unreliable_repositories,
)
from db_model.organizations.types import (
    Organization,
    OrganizationUnreliableIndicatorsToUpdate,
)
from db_model.organizations.update import (
    update_unreliable_org_indicators,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from git.cmd import (
    Git,
)
from itertools import (
    chain,
)
import logging
import logging.config
from organizations.domain import (
    get_group_names,
)
import os
from outside_repositories.domain import (
    clone_mirrors,
    get_azure_credentials_authors_stats,
    get_azure_credentials_stats,
    get_bitbucket_credentials_authors,
    get_bitbucket_credentials_stats,
    get_github_credentials_authors,
    get_github_credentials_stats,
    get_gitlab_credentials_authors,
    get_gitlab_credentials_stats,
    get_pat_credentials_authors_stats,
    get_pat_credentials_stats,
)
import re
from settings import (
    LOGGING,
)
import tempfile
from urllib.parse import (
    unquote_plus,
    urlparse,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def get_covered_nickname_authors(
    path: str, folder: str, group: str, git_root: GitRoot
) -> set[str]:
    proc = await asyncio.create_subprocess_exec(
        "git",
        "-C",
        os.path.join(path, folder),
        "shortlog",
        "-sne",
        git_root.state.branch,
        "--",
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL,
    )
    stdout, stderr = await proc.communicate()

    if proc.returncode == 0:
        pattern = r"(?<=\<).+(?=\>)"
        authors = re.findall(pattern, stdout.decode())

        return set(author.lower() for author in authors)

    LOGGER.error(
        "Error getting data over repository",
        extra={
            "extra": {
                "error": stderr.decode(),
                "out": stdout.decode(),
                "group": group,
                "repository": os.path.join(path, folder),
                "branch": git_root.state.branch,
            }
        },
    )

    return set()


async def get_covered_nickname(
    path: str, folder: str, group: str, git_root: GitRoot
) -> set[str]:
    if folder != git_root.state.nickname:
        return set()

    Git().execute(
        [
            "git",
            "config",
            "--global",
            "--add",
            "safe.directory",
            os.path.join(path, folder),
        ]
    )

    return await get_covered_nickname_authors(path, folder, group, git_root)


async def get_covered_group(
    path: str, folder: str, group: str, git_roots: tuple[GitRoot, ...]
) -> set[str]:
    group_foder_coverted: tuple[set[str], ...] = await collect(
        tuple(
            get_covered_nickname(path, folder, group, git_root)
            for git_root in git_roots
        ),
        workers=1,
    )

    return set(set().union(*list(authors for authors in group_foder_coverted)))


async def update_organization_unreliable(  # pylint: disable=too-many-locals
    *,
    organization: Organization,
    loaders: Dataloaders,
    progress: float,
    all_group_names: set[str],
) -> None:
    organization_group_names = await get_group_names(loaders, organization.id)
    organization_group_names = list(
        all_group_names.intersection(
            set(group.lower() for group in organization_group_names)
        )
    )
    if not organization_group_names:
        await update_unreliable_org_indicators(
            organization_id=organization.id,
            organization_name=organization.name,
            indicators=OrganizationUnreliableIndicatorsToUpdate(
                covered_authors=0,
                missed_authors=0,
            ),
        )
        LOGGER.info(
            "Updated covered commit stats for organization",
            extra={
                "extra": {
                    "organization_id": organization.id,
                    "organization_name": organization.name,
                    "progress": round(progress, 2),
                    "active_git_roots": 0,
                    "covered_authors": 0,
                }
            },
        )

        return

    groups_roots = await loaders.group_roots.load_many(
        organization_group_names
    )
    covered_organization: list[set[str]] = []
    for group, roots in zip(organization_group_names, groups_roots):
        active_git_roots: tuple[GitRoot, ...] = tuple(
            root
            for root in roots
            if (
                isinstance(root, GitRoot)
                and root.state.status == RootStatus.ACTIVE
            )
        )

        with tempfile.TemporaryDirectory(
            prefix="integrates_azure_", ignore_cleanup_errors=True
        ) as tmpdir:
            clone_path, clone_repos = await in_thread(
                clone_mirrors, tmpdir=tmpdir, group=group
            )
            covered_group = await collect(
                (
                    get_covered_group(
                        path=clone_path,
                        folder=repo,
                        group=group,
                        git_roots=active_git_roots,
                    )
                    for repo in clone_repos
                ),
                workers=1,
            )

            covered_organization.append(
                set(set().union(*list(authors for authors in covered_group)))
            )

    credentials: list[
        Credentials
    ] = await loaders.organization_credentials.load(organization.id)
    urls = {
        unquote_plus(urlparse(root.state.url.lower()).path)
        for root in tuple(chain.from_iterable(groups_roots))
        if isinstance(root, GitRoot)
    }
    nicknames = {
        root.state.nickname.lower()
        for root in tuple(chain.from_iterable(groups_roots))
        if isinstance(root, GitRoot)
    }
    authors_stats: tuple[set[str], ...] = await collect(
        [
            get_pat_credentials_authors_stats(
                credentials=credentials,
                urls=urls,
                nicknames=nicknames,
                loaders=loaders,
            ),
            get_gitlab_credentials_authors(
                credentials=credentials,
                urls=urls,
                nicknames=nicknames,
                loaders=loaders,
            ),
            get_github_credentials_authors(
                credentials=credentials,
                urls=urls,
                nicknames=nicknames,
            ),
            get_azure_credentials_authors_stats(
                credentials=credentials,
                urls=urls,
                nicknames=nicknames,
                loaders=loaders,
                organization_id=organization.id,
            ),
            get_bitbucket_credentials_authors(
                credentials=credentials,
                urls=urls,
                nicknames=nicknames,
                loaders=loaders,
            ),
        ],
        workers=1,
    )

    await update_unreliable_org_indicators(
        organization_id=organization.id,
        organization_name=organization.name,
        indicators=OrganizationUnreliableIndicatorsToUpdate(
            covered_authors=len(set(set().union(*list(covered_organization)))),
            missed_authors=len(set().union(*list(authors_stats))),
        ),
    )
    LOGGER.info(
        "Updated covered commit stats for organization",
        extra={
            "extra": {
                "organization_id": organization.id,
                "organization_name": organization.name,
                "progress": round(progress, 2),
                "active_git_roots": len(active_git_roots),
                "covered_authors": len(
                    set(set().union(*list(covered_organization)))
                ),
                "missed_authors": len(list(set().union(*list(authors_stats)))),
            }
        },
    )


async def _update(
    *,
    organization_id: str,
    organization_name: str,
    repositories: tuple[RepositoriesStats, ...],
    covered_repositores: int,
) -> None:
    org_repositories: tuple[OrganizationIntegrationRepository, ...] = tuple(
        {
            repo.id: repo
            for repo in chain.from_iterable(
                repository.repositories for repository in repositories
            )
        }.values()
    )

    await collect(
        tuple(
            update_unreliable_repositories(repository=repository)
            for repository in org_repositories
        ),
        workers=4,
    )

    await update_unreliable_org_indicators(
        organization_id=organization_id,
        organization_name=organization_name,
        indicators=OrganizationUnreliableIndicatorsToUpdate(
            missed_repositories=len(org_repositories),
            covered_repositories=covered_repositores,
        ),
    )


async def _remove(
    *,
    organization_id: str,
    valid_repositories_ids: set[str],
    loaders: Dataloaders,
) -> None:
    current_unreliable_repositories = (
        await loaders.organization_unreliable_integration_repositories.load(
            (organization_id, None, None)
        )
    )
    to_remove: tuple[OrganizationIntegrationRepository, ...] = tuple(
        repository
        for repository in current_unreliable_repositories
        if repository.id not in valid_repositories_ids
    )

    await collect(
        tuple(remove(repository=repository) for repository in to_remove),
        workers=4,
    )


async def get_credentials_repositories(
    loaders: Dataloaders, credentials: Credentials
) -> tuple[OrganizationIntegrationRepository, ...]:
    groups = await loaders.organization_groups.load(
        credentials.organization_id
    )
    urls: set[str] = {
        unquote_plus(urlparse(root.state.url.lower()).path)
        for root in await loaders.group_roots.load_many_chained(
            [group.name for group in groups]
        )
        if isinstance(root, GitRoot)
    }
    nicknames = {
        root.state.nickname.lower()
        for root in await loaders.group_roots.load_many_chained(
            [group.name for group in groups]
        )
        if isinstance(root, GitRoot)
    }
    organization_id = credentials.organization_id
    repositories_stats: tuple[RepositoriesStats, ...] = await collect(
        [
            get_pat_credentials_stats(
                credentials=[credentials],
                urls=urls,
                nicknames=nicknames,
                loaders=loaders,
                organization_id=organization_id,
            ),
            get_gitlab_credentials_stats(
                credentials=[credentials],
                urls=urls,
                nicknames=nicknames,
                loaders=loaders,
                organization_id=organization_id,
            ),
            get_github_credentials_stats(
                credentials=[credentials],
                urls=urls,
                nicknames=nicknames,
                organization_id=organization_id,
            ),
            get_azure_credentials_stats(
                credentials=[credentials],
                loaders=loaders,
                urls=urls,
                nicknames=nicknames,
                organization_id=organization_id,
            ),
            get_bitbucket_credentials_stats(
                credentials=[credentials],
                loaders=loaders,
                urls=urls,
                nicknames=nicknames,
                organization_id=organization_id,
            ),
        ],
        workers=1,
    )
    repositories = tuple(
        repo
        for repo in chain.from_iterable(
            repository.repositories for repository in repositories_stats
        )
    )

    cred_repositories = tuple(
        {repo.id: repo for repo in repositories}.values()
    )

    await collect(
        tuple(
            update_unreliable_repositories(repository=repository)
            for repository in cred_repositories
        ),
        workers=4,
    )

    return repositories


async def update_organization_repositories(
    *,
    organization: Organization,
    loaders: Dataloaders,
    progress: float,
    all_group_names: set[str],
) -> None:
    organization_group_names = await get_group_names(loaders, organization.id)
    organization_group_names = list(
        all_group_names.intersection(
            set(group.lower() for group in organization_group_names)
        )
    )
    if not organization_group_names:
        await update_unreliable_org_indicators(
            organization_id=organization.id,
            organization_name=organization.name,
            indicators=OrganizationUnreliableIndicatorsToUpdate(
                missed_repositories=0,
                covered_repositories=0,
            ),
        )
        LOGGER.info(
            "Organization integration repositories processed",
            extra={
                "extra": {
                    "organization_id": organization.id,
                    "organization_name": organization.name,
                    "progress": round(progress, 2),
                }
            },
        )

        return

    credentials: list[
        Credentials
    ] = await loaders.organization_credentials.load(organization.id)
    groups_roots = await loaders.group_roots.load_many_chained(
        organization_group_names
    )
    urls: set[str] = {
        unquote_plus(urlparse(root.state.url.lower()).path)
        for root in groups_roots
        if isinstance(root, GitRoot)
    }
    nicknames = {
        root.state.nickname.lower()
        for root in groups_roots
        if isinstance(root, GitRoot)
    }
    active_urls: set[str] = {
        unquote_plus(urlparse(root.state.url.lower()).path)
        for root in groups_roots
        if isinstance(root, GitRoot) and root.state.status == RootStatus.ACTIVE
    }
    if not credentials:
        return

    repositories_stats: tuple[RepositoriesStats, ...] = await collect(
        [
            get_pat_credentials_stats(
                credentials=credentials,
                urls=urls,
                nicknames=nicknames,
                loaders=loaders,
                organization_id=organization.id,
            ),
            get_gitlab_credentials_stats(
                credentials=credentials,
                urls=urls,
                nicknames=nicknames,
                loaders=loaders,
                organization_id=organization.id,
            ),
            get_github_credentials_stats(
                credentials=credentials,
                urls=urls,
                nicknames=nicknames,
                organization_id=organization.id,
            ),
            get_azure_credentials_stats(
                credentials=credentials,
                loaders=loaders,
                urls=urls,
                nicknames=nicknames,
                organization_id=organization.id,
            ),
            get_bitbucket_credentials_stats(
                credentials=credentials,
                loaders=loaders,
                urls=urls,
                nicknames=nicknames,
                organization_id=organization.id,
            ),
        ],
        workers=1,
    )

    try:
        await _update(
            organization_id=organization.id,
            organization_name=organization.name,
            repositories=repositories_stats,
            covered_repositores=len(active_urls),
        )
        await _remove(
            organization_id=organization.id,
            valid_repositories_ids={
                f"URL#{repository.id}#BRANCH#{repository.branch.lower()}"
                for stats in repositories_stats
                for repository in stats.repositories
            },
            loaders=loaders,
        )

        LOGGER.info(
            "Organization integration repositories processed",
            extra={
                "extra": {
                    "organization_id": organization.id,
                    "organization_name": organization.name,
                    "progress": round(progress, 2),
                    "covered_repositores": len(active_urls),
                }
            },
        )
    except (ClientError, TypeError, UnavailabilityError) as ex:
        msg: str = (
            "Error: An error ocurred updating integration "
            "repositories in the database"
        )
        LOGGER.error(
            msg,
            extra={
                "extra": {
                    "organization_id": organization.id,
                    "organization_name": organization.name,
                    "ex": ex,
                }
            },
        )
