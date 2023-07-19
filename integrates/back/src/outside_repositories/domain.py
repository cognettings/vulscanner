from aioextensions import (
    collect,
    in_thread,
)
from azure.devops.exceptions import (
    AzureDevOpsServiceError,
)
from azure.devops.v6_0.git.models import (
    GitRepository,
)
from contextlib import (
    suppress,
)
from custom_utils.datetime import (
    DEFAULT_ISO_STR,
    get_utc_now,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.azure_repositories.get import (
    get_account_names,
    get_azure_branches_names,
    get_bitbucket_authors,
    get_bitbucket_branches_names,
    get_bitbucket_repositories,
    get_github_branches_names,
    get_github_repos,
    get_github_repos_commits,
    get_gitlab_branches_names,
    get_gitlab_commit,
    get_gitlab_last_commit,
    get_gitlab_projects,
    get_oauth_repositories,
    get_oauth_repositories_commits,
)
from db_model.azure_repositories.types import (
    BasicRepoData,
    CredentialsGitRepository,
    CredentialsGitRepositoryCommit,
    GitRepositoryCommit,
    OGitRepository,
    ProjectStats,
    RepositoriesStats,
)
from db_model.azure_repositories.utils import (
    does_not_exist_in_gitroot_urls,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsRequest,
    OauthAzureSecret,
    OauthBitbucketSecret,
    OauthGithubSecret,
    OauthGitlabSecret,
)
from db_model.credentials.utils import (
    filter_pat_credentials,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
from decorators import (
    retry_on_exceptions,
)
from git_self import (
    pull_repositories,
)
import hashlib
from itertools import (
    chain,
)
import logging
import logging.config
from oauth.azure import (
    get_azure_token,
)
from oauth.bitbucket import (
    get_bitbucket_token,
)
from oauth.gitlab import (
    get_token,
)
import os
from settings import (
    LOGGING,
)
from urllib3.util.url import (
    parse_url,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def clone_mirrors(tmpdir: str, group: str) -> tuple[str, list[str]]:
    os.chdir(tmpdir)
    pull_repositories(
        tmpdir=tmpdir,
        group_name=group,
        optional_repo_nickname=None,
    )
    repositories_path = f"{tmpdir}/groups/{group}"
    os.chdir(repositories_path)
    repositories = [
        _dir for _dir in os.listdir(repositories_path) if os.path.isdir(_dir)
    ]

    return repositories_path, repositories


async def get_pat_credentials_authors_stats(
    credentials: list[Credentials],
    urls: set[str],
    nicknames: set[str],
    loaders: Dataloaders,
) -> set[str]:
    pat_credentials = filter_pat_credentials(credentials)
    all_repositories = (
        await loaders.organization_integration_repositories.load_many(
            pat_credentials
        )
    )
    repositories: tuple[CredentialsGitRepository, ...] = tuple(
        CredentialsGitRepository(
            credential=credential,
            repository=repository,
        )
        for credential, _repositories in zip(pat_credentials, all_repositories)
        for repository in _repositories
        if does_not_exist_in_gitroot_urls(
            repository=repository,
            urls=urls,
            nicknames=nicknames,
        )
    )
    repositories_authors: tuple[set[str], ...] = await collect(
        tuple(
            _get_missed_authors(loaders=loaders, repository=repository)
            for repository in repositories
        ),
        workers=1,
    )

    return set().union(*list(repositories_authors))


async def get_gitlab_credentials_authors(
    *,
    credentials: list[Credentials],
    urls: set[str],
    nicknames: set[str],
    loaders: Dataloaders,
) -> set[str]:
    stats: tuple[ProjectStats, ...] = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    _get_gitlab_credential_stats(
                        credential=credential,
                        urls=urls,
                        nicknames=nicknames,
                        loaders=loaders,
                        get_all=True,
                    )
                    for credential in credentials
                ),
                workers=1,
            )
        )
    )
    filtered_stats: tuple[ProjectStats, ...] = tuple(
        {stat.project.id: stat for stat in stats}.values()
    )

    return {
        commit["author_email"].lower()
        for stat in filtered_stats
        for commit in stat.commits
    }


