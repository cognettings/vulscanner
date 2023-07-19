from azure.devops.v6_0.git.models import (
    GitRepository,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    Credentials,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
    OrganizationIntegrationRepositoryConnection,
)
from typing import (
    NamedTuple,
)


class CredentialsGitRepository(NamedTuple):
    credential: Credentials
    repository: GitRepository


class CredentialsGitRepositoryCommit(NamedTuple):
    credential: Credentials
    project_name: str
    repository_id: str
    total: bool = False


class AccountInfo(NamedTuple):
    base_url: str
    name: str


class OGitRepository(NamedTuple):
    account: AccountInfo
    token: str
    repository: GitRepository
    credential: Credentials
    is_oauth: bool = False


class GitRepositoryCommit(NamedTuple):
    account_name: str
    access_token: str
    project_name: str
    repository_id: str
    base_url: str | None = None
    total: bool = False


class CredentialsGitRepositoryResolver(NamedTuple):
    credential: Credentials | None = None
    repository: GitRepository | None = None
    connection: OrganizationIntegrationRepositoryConnection | None = None


class BranchesData(NamedTuple):
    name: str


class BasicRepoData(NamedTuple):
    id: str
    remote_url: str
    ssh_url: str
    web_url: str
    branch: str
    branches: tuple[str, ...]
    last_activity_at: datetime
    name: str


class ProjectStats(NamedTuple):
    project: BasicRepoData
    commits: tuple[dict, ...]
    credential: Credentials


class RepositoriesStats(NamedTuple):
    repositories: tuple[OrganizationIntegrationRepository, ...]
