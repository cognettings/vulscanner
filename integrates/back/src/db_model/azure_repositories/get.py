# pylint: disable=protected-access
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
    in_thread,
)
from atlassian.bitbucket import (
    Cloud,
)
from atlassian.bitbucket.cloud.base import (
    BitbucketCloudBase,
)
from azure.devops.client import (
    AzureDevOpsAuthenticationError,
)
from azure.devops.connection import (
    Connection,
)
from azure.devops.exceptions import (
    AzureDevOpsClientRequestError,
    AzureDevOpsServiceError,
)
from azure.devops.v6_0.accounts.accounts_client import (
    AccountsClient,
)
from azure.devops.v6_0.accounts.models import (
    Account,
)
from azure.devops.v6_0.git.git_client import (
    GitClient,
)
from azure.devops.v6_0.git.models import (
    GitBranchStats,
    GitCommit,
    GitQueryCommitsCriteria,
    GitRepository,
)
from azure.devops.v6_0.profile.models import (
    Profile,
)
from azure.devops.v6_0.profile.profile_client import (
    ProfileClient,
)
from collections.abc import (
    Iterable,
)
from context import (
    FI_AZURE_OAUTH2_REPOSITORY_APP_ID,
    FI_BITBUCKET_OAUTH2_REPOSITORY_APP_ID,
)
from datetime import (
    datetime,
    timezone,
)
from dateutil import (
    parser,
)
from db_model.azure_repositories.types import (
    AccountInfo,
    BasicRepoData,
    CredentialsGitRepositoryCommit,
    GitRepositoryCommit,
)
from db_model.credentials.types import (
    Credentials,
    HttpsPatSecret,
)
from git.exc import (
    GitError,
)
from git.repo.base import (
    Repo,
)
from git_self import (
    https_clone,
)
from github import (
    Commit,
    Github,
)
from github.GithubException import (
    BadCredentialsException,
    GithubException,
    RateLimitExceededException,
)
import gitlab
from gitlab.const import (
    AccessLevel,
)
from gitlab.exceptions import (
    GitlabAuthenticationError,
    GitlabListError,
)
import json
import logging
import logging.config
from msrest.authentication import (
    BasicAuthentication,
    OAuthTokenAuthentication,
)
from msrest.exceptions import (
    ClientRequestError,
    DeserializationError,
)
import requests
from settings import (
    LOGGING,
)
import shutil
from tempfile import (
    TemporaryDirectory,
)
from urllib3.util.url import (
    parse_url,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
BASE_URL = "https://dev.azure.com"
PROFILE_BASE_URL = "https://app.vssps.visualstudio.com"


async def get_repositories(
    *,
    credentials: Iterable[Credentials],
) -> list[list[GitRepository]]:
    return list(
        await collect(
            tuple(
                in_thread(
                    _get_repositories,
                    base_url=f"{BASE_URL}/"
                    f"{credential.state.azure_organization}",
                    access_token=credential.state.secret.token
                    if isinstance(credential.state.secret, HttpsPatSecret)
                    else "",
                )
                for credential in credentials
            ),
            workers=1,
        )
    )


def _get_repositories(
    *,
    base_url: str,
    access_token: str,
    is_oauth: bool = False,
) -> list[GitRepository]:
    credentials: BasicAuthentication | OAuthTokenAuthentication
    if is_oauth:
        credentials = OAuthTokenAuthentication(
            FI_AZURE_OAUTH2_REPOSITORY_APP_ID, {"access_token": access_token}
        )
    else:
        credentials = BasicAuthentication("", access_token)
    connection = Connection(base_url=base_url, creds=credentials)
    try:
        git_client: GitClient = connection.clients.get_git_client()
        repositories: list[GitRepository] = git_client.get_repositories()
    except (
        AzureDevOpsClientRequestError,
        AzureDevOpsAuthenticationError,
        AzureDevOpsServiceError,
        requests.exceptions.ChunkedEncodingError,
    ) as exc:
        if (
            is_oauth
            and str(exc).startswith("TF400813")
            and not str(exc).startswith(
                "TF400813: The user is not authorized to access this resource."
            )
        ):
            raise exc

        LOGGER.error(
            "Error getting azure repo data",
            extra=dict(
                extra=dict(
                    exception=exc,
                    base_url=base_url,
                    is_oauth=is_oauth,
                )
            ),
        )
        return []
    else:
        return [
            repo
            for repo in repositories
            if not repo.additional_properties["isDisabled"]
        ]


async def get_oauth_repositories(
    *,
    token: str,
    base_urls: tuple[str, ...],
) -> list[list[GitRepository]]:
    return list(
        await collect(
            tuple(
                in_thread(
                    _get_repositories,
                    base_url=base_url,
                    access_token=token,
                    is_oauth=True,
                )
                for base_url in base_urls
            ),
            workers=1,
        )
    )


async def get_bitbucket_authors(
    *, token: str, repos_ids: tuple[str, ...]
) -> tuple[tuple[dict, ...], ...]:
    return await collect(
        tuple(
            _get_bitbucket_authors(token=token, repo_id=repo_id)
            for repo_id in repos_ids
        ),
        workers=1,
    )


async def _get_authors(
    *,
    branch: str,
    url: str,
    token: str,
    oauth_type: str,
) -> tuple[dict, ...]:
    with TemporaryDirectory(
        prefix="integrates_clone_", ignore_cleanup_errors=True
    ) as temp_dir:
        folder_to_clone_root, stderr = await https_clone(
            branch=branch,
            password=None,
            repo_url=url,
            temp_dir=temp_dir,
            token=token,
            user=None,
            is_oauth=True,
            provider=oauth_type,
        )

        if folder_to_clone_root is None:
            shutil.rmtree(temp_dir, ignore_errors=True)
            LOGGER.info(
                "Failed to clone",
                extra=dict(
                    extra={
                        "url": url,
                        "error": stderr,
                    }
                ),
            )
            return tuple()

        try:
            repo = Repo(folder_to_clone_root, search_parent_directories=True)
            authors = tuple(
                {
                    "author": commit.author.email.lower(),
                    "date": commit.committed_date,
                }
                for commit in repo.iter_commits()
                if commit.author.email
            )

            shutil.rmtree(temp_dir, ignore_errors=True)
            return authors
        except (GitError, AttributeError) as exc:
            shutil.rmtree(temp_dir, ignore_errors=True)
            LOGGER.error(
                exc,
                extra=dict(
                    extra={
                        "url": url,
                    }
                ),
            )
            return tuple()


def get_gitlab_branches_names(
    token: str,
    project_id: str,
) -> tuple[str, ...]:
    try:
        with gitlab.Gitlab(oauth_token=token) as g_session:
            project = g_session.projects.get(project_id)
            branches = project.branches.list(get_all=True)

            return tuple(branch.name for branch in branches)
    except (GitlabAuthenticationError, KeyError, GitlabListError) as exc:
        LOGGER.error(
            "Error getting gitlab branches",
            extra=dict(extra=dict(exception=exc, project_id=project_id)),
        )
    return tuple()


def get_azure_branches_names(
    *,
    organization: str,
    access_token: str,
    repository_id: str,
    project_name: str,
    is_oauth: bool = False,
    base_url: str | None = None,
) -> tuple[str, ...]:
    credentials: BasicAuthentication | OAuthTokenAuthentication
    if is_oauth:
        credentials = OAuthTokenAuthentication(
            FI_AZURE_OAUTH2_REPOSITORY_APP_ID, {"access_token": access_token}
        )
    else:
        credentials = BasicAuthentication("", access_token)
    connection = Connection(
        base_url=base_url or f"{BASE_URL}/{organization}", creds=credentials
    )
    try:
        git_client: GitClient = connection.clients_v6_0.get_git_client()
        branches: list[GitBranchStats] = git_client.get_branches(
            repository_id=repository_id,
            project=project_name,
        )
        branches_names: list[str] = list(branch.name for branch in branches)
    except (
        AzureDevOpsAuthenticationError,
        AzureDevOpsClientRequestError,
        AzureDevOpsServiceError,
        DeserializationError,
    ) as exc:
        if is_oauth and str(exc).startswith("TF400813"):
            raise exc

        if any(
            str(exc).startswith(error) for error in ["TF401019", "VS403403"]
        ):
            return tuple()

        LOGGER.error(
            "Error getting azure repo branches data",
            extra=dict(
                extra=dict(
                    exception=exc,
                    repository_id=repository_id,
                    project_name=project_name,
                    is_oauth=is_oauth,
                )
            ),
        )
        return tuple()
    else:
        return tuple(branches_names)


async def get_bitbucket_branches_names(
    *, token: str, repo_id: str
) -> tuple[str, ...]:
    oauth2_dict = {
        "client_id": FI_BITBUCKET_OAUTH2_REPOSITORY_APP_ID,
        "token": {"access_token": token},
    }
    workspace, slug = repo_id.rsplit("#REPOSITORY#", 1)

    return await in_thread(
        _get_bitbucket_branches_names, workspace, slug, oauth2_dict
    )


def _get_bitbucket_branches_names(
    workspace_uuid: str, repo_slug: str, oauth2: dict
) -> tuple[str, ...]:
    branches = []
    try:
        base_cloud = BitbucketCloudBase(
            oauth2=oauth2,
            cloud=True,
            api_root=None,
            api_version="2.0",
            url=(
                "https://api.bitbucket.org/2.0/repositories"
                f"/{workspace_uuid}/{repo_slug}/refs/branches"
            ),
        )
        for branch in base_cloud._get_paged(
            None, trailing=True, params={"sort": "-target.date"}
        ):
            branches.append(branch["name"])
    except (
        requests.exceptions.HTTPError,
        json.decoder.JSONDecodeError,
    ) as exc:
        LOGGER.error(
            "Error getting bitbucket repo branches data",
            extra=dict(extra=dict(exception=exc, repo_id=repo_slug)),
        )

    return tuple(branches)[:50]


async def _get_bitbucket_authors(
    *, token: str, repo_id: str
) -> tuple[dict, ...]:
    oauth2_dict = {
        "client_id": FI_BITBUCKET_OAUTH2_REPOSITORY_APP_ID,
        "token": {"access_token": token},
    }
    bitbucket_cloud = Cloud(oauth2=oauth2_dict)
    _workspace, _slug = repo_id.rsplit("#REPOSITORY#", 1)
    try:
        repo = bitbucket_cloud.repositories.get(_workspace, _slug)
    except requests.exceptions.HTTPError as exc:
        LOGGER.error(
            "Error getting bitbucket repo authors data",
            extra=dict(extra=dict(exception=exc, repo_id=repo_id)),
        )

        return tuple()

    return await _get_authors(
        branch=repo._BitbucketBase__data["mainbranch"]["name"],
        url=repo._BitbucketBase__data["links"]["clone"][0]["href"],
        token=token,
        oauth_type="BITBUCKET",
    )


async def get_bitbucket_repositories(
    *, token: str
) -> tuple[BasicRepoData, ...]:
    try:
        return await in_thread(_get_bitbucket_repositories, token=token)
    except requests.exceptions.HTTPError as exc:
        LOGGER.exception(
            exc,
            extra=dict(extra="Error when requesting bitbucket repositories"),
        )
        return tuple()


def _get_bitbucket_repositories(*, token: str) -> tuple[BasicRepoData, ...]:
    repos: list[BasicRepoData] = []
    oauth2_dict = {
        "client_id": FI_BITBUCKET_OAUTH2_REPOSITORY_APP_ID,
        "token": {"access_token": token},
    }
    bitbucket_cloud = Cloud(oauth2=oauth2_dict)
    for workspace in bitbucket_cloud.workspaces.each():
        for repo in workspace.repositories.each():
            main_branch = repo._BitbucketBase__data["mainbranch"]["name"]
            default_branch = (
                f'refs/heads/{main_branch.rstrip().lstrip("refs/heads/")}'
            )

            repos.append(
                BasicRepoData(
                    id=(f"{workspace.uuid}#REPOSITORY#{repo.slug}"),
                    remote_url=parse_url(
                        repo._BitbucketBase__data["links"]["clone"][0]["href"],
                    )
                    ._replace(auth=None)
                    .url,
                    ssh_url=repo._BitbucketBase__data["links"]["clone"][1][
                        "href"
                    ],
                    web_url=parse_url(
                        repo._BitbucketBase__data["links"]["html"]["href"]
                    ).url,
                    branch=default_branch,
                    branches=tuple(),
                    name=repo.name,
                    last_activity_at=datetime.fromisoformat(
                        "2000-01-01T05:00:00+00:00"
                    )
                    if repo.updated_on == "never updated"
                    else parser.parse(
                        repo.updated_on,
                    ).astimezone(timezone.utc),
                )
            )

    return tuple(repos)


async def get_account_names(
    *,
    tokens: tuple[str, ...],
    credentials: list[Credentials],
) -> tuple[tuple[AccountInfo, ...], ...]:
    profiles: tuple[Profile, ...] = await collect(
        tuple(
            in_thread(
                _get_profile, base_url=PROFILE_BASE_URL, access_token=token
            )
            for token in tokens
        ),
        workers=1,
    )

    for profile, credential in zip(profiles, credentials):
        if profile is None:
            LOGGER.info(
                "Empty profile response",
                extra=dict(extra=dict(credential_id=credential.id)),
            )

    accounts = await collect(
        tuple(
            in_thread(
                _get_account,
                base_url=PROFILE_BASE_URL,
                access_token=token,
                public_alias=profile.additional_properties["publicAlias"],
            )
            for profile, token in zip(profiles, tokens)
            if profile is not None
        ),
        workers=1,
    )

    return tuple(
        tuple(
            AccountInfo(
                name=account.account_name, base_url=account.account_uri
            )
            for account in _accounts
        )
        for _accounts in accounts
    )


def _get_account(
    *, base_url: str, access_token: str, public_alias: str
) -> tuple[Account, ...]:
    credentials = OAuthTokenAuthentication(
        FI_AZURE_OAUTH2_REPOSITORY_APP_ID, {"access_token": access_token}
    )
    connection = Connection(base_url=base_url, creds=credentials)
    try:
        account_client: AccountsClient = (
            connection.clients_v6_0.get_accounts_client()
        )
        account: list[Account] = account_client.get_accounts(
            None, public_alias
        )
    except (
        AzureDevOpsClientRequestError,
        AzureDevOpsAuthenticationError,
        AzureDevOpsServiceError,
    ) as exc:
        LOGGER.error(
            "Error getting azure account data",
            extra=dict(
                extra=dict(
                    exception=exc,
                    base_url=base_url,
                    public_alias=public_alias,
                )
            ),
        )
        if str(exc.message).startswith("TF400813"):
            raise exc
        return tuple()
    else:
        return tuple(account)


def _get_profile(*, base_url: str, access_token: str) -> Profile:
    credentials = OAuthTokenAuthentication(
        FI_AZURE_OAUTH2_REPOSITORY_APP_ID, {"access_token": access_token}
    )
    connection = Connection(base_url=base_url, creds=credentials)
    try:
        profile_client: ProfileClient = (
            connection.clients_v6_0.get_profile_client()
        )
        profile: Profile = profile_client.get_profile("me")
    except (
        AzureDevOpsClientRequestError,
        AzureDevOpsAuthenticationError,
        AzureDevOpsServiceError,
        ClientRequestError,
    ) as exc:
        LOGGER.error(
            "Error getting azure profile data",
            extra=dict(
                extra=dict(
                    exception=exc,
                    base_url=base_url,
                )
            ),
        )
        if str(exc).startswith("TF400813"):
            raise exc
        return None
    else:
        return profile


async def get_oauth_repositories_commits(
    *,
    repositories: list[GitRepositoryCommit],
) -> list[list[GitCommit]]:
    repositories_commits = await collect(
        tuple(
            in_thread(
                _get_repositories_commits,
                organization=repository.account_name,
                access_token=repository.access_token,
                repository_id=repository.repository_id,
                project_name=repository.project_name,
                base_url=repository.base_url,
                is_oauth=True,
            )
            for repository in repositories
        ),
        workers=1,
    )

    return list(repositories_commits)


async def get_repositories_commits(
    *,
    repositories: Iterable[CredentialsGitRepositoryCommit],
) -> list[list[GitCommit]]:
    repositories_commits = await collect(
        tuple(
            in_thread(
                _get_repositories_commits,
                organization=repository.credential.state.azure_organization,
                access_token=repository.credential.state.secret.token
                if isinstance(
                    repository.credential.state.secret, HttpsPatSecret
                )
                else "",
                repository_id=repository.repository_id,
                project_name=repository.project_name,
            )
            for repository in repositories
        ),
        workers=1,
    )

    return list(repositories_commits)


def _get_repositories_commits(
    *,
    organization: str,
    access_token: str,
    repository_id: str,
    project_name: str,
    total: bool = False,
    is_oauth: bool = False,
    base_url: str | None = None,
) -> list[GitCommit]:
    credentials: BasicAuthentication | OAuthTokenAuthentication
    if is_oauth:
        credentials = OAuthTokenAuthentication(
            FI_AZURE_OAUTH2_REPOSITORY_APP_ID, {"access_token": access_token}
        )
    else:
        credentials = BasicAuthentication("", access_token)
    connection = Connection(
        base_url=base_url or f"{BASE_URL}/{organization}", creds=credentials
    )
    try:
        git_client: GitClient = connection.clients_v6_0.get_git_client()
        commits: list[GitCommit] = git_client.get_commits(
            search_criteria=GitQueryCommitsCriteria()
            if total
            else GitQueryCommitsCriteria(top=1),
            repository_id=repository_id,
            project=project_name,
        )
    except (
        AzureDevOpsAuthenticationError,
        AzureDevOpsClientRequestError,
        AzureDevOpsServiceError,
    ) as exc:
        if is_oauth and str(exc.message).startswith("TF400813"):
            raise exc

        LOGGER.error(
            "Error getting azure commit data",
            extra=dict(
                extra=dict(
                    exception=exc,
                    repository_id=repository_id,
                    project_name=project_name,
                    is_oauth=is_oauth,
                    organization=organization,
                )
            ),
        )
        return []
    else:
        return commits


async def get_gitlab_commit(
    *,
    token: str,
    projects: tuple[str, ...],
) -> tuple[tuple[dict, ...], ...]:
    return await collect(
        tuple(
            in_thread(_get_gitlab_commit, token=token, project_id=project_id)
            for project_id in projects
        ),
        workers=1,
    )


def _get_gitlab_commit(token: str, project_id: str) -> tuple[dict, ...]:
    try:
        with gitlab.Gitlab(oauth_token=token) as g_session:
            project = g_session.projects.get(project_id)
            commits = project.commits.list(get_all=True, order_by="default")

            return tuple(commit.attributes for commit in commits)
    except (GitlabAuthenticationError, GitlabListError) as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))

    return tuple()