async def get_github_credentials_authors(
    *,
    credentials: list[Credentials],
    urls: set[str],
    nicknames: set[str],
) -> set[str]:
    stats: tuple[ProjectStats, ...] = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    _get_github_credential_stats(
                        credential=credential,
                        urls=urls,
                        nicknames=nicknames,
                        get_all=True,
                    )
                    for credential in credentials
                ),
                workers=1,
            )
        )
    )
    filtered_stats: tuple[ProjectStats, ...] = tuple(
        {stat.project.id: stat for stat in stats}.values()
    )

    return {
        str(
            commit["author"].get("email") or commit["author"].get("login")
        ).lower()
        for stat in filtered_stats
        for commit in stat.commits
        if commit["author"] is not None
    }


async def get_bitbucket_credentials_authors(
    *,
    credentials: list[Credentials],
    urls: set[str],
    nicknames: set[str],
    loaders: Dataloaders,
) -> set[str]:
    stats: tuple[ProjectStats, ...] = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    _get_bitbucket_credential_stats(
                        credential=credential,
                        urls=urls,
                        nicknames=nicknames,
                        loaders=loaders,
                        get_all=True,
                    )
                    for credential in credentials
                ),
                workers=1,
            )
        )
    )
    filtered_stats: tuple[ProjectStats, ...] = tuple(
        {stat.project.id: stat for stat in stats}.values()
    )

    return {
        str(commit["author"]).lower()
        for stat in filtered_stats
        for commit in stat.commits
    }


async def _get_azure_credentials_tokens(
    *,
    credential: Credentials,
    loaders: Dataloaders,
    organization_id: str,
) -> str:
    _credential = await loaders.credentials.load(
        CredentialsRequest(
            id=credential.id,
            organization_id=organization_id,
        )
    )
    if not _credential:
        return ""

    if isinstance(_credential.state.secret, OauthAzureSecret):
        token = _credential.state.secret.access_token
        if _credential.state.secret.valid_until <= get_utc_now():
            updated_token: str | None = await get_azure_token(
                credential=_credential,
                loaders=loaders,
            )
            if updated_token:
                return updated_token

        return token
    return ""


async def __get_azure_credentials_stats(
    *,
    credential: Credentials,
    loaders: Dataloaders,
    urls: set[str],
    nicknames: set[str],
    organization_id: str,
) -> tuple[OGitRepository, ...]:
    token: str = await _get_azure_credentials_tokens(
        credential=credential,
        loaders=loaders,
        organization_id=organization_id,
    )

    accounts_names = await get_account_names(
        tokens=tuple([token]),
        credentials=[credential],
    )

    all_repositories: tuple[list[list[GitRepository]], ...] = await collect(
        tuple(
            get_oauth_repositories(
                token=token,
                base_urls=tuple(
                    account.base_url for account in _accounts_names
                ),
            )
            for _accounts_names in accounts_names
        ),
        workers=1,
    )

    repositories: tuple[OGitRepository, ...] = tuple(
        OGitRepository(
            token=token,
            repository=repository,
            account=account,
            credential=credential,
            is_oauth=isinstance(credential.state.secret, OauthAzureSecret),
        )
        for _accounts, _all_repositories in zip(
            accounts_names, all_repositories
        )
        for _repositories, account in zip(_all_repositories, _accounts)
        for repository in _repositories
        if does_not_exist_in_gitroot_urls(
            repository=repository,
            urls=urls,
            nicknames=nicknames,
        )
    )

    return repositories


async def get_azure_credentials_authors_stats(
    *,
    credentials: list[Credentials],
    urls: set[str],
    nicknames: set[str],
    loaders: Dataloaders,
    organization_id: str,
) -> set[str]:
    with suppress(AzureDevOpsServiceError):
        return await _get_azure_credentials_authors_stats(
            credentials=credentials,
            loaders=loaders,
            urls=urls,
            nicknames=nicknames,
            organization_id=organization_id,
        )

    return set()


@retry_on_exceptions(
    exceptions=(AzureDevOpsServiceError,),
    sleep_seconds=float("2"),
    max_attempts=3,
)
async def _get_azure_credentials_authors_stats(
    *,
    credentials: list[Credentials],
    urls: set[str],
    nicknames: set[str],
    loaders: Dataloaders,
    organization_id: str,
) -> set[str]:
    repositories: tuple[OGitRepository, ...] = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    __get_azure_credentials_stats(
                        credential=credential,
                        loaders=loaders,
                        urls=urls,
                        nicknames=nicknames,
                        organization_id=organization_id,
                    )
                    for credential in credentials
                    if isinstance(credential.state.secret, OauthAzureSecret)
                )
            )
        )
    )

    repositories_authors: tuple[set[str], ...] = await collect(
        tuple(
            _get_oauth_missed_authors(repository=repository)
            for repository in repositories
        ),
        workers=32,
    )

    return set().union(*list(repositories_authors))


def _get_id(repository: CredentialsGitRepository | OGitRepository) -> str:
    return hashlib.sha256(
        str(parse_url(repository.repository.web_url).url)
        .lower()
        .encode("utf-8")
    ).hexdigest()


def __get_id(url: str) -> str:
    return hashlib.sha256(url.lower().encode("utf-8")).hexdigest()


def _get_branch(repository: CredentialsGitRepository | OGitRepository) -> str:
    return str(
        repository.repository.default_branch
        if repository.repository.default_branch is not None
        else "main"
    )


async def _get_missed_authors(
    *, loaders: Dataloaders, repository: CredentialsGitRepository
) -> set[str]:
    git_commits = (
        await loaders.organization_integration_repositories_commits.load(
            CredentialsGitRepositoryCommit(
                credential=repository.credential,
                project_name=repository.repository.project.name,
                repository_id=repository.repository.id,
                total=True,
            )
        )
    )

    if git_commits:
        return {commit.author.email.lower() for commit in git_commits}

    return set()


async def _get_commit_date(
    *, loaders: Dataloaders, repository: CredentialsGitRepository
) -> datetime:
    git_commits = (
        await loaders.organization_integration_repositories_commits.load(
            CredentialsGitRepositoryCommit(
                credential=repository.credential,
                project_name=repository.repository.project.name,
                repository_id=repository.repository.id,
            )
        )
    )

    if git_commits:
        return git_commits[0].committer.date

    return datetime.fromisoformat(DEFAULT_ISO_STR)


async def get_gitlab_credentials_stats(
    *,
    credentials: list[Credentials],
    urls: set[str],
    nicknames: set[str],
    loaders: Dataloaders,
    organization_id: str,
) -> RepositoriesStats:
    stats: tuple[ProjectStats, ...] = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    _get_gitlab_credential_stats(
                        credential=credential,
                        urls=urls,
                        nicknames=nicknames,
                        loaders=loaders,
                    )
                    for credential in credentials
                ),
                workers=1,
            )
        )
    )
    filtered_stats: tuple[ProjectStats, ...] = tuple(
        {stat.project.id: stat for stat in stats}.values()
    )

    return RepositoriesStats(
        repositories=tuple(
            OrganizationIntegrationRepository(
                id=__get_id(stat.project.remote_url),
                organization_id=organization_id,
                branch=stat.project.branch,
                last_commit_date=stat.project.last_activity_at,
                url=stat.project.remote_url,
                credential_id=stat.credential.id,
                branches=stat.project.branches,
                name=stat.project.name,
            )
            for stat in filtered_stats
        ),
    )