async def get_gitlab_last_commit(
    *,
    token: str,
    projects: tuple[str, ...],
) -> tuple[tuple[dict, ...], ...]:
    return await collect(
        tuple(
            in_thread(
                _get_gitlab_last_commit, token=token, project_id=project_id
            )
            for project_id in projects
        ),
        workers=1,
    )


def _get_gitlab_last_commit(token: str, project_id: str) -> tuple[dict, ...]:
    try:
        with gitlab.Gitlab(oauth_token=token) as g_session:
            project = g_session.projects.get(project_id)
            commits = project.commits.list(
                per_page=1, page=1, order_by="default"
            )

            return tuple(commit.attributes for commit in commits)
    except (
        GitlabAuthenticationError,
        GitlabListError,
        requests.exceptions.ChunkedEncodingError,
    ) as exc:
        LOGGER.error(
            "Error getting gitlab commit data",
            extra=dict(extra=dict(exception=exc, project_id=project_id)),
        )
    return tuple()


async def get_github_repos_commits(
    *, token: str, repositories: tuple[str, ...]
) -> tuple[tuple[Commit.Commit, ...], ...]:
    try:
        return await collect(
            tuple(
                in_thread(
                    _get_github_repos_commits, token=token, repo_id=repo_id
                )
                for repo_id in repositories
            ),
            workers=1,
        )
    except BadCredentialsException as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
    return tuple()