async def _get_oauth_missed_authors(*, repository: OGitRepository) -> set[str]:
    git_commits = await get_oauth_repositories_commits(
        repositories=[
            GitRepositoryCommit(
                account_name=repository.account.name,
                access_token=repository.token,
                project_name=repository.repository.project.name,
                repository_id=repository.repository.id,
                base_url=repository.account.base_url,
                total=True,
            )
        ]
    )

    if git_commits and git_commits[0]:
        return {
            commit.author.email.lower()
            for commit in git_commits[0]
            if commit.author is not None
        }

    return set()


async def _get_oauth_commit_date(*, repository: OGitRepository) -> datetime:
    git_commits = await get_oauth_repositories_commits(
        repositories=[
            GitRepositoryCommit(
                account_name=repository.account.name,
                access_token=repository.token,
                project_name=repository.repository.project.name,
                repository_id=repository.repository.id,
                base_url=repository.account.base_url,
            )
        ]
    )

    if git_commits and git_commits[0]:
        return git_commits[0][0].committer.date

    return datetime.fromisoformat(DEFAULT_ISO_STR)


async def get_azure_credentials_stats(
    *,
    credentials: list[Credentials],
    loaders: Dataloaders,
    urls: set[str],
    nicknames: set[str],
    organization_id: str,
) -> RepositoriesStats:
    with suppress(AzureDevOpsServiceError):
        return await _get_azure_credentials_stats(
            credentials=credentials,
            loaders=loaders,
            urls=urls,
            nicknames=nicknames,
            organization_id=organization_id,
        )

    return RepositoriesStats(
        repositories=tuple(),
    )


@retry_on_exceptions(
    exceptions=(AzureDevOpsServiceError,),
    sleep_seconds=float("5"),
    max_attempts=3,
)
async def _get_azure_credentials_stats(
    *,
    credentials: list[Credentials],
    loaders: Dataloaders,
    urls: set[str],
    nicknames: set[str],
    organization_id: str,
) -> RepositoriesStats:
    repositories: tuple[OGitRepository, ...] = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    __get_azure_credentials_stats(
                        credential=credential,
                        loaders=loaders,
                        urls=urls,
                        nicknames=nicknames,
                        organization_id=organization_id,
                    )
                    for credential in credentials
                    if isinstance(credential.state.secret, OauthAzureSecret)
                )
            )
        )
    )

    repositories_branches = await collect(
        tuple(
            in_thread(
                get_azure_branches_names,
                organization=repository.account.name,
                access_token=repository.token,
                project_name=repository.repository.project.name,
                repository_id=repository.repository.id,
                is_oauth=repository.is_oauth,
                base_url=repository.account.base_url,
            )
            for repository in repositories
        ),
        workers=64,
    )

    return RepositoriesStats(
        repositories=tuple(
            OrganizationIntegrationRepository(
                id=_get_id(repository),
                organization_id=organization_id,
                branch=_get_branch(repository),
                last_commit_date=(
                    repository.repository.project.last_update_time
                ),
                url=parse_url(repository.repository.web_url).url,
                credential_id=repository.credential.id,
                branches=branches
                or tuple(
                    # pylint: disable=bad-str-strip-call
                    [_get_branch(repository).lstrip("refs/heads/")]
                ),
                name=repository.repository.name,
            )
            for repository, branches in zip(
                repositories, repositories_branches
            )
        ),
    )


async def _get_gitlab_credential_stats(
    *,
    credential: Credentials,
    urls: set[str],
    nicknames: set[str],
    loaders: Dataloaders,
    get_all: bool = False,
) -> tuple[ProjectStats, ...]:
    if isinstance(credential.state.secret, OauthGitlabSecret):
        token: str | None = credential.state.secret.access_token
        if credential.state.secret.valid_until <= get_utc_now():
            token = await get_token(
                credential=credential,
                loaders=loaders,
            )
        if not token:
            return tuple()

        projects: tuple[BasicRepoData, ...] = await get_gitlab_projects(
            token=token,
            credential_id=credential.id,
        )
        filtered_projects = tuple(
            project
            for project in projects
            if does_not_exist_in_gitroot_urls(
                repository=project, urls=urls, nicknames=nicknames
            )
        )
        commits: tuple[tuple[dict, ...], ...]
        repositories_branches: tuple[tuple[str, ...], ...] = tuple([])
        if get_all:
            commits = await get_gitlab_commit(
                token=token,
                projects=tuple(project.id for project in filtered_projects),
            )
        else:
            commits = await get_gitlab_last_commit(
                token=token,
                projects=tuple(project.id for project in filtered_projects),
            )
            repositories_branches = await collect(
                tuple(
                    in_thread(
                        get_gitlab_branches_names,
                        token=token,
                        project_id=project.id,
                    )
                    for project in filtered_projects
                ),
                workers=32,
            )

        sorted_commits: tuple[tuple[dict, ...], ...] = tuple(
            tuple(
                sorted(
                    p_commits, key=lambda x: x["committed_date"], reverse=True
                )
            )
            for p_commits in commits
        )

        return tuple(
            ProjectStats(
                project=project._replace(
                    branches=repositories_branches[index] or project.branches
                    if repositories_branches
                    else project.branches
                ),
                commits=p_commits,
                credential=credential,
            )
            for index, (project, p_commits) in enumerate(
                zip(filtered_projects, sorted_commits)
            )
            if p_commits
        )

    return tuple()


async def get_github_credentials_stats(
    *,
    credentials: list[Credentials],
    urls: set[str],
    nicknames: set[str],
    organization_id: str,
) -> RepositoriesStats:
    stats: tuple[ProjectStats, ...] = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    _get_github_credential_stats(
                        credential=credential,
                        urls=urls,
                        nicknames=nicknames,
                    )
                    for credential in credentials
                ),
                workers=1,
            )
        )
    )
    filtered_stats: tuple[ProjectStats, ...] = tuple(
        {stat.project.id: stat for stat in stats}.values()
    )

    return RepositoriesStats(
        repositories=tuple(
            OrganizationIntegrationRepository(
                id=__get_id(stat.project.remote_url),
                organization_id=organization_id,
                branch=stat.project.branch,
                last_commit_date=stat.project.last_activity_at,
                url=stat.project.remote_url,
                credential_id=stat.credential.id,
                branches=stat.project.branches,
                name=stat.project.name,
            )
            for stat in filtered_stats
        ),
    )


async def get_bitbucket_credentials_stats(
    *,
    credentials: list[Credentials],
    urls: set[str],
    nicknames: set[str],
    loaders: Dataloaders,
    organization_id: str,
) -> RepositoriesStats:
    stats: tuple[ProjectStats, ...] = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    _get_bitbucket_credential_stats(
                        credential=credential,
                        urls=urls,
                        nicknames=nicknames,
                        loaders=loaders,
                    )
                    for credential in credentials
                ),
                workers=1,
            )
        )
    )

    filtered_stats: tuple[ProjectStats, ...] = tuple(
        {stat.project.id: stat for stat in stats}.values()
    )

    return RepositoriesStats(
        repositories=tuple(
            OrganizationIntegrationRepository(
                id=__get_id(stat.project.remote_url),
                organization_id=organization_id,
                branch=stat.project.branch,
                last_commit_date=datetime.fromtimestamp(
                    int(stat.commits[0]["date"])
                )
                if stat.commits
                else stat.project.last_activity_at,
                url=stat.project.remote_url,
                credential_id=stat.credential.id,
                branches=stat.project.branches,
                name=stat.project.name,
            )
            for stat in filtered_stats
        ),
    )