def _get_github_repos_commits(
    token: str, repo_id: str
) -> tuple[Commit.Commit, ...]:
    commits = []
    try:
        for commit in Github(token).get_repo(int(repo_id)).get_commits():
            commits.append(commit)
    except (GithubException, RateLimitExceededException) as exc:
        if "Git Repository is empty" in str(exc):
            return tuple()

        LOGGER.exception(exc, extra=dict(extra=locals()))

    return tuple(commits)


async def get_github_repos(
    *, token: str, credential_id: str
) -> tuple[BasicRepoData, ...]:
    try:
        return await in_thread(_get_github_repos, token=token)
    except (
        BadCredentialsException,
        GithubException,
        RateLimitExceededException,
    ) as exc:
        LOGGER.error(
            "Error getting github repos data",
            extra=dict(extra=dict(exception=exc, credential_id=credential_id)),
        )
    return tuple()


def get_github_branches_names(
    token: str,
    repo_id: str,
) -> tuple[str, ...]:
    try:
        repo = Github(token).get_repo(int(repo_id))
        return tuple(branch.name for branch in repo.get_branches())
    except (
        BadCredentialsException,
        GithubException,
        RateLimitExceededException,
    ) as exc:
        LOGGER.error(
            "Error getting github branches data",
            extra=dict(extra=dict(exception=exc, repo_id=repo_id)),
        )
    return tuple()