async def _get_bitbucket_credential_stats(
    *,
    credential: Credentials,
    loaders: Dataloaders,
    urls: set[str],
    nicknames: set[str],
    get_all: bool = False,
) -> tuple[ProjectStats, ...]:
    if isinstance(credential.state.secret, OauthBitbucketSecret):
        token: str | None = credential.state.secret.access_token
        if credential.state.secret.valid_until <= get_utc_now():
            token = await get_bitbucket_token(
                credential=credential,
                loaders=loaders,
            )
        if not token:
            return tuple()

        repositories: tuple[
            BasicRepoData, ...
        ] = await get_bitbucket_repositories(token=token)
        filtered_repositories = tuple(
            repository
            for repository in repositories
            if does_not_exist_in_gitroot_urls(
                repository=repository, urls=urls, nicknames=nicknames
            )
        )
        if get_all:
            commits = await get_bitbucket_authors(
                token=token,
                repos_ids=tuple(
                    repository.id for repository in filtered_repositories
                ),
            )
        else:
            branches = await collect(
                tuple(
                    get_bitbucket_branches_names(
                        token=token, repo_id=repository.id
                    )
                    for repository in filtered_repositories
                ),
                workers=1,
            )

        return tuple(
            ProjectStats(
                project=project._replace(
                    branches=branches[index] or tuple([project.branch])
                )
                if not get_all and branches
                else project,
                commits=commits[index] if get_all and commits else tuple(),
                credential=credential,
            )
            for index, project in enumerate(filtered_repositories)
        )

    return tuple()


async def _get_github_credential_stats(
    *,
    credential: Credentials,
    urls: set[str],
    nicknames: set[str],
    get_all: bool = False,
) -> tuple[ProjectStats, ...]:
    if isinstance(credential.state.secret, OauthGithubSecret):
        token: str = credential.state.secret.access_token

        repositories: tuple[BasicRepoData, ...] = await get_github_repos(
            token=token,
            credential_id=credential.id,
        )
        filtered_repositories = tuple(
            repository
            for repository in repositories
            if does_not_exist_in_gitroot_urls(
                repository=repository, urls=urls, nicknames=nicknames
            )
        )
        repositories_branches: tuple[tuple[str, ...], ...] = tuple()
        if get_all:
            commits = await get_github_repos_commits(
                token=token,
                repositories=tuple(
                    repository.id for repository in filtered_repositories
                ),
            )
        else:
            repositories_branches = await collect(
                tuple(
                    in_thread(
                        get_github_branches_names,
                        token=token,
                        repo_id=repo.id,
                    )
                    for repo in filtered_repositories
                ),
                workers=32,
            )

        return tuple(
            ProjectStats(
                project=project._replace(
                    branches=repositories_branches[index] or project.branches
                    if repositories_branches
                    else project.branches
                ),
                commits=tuple(
                    # pylint: disable-next=protected-access
                    commit._rawData["commit"]  # type: ignore[attr-defined]
                    for commit in commits[index]
                )
                if get_all
                else tuple(),
                credential=credential,
            )
            for index, project in enumerate(filtered_repositories)
        )

    return tuple()


async def get_pat_credentials_stats(
    credentials: list[Credentials],
    urls: set[str],
    nicknames: set[str],
    loaders: Dataloaders,
    organization_id: str,
) -> RepositoriesStats:
    pat_credentials = filter_pat_credentials(credentials)
    all_repositories = (
        await loaders.organization_integration_repositories.load_many(
            pat_credentials
        )
    )

    repositories: tuple[CredentialsGitRepository, ...] = tuple(
        CredentialsGitRepository(
            credential=credential,
            repository=repository,
        )
        for credential, _repositories in zip(pat_credentials, all_repositories)
        for repository in _repositories
        if does_not_exist_in_gitroot_urls(
            repository=repository,
            urls=urls,
            nicknames=nicknames,
        )
    )

    repositories_dates: tuple[datetime, ...] = await collect(
        tuple(
            _get_commit_date(loaders=loaders, repository=repository)
            for repository in repositories
        ),
        workers=16,
    )

    return RepositoriesStats(
        repositories=tuple(
            OrganizationIntegrationRepository(
                id=_get_id(repository),
                organization_id=organization_id,
                branch=_get_branch(repository),
                last_commit_date=date,
                url=parse_url(repository.repository.web_url).url,
                credential_id=repository.credential.id,
            )
            for repository, date in zip(repositories, repositories_dates)
        ),
    )