def _get_github_repos(token: str) -> tuple[BasicRepoData, ...]:
    repos = Github(token).get_user().get_repos()

    return tuple(
        BasicRepoData(
            id=str(repo.id),
            remote_url=parse_url(repo.clone_url).url,
            ssh_url=repo.git_url,
            web_url=parse_url(repo.html_url).url,
            branch=(
                "refs/heads/"
                f'{repo.default_branch.rstrip().lstrip("refs/heads/")}'
            ),
            branches=tuple(
                [f'{repo.default_branch.rstrip().lstrip("refs/heads/")}']
            ),
            name=repo.name,
            last_activity_at=repo.updated_at.astimezone(timezone.utc),
        )
        for repo in repos
    )


async def get_gitlab_projects(
    *, token: str, credential_id: str
) -> tuple[BasicRepoData, ...]:
    try:
        return await in_thread(_get_gitlab_projects, token=token)
    except (GitlabAuthenticationError, KeyError, GitlabListError) as exc:
        LOGGER.error(
            exc,
            extra=dict(extra=dict(credential_id=credential_id)),
        )
    return tuple()


def _get_gitlab_projects(token: str) -> tuple[BasicRepoData, ...]:
    with gitlab.Gitlab(oauth_token=token) as g_session:
        projects = tuple(
            g_session.projects.list(
                all=True,
                min_access_level=AccessLevel.REPORTER.value,
            )
        )

        return tuple(
            BasicRepoData(
                id=gproject.id,
                remote_url=parse_url(
                    gproject.attributes["http_url_to_repo"]
                ).url,
                ssh_url=gproject.attributes["ssh_url_to_repo"],
                web_url=parse_url(gproject.attributes["web_url"]).url,
                branch=(
                    "refs/heads/"
                    + gproject.attributes["default_branch"]
                    .rstrip()
                    .lstrip("refs/heads/")
                ),
                branches=tuple(
                    [
                        gproject.attributes["default_branch"]
                        .rstrip()
                        .lstrip("refs/heads/")
                    ]
                ),
                name=gproject.name,
                last_activity_at=parser.parse(
                    gproject.attributes["last_activity_at"]
                ).astimezone(timezone.utc),
            )
            for gproject in projects
            if not bool(gproject.attributes["archived"])
        )


class OrganizationRepositoriesLoader(
    DataLoader[Credentials, list[GitRepository]]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        credentials: Iterable[Credentials],
    ) -> list[list[GitRepository]]:
        return await get_repositories(credentials=credentials)


class OrganizationRepositoriesCommitsLoader(
    DataLoader[CredentialsGitRepositoryCommit, list[GitCommit]]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        repositories: Iterable[CredentialsGitRepositoryCommit],
    ) -> list[list[GitCommit]]:
        return await get_repositories_commits(repositories=repositories)
