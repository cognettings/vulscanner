# pylint: disable=too-many-lines,too-many-statements, import-error
from . import (
    get_organization_events,
    get_result,
    get_vulnerabilities_url,
)
from azure.devops.v6_0.git.models import (
    GitCommit,
    GitRepository,
    GitUserDate,
    TeamProjectReference,
)
from back.test.functional.src.remove_credentials import (
    get_result as remove_credentials,
)
from back.test.functional.src.remove_stakeholder_access import (
    get_access_token,
)
from custom_exceptions import (
    RequiredVerificationCode,
)
from custom_utils.datetime import (
    get_as_utc_iso_format,
    get_now_minus_delta,
    get_now_plus_delta,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model.azure_repositories.types import (
    AccountInfo,
    BasicRepoData,
    CredentialsGitRepository,
    OGitRepository,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsState,
    OauthAzureSecret,
    OauthGitlabSecret,
)
from db_model.credentials.update import (
    update_credential_state,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
from db_model.roots.types import (
    GitRoot,
)
from github import (
    GitCommit as GitHubCommit,
)
from github.GithubException import (
    BadCredentialsException,
)
from gitlab.exceptions import (
    GitlabAuthenticationError,
)
import glob
import os
import pytest
import pytz
from schedulers.update_organization_overview import (
    main as update_organization_overview,
)
from schedulers.update_organization_repositories import (
    main as update_organization_repositories,
)
import shutil
from typing import (
    Any,
)
from unittest import (
    mock,
)


def get_account_names(
    *,
    tokens: tuple[str, ...],  # pylint: disable=unused-argument
    credentials: list[Credentials],  # pylint: disable=unused-argument
) -> tuple[tuple[AccountInfo, ...], ...]:
    return tuple(
        [tuple([AccountInfo(name="testorg1", base_url="https://test.test")])]
    )


def _get_bitbucket_repositories(
    *,
    token: str,  # pylint: disable=unused-argument
) -> tuple[BasicRepoData, ...]:
    return tuple(
        [
            BasicRepoData(
                id="678912345",
                ssh_url="ssh://git@test.com/testprojects/sixthtrepo",
                remote_url="https://git@test.com/testprojects/sixthtrepo.git",
                web_url="https://test.com/testprojects/sixthtrepo",
                branch="refs/heads/main",
                branches=tuple(),
                name="sixthtrepo",
                last_activity_at=get_now_minus_delta(days=10),
            )
        ]
    )


def get_repositories(
    *,
    base_url: str,  # pylint: disable=unused-argument
    access_token: str,  # pylint: disable=unused-argument
    is_oauth: bool = False,  # pylint: disable=unused-argument
) -> tuple[GitRepository, ...]:
    return tuple(
        [
            GitRepository(
                project=TeamProjectReference(
                    last_update_time=get_now_minus_delta(days=2),
                    name="testprojects",
                ),
                default_branch="refs/head/main",
                id="2",
                remote_url=(
                    "https://test.com/testprojects/_git/secondrepor.git"
                ),
                ssh_url="ssh://git@test.com:v3/testprojects/_git/secondrepor",
                url="https://test.com/testprojects/_git/secondrepor",
                web_url="https://test.com/testprojects/_git/secondrepor",
            ),
            GitRepository(
                project=TeamProjectReference(
                    last_update_time=get_now_minus_delta(days=2),
                    name="testprojects",
                ),
                default_branch="refs/head/trunk",
                id="1",
                ssh_url="ssh://git@test.com:v3/testprojects/_git/firstrepo",
                remote_url=(
                    "https://git@test.com/testprojects/_git/firstrepo.git"
                ),
                url="https://test.com/testprojects/_git/firstrepo",
                web_url="https://test.com/testprojects/_git/firstrepo",
            ),
        ]
    )


def get_credentials_repositories(
    credential: Credentials,  # pylint: disable=unused-argument
    loaders: Dataloaders,  # pylint: disable=unused-argument
) -> tuple[OrganizationIntegrationRepository, ...]:
    return tuple(
        [
            OrganizationIntegrationRepository(
                id=(
                    "4334ca3f5c8afb8b529782a6b96daa94160e5f3c030ebbc5f"
                    "369d800b2a8b584"
                ),
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                branch="main",
                branches=tuple(["main"]),
                last_commit_date=datetime.fromisoformat(
                    "2022-11-02T09:37:57+00:00"
                ),
                url="ssh://git@test.com:v3/testprojects/_git/secondrepor",
                credential_id="1a5dacda-1d52-465c-9158-f6fd5dfe0998",
            ),
        ]
    )


def get_repositories_commits(
    *,
    organization: str,  # pylint: disable=unused-argument
    access_token: str,  # pylint: disable=unused-argument
    repository_id: str,  # pylint: disable=unused-argument
    project_name: str,  # pylint: disable=unused-argument
    total: bool = False,  # pylint: disable=unused-argument
    is_oauth: bool = False,  # pylint: disable=unused-argument
    base_url: str | None = None,  # pylint: disable=unused-argument
) -> tuple[GitCommit, ...]:
    return tuple(
        [
            GitCommit(committer=GitUserDate(date=get_now_minus_delta(days=1))),
            GitCommit(committer=GitUserDate(date=get_now_minus_delta(days=2))),
        ]
    )


def get_azure_branches_names(
    *,
    organization: str,  # pylint: disable=unused-argument
    access_token: str,  # pylint: disable=unused-argument
    repository_id: str,  # pylint: disable=unused-argument
    project_name: str,  # pylint: disable=unused-argument
    is_oauth: bool = False,  # pylint: disable=unused-argument
    base_url: str | None = None,  # pylint: disable=unused-argument
) -> tuple[str, ...]:
    return tuple(["main"])


def get_lab_repositories_stats(
    token: str,  # pylint: disable=unused-argument
) -> tuple[BasicRepoData, ...]:
    return tuple(
        [
            BasicRepoData(
                id="123456789",
                ssh_url="ssh://git@test.com/testprojects/fourthtrepo",
                remote_url="https://git@test.com/testprojects/fourthtrepo.git",
                web_url="https://test.com/testprojects/fourthtrepo",
                branch="refs/heads/main",
                branches=tuple(["main"]),
                name="fourthtrepo",
                last_activity_at=get_now_minus_delta(days=4),
            )
        ]
    )


def get_hub_repositories_stats(
    token: str,  # pylint: disable=unused-argument
) -> tuple[BasicRepoData, ...]:
    return tuple(
        [
            BasicRepoData(
                id="234567890",
                ssh_url="ssh://git@test.com/testprojects/fifthtrepo",
                remote_url="https://git@test.com/testprojects/fifthtrepo.git",
                web_url="https://test.com/testprojects/fifthtrepo",
                branch="refs/heads/dev",
                branches=tuple(["dev"]),
                name="fifthtrepo",
                last_activity_at=get_now_minus_delta(days=6),
            )
        ]
    )


def get_lab_commit_stats(
    token: str,  # pylint: disable=unused-argument
    project_id: str,  # pylint: disable=unused-argument
) -> tuple[dict, ...]:
    return tuple(
        [
            dict(
                committed_date=get_as_utc_iso_format(
                    get_now_minus_delta(days=5)
                ),
                author_email="testemail1@test.test",
            ),
            dict(
                committed_date=get_as_utc_iso_format(
                    get_now_minus_delta(days=4)
                ),
                author_email="testemail2@test.test",
            ),
        ]
    )


def get_lab_last_commit_stats(
    token: str,  # pylint: disable=unused-argument
    project_id: str,  # pylint: disable=unused-argument
) -> tuple[dict, ...]:
    return tuple(
        [
            dict(
                committed_date=get_as_utc_iso_format(
                    get_now_minus_delta(days=4)
                ),
                author_email="testemail2@test.test",
            ),
        ]
    )


def get_hub_commit_stats(
    token: str,  # pylint: disable=unused-argument
    repo_id: str,  # pylint: disable=unused-argument
) -> tuple[GitHubCommit.GitCommit, ...]:
    return tuple()


def _get_lab_last_commit_stats(
    token: str, project_id: str
) -> tuple[dict, ...]:
    raise GitlabAuthenticationError("")


def _get_lab_repositories_stats(token: str) -> tuple[BasicRepoData, ...]:
    raise GitlabAuthenticationError("")


def _get_hub_repositories_stats(token: str) -> tuple[BasicRepoData, ...]:
    raise BadCredentialsException(401, "", None)


def _get_lab_commit_stats(token: str, project_id: str) -> tuple[dict, ...]:
    raise GitlabAuthenticationError("")


async def get_azure_token(
    *,
    credential: Credentials,
    loaders: Dataloaders,
) -> str | None:
    if not isinstance(credential.state.secret, OauthAzureSecret):
        return None
    new_state = CredentialsState(
        modified_by=credential.state.modified_by,
        modified_date=datetime.now(tz=pytz.timezone("UTC")),
        name=credential.state.name,
        secret=OauthAzureSecret(
            redirect_uri=credential.state.secret.redirect_uri,
            arefresh_token="CFCzdCBTU0gK",
            access_token="DEDzdCBTU0gK",
            valid_until=get_now_plus_delta(hours=2),
        ),
        is_pat=credential.state.is_pat,
        azure_organization=credential.state.azure_organization,
        type=credential.state.type,
    )
    await update_credential_state(
        current_value=credential.state,
        credential_id=credential.id,
        organization_id=credential.organization_id,
        state=new_state,
        force_update_owner=False,
    )
    loaders.credentials.clear_all()
    loaders.organization_credentials.clear(credential.organization_id)
    return "DEDzdCBTU0gK"


def get_bitbucket_branches_names(
    *,
    token: str,  # pylint: disable=unused-argument
    repo_id: str,  # pylint: disable=unused-argument
) -> tuple[str, ...]:
    return tuple(["main"])


async def get_token(
    *,
    credential: Credentials,
    loaders: Dataloaders,
) -> str | None:
    if not isinstance(credential.state.secret, OauthGitlabSecret):
        return None
    new_state = CredentialsState(
        modified_by=credential.state.modified_by,
        modified_date=datetime.now(tz=pytz.timezone("UTC")),
        name=credential.state.name,
        secret=OauthGitlabSecret(
            redirect_uri=credential.state.secret.redirect_uri,
            refresh_token="UFUzdCBTU0gK",
            access_token="TETzdCBTU0gK",
            valid_until=get_now_plus_delta(hours=2),
        ),
        is_pat=credential.state.is_pat,
        azure_organization=credential.state.azure_organization,
        type=credential.state.type,
    )
    await update_credential_state(
        current_value=credential.state,
        credential_id=credential.id,
        organization_id=credential.organization_id,
        state=new_state,
        force_update_owner=False,
    )
    loaders.credentials.clear_all()
    loaders.organization_credentials.clear(credential.organization_id)
    return "TETzdCBTU0gK"


async def get_covered_group(
    path: str,  # pylint: disable=unused-argument
    folder: str,  # pylint: disable=unused-argument
    group: str,  # pylint: disable=unused-argument
    git_roots: tuple[GitRoot, ...],  # pylint: disable=unused-argument
) -> set[str]:
    return {"devtest1@test.com"}


async def _get_missed_authors(
    *,
    loaders: Dataloaders,  # pylint: disable=unused-argument
    repository: CredentialsGitRepository,  # pylint: disable=unused-argument
) -> set[str]:
    return {"devtest2@test.com"}


def _get_bitbucket_authors(
    *,
    token: str,  # pylint: disable=unused-argument
    repo_id: str,  # pylint: disable=unused-argument
) -> tuple[dict, ...]:
    return tuple()


async def _get_oauth_missed_authors(
    *,
    repository: OGitRepository,  # pylint: disable=unused-argument
) -> set[str]:
    return {"devtest7@test.com"}


def _get_hub_commit_stats(
    token: str, repo_id: str  # pylint: disable=unused-argument
) -> tuple[GitHubCommit.GitCommit, ...]:
    return tuple()


def _get_gitlab_branches_names(
    token: str, project_id: str  # pylint: disable=unused-argument
) -> tuple[str, ...]:
    return tuple()


def mocked_pull_repositories(
    tmpdir: str, group_name: str, optional_repo_nickname: str
) -> None:
    dirname = os.path.dirname(__file__)
    filename = os.path.join(f"{dirname}/../refresh_toe_lines", "mocks")
    fusion_path = f"{tmpdir}/groups/{group_name}"
    if optional_repo_nickname:
        shutil.copytree(
            f"{filename}/{optional_repo_nickname}",
            f"{fusion_path}/{optional_repo_nickname}",
        )
    else:
        shutil.copytree(filename, fusion_path)

    git_mocks = glob.glob(f"{fusion_path}/*/.git_mock")
    for git_mock in git_mocks:
        os.rename(git_mock, git_mock.replace("/.git_mock", "/.git"))


def _get_github_branches_names(
    token: str, repo_id: str  # pylint: disable=unused-argument
) -> tuple[str, ...]:
    return tuple()


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.mark.parametrize(
    ("email", "role"),
    (("admin@gmail.com", "admin"),),
)
async def test_get_organization_ver_1(
    populate: bool,
    email: str,
    role: str,
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    org_name: str = "orgtest"
    with (
        mock.patch(
            "roots.validations.get_azure_token",
            side_effect=get_azure_token,
        ),
        mock.patch("roots.validations.get_token", side_effect=get_token),
        mock.patch(
            (
                "api.resolvers.credentials.integration_repositories."
                "get_credentials_repositories"
            ),
            side_effect=get_credentials_repositories,
        ),
    ):
        result: dict[str, Any] = await get_result(
            user=email, org=org_id, should_get_token=True
        )
    assert "errors" not in result
    assert result["data"]["organization"]["id"] == org_id
    assert result["data"]["organization"]["name"] == org_name.lower()
    assert (
        result["data"]["organization"]["integrationRepositoriesConnection"][
            "edges"
        ][0]["node"]["defaultBranch"]
        == "main"
    )
    assert (
        result["data"]["organization"]["integrationRepositoriesConnection"][
            "edges"
        ][0]["node"]["lastCommitDate"]
        == "2022-11-02 04:37:57"
    )
    assert result["data"]["organization"]["userRole"] == role
    assert result["data"]["organization"]["coveredAuthors"] == 0
    assert result["data"]["organization"]["coveredRepositories"] == 0
    assert result["data"]["organization"]["missedAuthors"] == 0
    assert result["data"]["organization"]["missedRepositories"] == 0
    assert len(result["data"]["organization"]["credentials"]) == 6
    assert (
        result["data"]["organization"]["credentials"][0]["token"]
        == "QEQzdCBTU0gK"
    )
    assert (
        result["data"]["organization"]["credentials"][1]["token"]
        == "TETzdCBTU0gK"
    )
    assert result["data"]["organization"]["credentials"][2]["token"] is None
    assert (
        result["data"]["organization"]["credentials"][3]["token"]
        == "DEDzdCBTU0gK"
    )
    assert (
        result["data"]["organization"]["credentials"][4]["token"]
        == "SDSzdCBTU0gK"
    )
    assert (
        result["data"]["organization"]["credentials"][5]["token"]
        == "VGVzdCBTU0gK"
    )
    assert (
        result["data"]["organization"]["credentials"][1][
            "integrationRepositories"
        ][0]["url"]
        == "ssh://git@test.com:v3/testprojects/_git/secondrepor"
    )

    loaders = get_new_context()
    current_repositories = (
        await loaders.organization_unreliable_integration_repositories.load(
            (org_id, None, None)
        )
    )
    assert len(current_repositories) == 1
    assert (
        next(
            (
                repository
                for repository in current_repositories
                if repository.branch == "trunk"
            ),
            None,
        )
        is None
    )

    with (
        mock.patch(
            "db_model.azure_repositories.get._get_repositories",
            side_effect=get_repositories,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_repositories_commits",
            side_effect=get_repositories_commits,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_bitbucket_repositories",
            side_effect=_get_bitbucket_repositories,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_gitlab_projects",
            side_effect=_get_lab_repositories_stats,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_github_repos",
            side_effect=_get_hub_repositories_stats,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_gitlab_last_commit",
            side_effect=_get_lab_last_commit_stats,
        ),
        mock.patch(
            "outside_repositories.domain.get_gitlab_branches_names",
            side_effect=_get_gitlab_branches_names,
        ),
        mock.patch(
            "outside_repositories.domain.get_account_names",
            side_effect=get_account_names,
        ),
        mock.patch(
            "outside_repositories.domain.get_github_branches_names",
            side_effect=_get_github_branches_names,
        ),
        mock.patch(
            "outside_repositories.domain.get_bitbucket_branches_names",
            side_effect=get_bitbucket_branches_names,
        ),
        mock.patch(
            "outside_repositories.domain.get_azure_branches_names",
            side_effect=get_azure_branches_names,
        ),
    ):
        await update_organization_repositories()

    with (
        mock.patch(
            "outside_repositories.domain.pull_repositories",
            side_effect=mocked_pull_repositories,
        ),
        mock.patch(
            "outside_repositories.utils.get_covered_group",
            side_effect=get_covered_group,
        ),
        mock.patch(
            "outside_repositories.domain._get_missed_authors",
            side_effect=_get_missed_authors,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_repositories",
            side_effect=get_repositories,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_repositories_commits",
            side_effect=get_repositories_commits,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_gitlab_projects",
            side_effect=_get_lab_repositories_stats,
        ),
        mock.patch(
            "outside_repositories.domain.get_azure_branches_names",
            side_effect=get_azure_branches_names,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_bitbucket_repositories",
            side_effect=_get_bitbucket_repositories,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_gitlab_commit",
            side_effect=_get_lab_commit_stats,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_github_repos",
            side_effect=_get_hub_repositories_stats,
        ),
        mock.patch(
            "outside_repositories.domain.get_gitlab_branches_names",
            side_effect=_get_gitlab_branches_names,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_github_repos_commits",
            side_effect=_get_hub_commit_stats,
        ),
        mock.patch(
            "outside_repositories.domain.get_account_names",
            side_effect=get_account_names,
        ),
        mock.patch(
            "outside_repositories.domain._get_oauth_missed_authors",
            side_effect=_get_oauth_missed_authors,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_bitbucket_authors",
            side_effect=_get_bitbucket_authors,
        ),
    ):
        await update_organization_overview()

    with (
        mock.patch(
            "roots.validations.get_azure_token",
            side_effect=get_azure_token,
        ),
        mock.patch("roots.validations.get_token", side_effect=get_token),
        mock.patch(
            (
                "api.resolvers.credentials.integration_repositories."
                "get_credentials_repositories"
            ),
            side_effect=get_credentials_repositories,
        ),
    ):
        result = await get_result(user=email, org=org_id)
    assert "errors" not in result
    assert result["data"]["organization"]["coveredAuthors"] == 1
    assert result["data"]["organization"]["coveredRepositories"] == 1
    assert result["data"]["organization"]["missedAuthors"] == 2
    assert result["data"]["organization"]["missedRepositories"] == 3

    loaders.organization_unreliable_integration_repositories.clear_all()
    current_repositories = (
        await loaders.organization_unreliable_integration_repositories.load(
            (org_id, None, None)
        )
    )
    assert len(current_repositories) == 3
    assert (
        next(
            (
                repository
                for repository in current_repositories
                if repository.branch == "refs/head/trunk"
            ),
            None,
        )
        is not None
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.mark.parametrize(
    ("email", "role", "permissions"),
    (("admin@gmail.com", "admin", 27),),
)
async def test_get_organization_ver_2(
    populate: bool,
    email: str,
    role: str,
    permissions: int,
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    org_name: str = "orgtest"
    org_stakeholders: list[str] = [
        "admin@gmail.com",
        "architect@gmail.com",
        "hacker@gmail.com",
        "reattacker@gmail.com",
        "resourcer@gmail.com",
        "reviewer@gmail.com",
        "service_forces@gmail.com",
        "user@gmail.com",
        "user_manager@gmail.com",
        "vulnerability_manager@gmail.com",
    ]
    with (
        mock.patch(
            "roots.validations.get_azure_token",
            side_effect=get_azure_token,
        ),
        mock.patch("roots.validations.get_token", side_effect=get_token),
        mock.patch(
            (
                "api.resolvers.credentials.integration_repositories."
                "get_credentials_repositories"
            ),
            side_effect=get_credentials_repositories,
        ),
    ):
        result: dict[str, Any] = await get_result(user=email, org=org_id)
    groups: list[str] = [
        group["name"] for group in result["data"]["organization"]["groups"]
    ]
    stakeholders: list[str] = [
        stakeholder["email"]
        for stakeholder in result["data"]["organization"]["stakeholders"]
    ]
    assert "errors" not in result
    assert result["data"]["organization"]["id"] == org_id
    assert result["data"]["organization"]["inactivityPeriod"] == 180
    assert result["data"]["organization"]["maxAcceptanceDays"] == 90
    assert result["data"]["organization"]["maxAcceptanceSeverity"] == 7
    assert result["data"]["organization"]["maxNumberAcceptances"] == 4
    assert result["data"]["organization"]["minAcceptanceSeverity"] == 3
    assert result["data"]["organization"]["minBreakingSeverity"] == 2
    assert result["data"]["organization"]["vulnerabilityGracePeriod"] == 5
    assert result["data"]["organization"]["name"] == org_name.lower()
    assert sorted(groups) == sorted(["group1", "group3", "unittesting"])
    assert sorted(stakeholders) == sorted(org_stakeholders)
    assert (
        result["data"]["organization"]["integrationRepositoriesConnection"][
            "edges"
        ][0]["node"]["defaultBranch"]
        == "refs/heads/main"
    )
    assert (
        result["data"]["organization"]["integrationRepositoriesConnection"][
            "edges"
        ][0]["node"]["url"]
        == "https://git@test.com/testprojects/sixthtrepo.git"
    )
    assert len(result["data"]["organization"]["permissions"]) == permissions
    assert result["data"]["organization"]["userRole"] == role
    assert result["data"]["organization"]["coveredAuthors"] == 1
    assert result["data"]["organization"]["coveredRepositories"] == 1
    assert result["data"]["organization"]["missedAuthors"] == 2
    assert result["data"]["organization"]["missedRepositories"] == 3
    assert len(result["data"]["organization"]["credentials"]) == 6
    assert (
        result["data"]["organization"]["credentials"][0]["oauthType"]
        == "BITBUCKET"
    )
    assert (
        result["data"]["organization"]["credentials"][1]["oauthType"]
        == "GITLAB"
    )
    assert result["data"]["organization"]["credentials"][2]["oauthType"] == ""
    assert (
        result["data"]["organization"]["credentials"][3]["oauthType"]
        == "AZURE"
    )
    assert (
        result["data"]["organization"]["credentials"][4]["oauthType"]
        == "GITHUB"
    )
    assert result["data"]["organization"]["credentials"][1]["isPat"] is False
    assert (
        result["data"]["organization"]["credentials"][2]["name"] == "SSH Key"
    )
    assert result["data"]["organization"]["credentials"][2]["isToken"] is False
    assert result["data"]["organization"]["credentials"][2]["key"] is not None
    assert result["data"]["organization"]["credentials"][5]["isPat"] is True
    assert result["data"]["organization"]["credentials"][5]["isToken"] is True
    assert result["data"]["organization"]["credentials"][5]["key"] is None
    assert (
        result["data"]["organization"]["credentials"][5]["name"] == "pat token"
    )
    assert result["data"]["organization"]["credentials"][5]["oauthType"] == ""

    loaders = get_new_context()
    current_repositories = (
        await loaders.organization_unreliable_integration_repositories.load(
            (org_id, None, None)
        )
    )
    assert len(current_repositories) == 3

    with (
        mock.patch(
            "db_model.azure_repositories.get._get_repositories",
            side_effect=get_repositories,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_repositories_commits",
            side_effect=get_repositories_commits,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_bitbucket_repositories",
            side_effect=_get_bitbucket_repositories,
        ),
        mock.patch(
            "outside_repositories.domain.get_azure_branches_names",
            side_effect=get_azure_branches_names,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_gitlab_projects",
            side_effect=get_lab_repositories_stats,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_github_repos",
            side_effect=get_hub_repositories_stats,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_gitlab_last_commit",
            side_effect=get_lab_last_commit_stats,
        ),
        mock.patch(
            "outside_repositories.domain.get_gitlab_branches_names",
            side_effect=_get_gitlab_branches_names,
        ),
        mock.patch(
            "outside_repositories.domain.get_account_names",
            side_effect=get_account_names,
        ),
        mock.patch(
            "outside_repositories.domain.get_github_branches_names",
            side_effect=_get_github_branches_names,
        ),
        mock.patch(
            "outside_repositories.domain.get_bitbucket_branches_names",
            side_effect=get_bitbucket_branches_names,
        ),
    ):
        await update_organization_repositories()

    with (
        mock.patch(
            "outside_repositories.domain.pull_repositories",
            side_effect=mocked_pull_repositories,
        ),
        mock.patch(
            "outside_repositories.utils.get_covered_group",
            side_effect=get_covered_group,
        ),
        mock.patch(
            "outside_repositories.domain._get_missed_authors",
            side_effect=_get_missed_authors,
        ),
        mock.patch(
            "outside_repositories.domain.get_azure_branches_names",
            side_effect=get_azure_branches_names,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_repositories",
            side_effect=get_repositories,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_repositories_commits",
            side_effect=get_repositories_commits,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_gitlab_projects",
            side_effect=get_lab_repositories_stats,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_gitlab_commit",
            side_effect=get_lab_commit_stats,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_github_repos",
            side_effect=get_hub_repositories_stats,
        ),
        mock.patch(
            "outside_repositories.domain.get_gitlab_branches_names",
            side_effect=_get_gitlab_branches_names,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_github_repos_commits",
            side_effect=_get_hub_commit_stats,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_bitbucket_repositories",
            side_effect=_get_bitbucket_repositories,
        ),
        mock.patch(
            "outside_repositories.domain.get_account_names",
            side_effect=get_account_names,
        ),
        mock.patch(
            "outside_repositories.domain._get_oauth_missed_authors",
            side_effect=_get_oauth_missed_authors,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_bitbucket_authors",
            side_effect=_get_bitbucket_authors,
        ),
    ):
        await update_organization_overview()

    with (
        mock.patch(
            "roots.validations.get_azure_token",
            side_effect=get_azure_token,
        ),
        mock.patch("roots.validations.get_token", side_effect=get_token),
        mock.patch(
            (
                "api.resolvers.credentials.integration_repositories."
                "get_credentials_repositories"
            ),
            side_effect=get_credentials_repositories,
        ),
    ):
        result = await get_result(user=email, org=org_id)
    assert "errors" not in result
    assert result["data"]["organization"]["coveredAuthors"] == 1
    assert result["data"]["organization"]["coveredRepositories"] == 1
    assert result["data"]["organization"]["missedAuthors"] == 4
    assert result["data"]["organization"]["missedRepositories"] == 5

    loaders.organization_unreliable_integration_repositories.clear_all()
    current_repositories = (
        await loaders.organization_unreliable_integration_repositories.load(
            (org_id, None, None)
        )
    )
    assert len(current_repositories) == 5
    assert (
        next(
            (
                repository
                for repository in current_repositories
                if repository.branch == "refs/head/trunk"
            ),
            None,
        )
        is not None
    )

    result_remove = await remove_credentials(
        user="user_manager@fluidattacks.com",
        credentials_id="1a5dacda-1d52-465c-9158-f6fd5dfe0998",
        organization_id=org_id,
    )
    assert "errors" not in result_remove
    assert "success" in result_remove["data"]["removeCredentials"]
    assert result_remove["data"]["removeCredentials"]["success"]

    result_remove = await remove_credentials(
        user="user_manager@fluidattacks.com",
        credentials_id="c9ecb25c-8d9f-422c-abc4-44c0c700a760",
        organization_id=org_id,
    )
    assert "errors" not in result_remove
    assert "success" in result_remove["data"]["removeCredentials"]
    assert result_remove["data"]["removeCredentials"]["success"]

    result_remove = await remove_credentials(
        user="user_manager@fluidattacks.com",
        credentials_id="5b81d698-a5bc-4dda-bdf9-40d0725358b4",
        organization_id=org_id,
    )
    assert "errors" not in result_remove
    assert "success" in result_remove["data"]["removeCredentials"]
    assert result_remove["data"]["removeCredentials"]["success"]

    result_remove = await remove_credentials(
        user="user_manager@fluidattacks.com",
        credentials_id="5990e0ec-dc8f-4c9a-82cc-9da9fbb35c11",
        organization_id=org_id,
    )
    assert "errors" not in result_remove
    assert "success" in result_remove["data"]["removeCredentials"]
    assert result_remove["data"]["removeCredentials"]["success"]

    result_remove = await remove_credentials(
        user="user_manager@fluidattacks.com",
        credentials_id="158d1f7f-65c5-4c79-85e3-de3acfe03774",
        organization_id=org_id,
    )
    assert "errors" not in result_remove
    assert "success" in result_remove["data"]["removeCredentials"]
    assert result_remove["data"]["removeCredentials"]["success"]

    loaders.organization_unreliable_integration_repositories.clear_all()
    current_repositories = (
        await loaders.organization_unreliable_integration_repositories.load(
            (org_id, None, None)
        )
    )
    assert len(current_repositories) == 5

    await update_organization_repositories()
    with mock.patch(
        "outside_repositories.domain.pull_repositories",
        side_effect=mocked_pull_repositories,
    ):
        await update_organization_overview()

    loaders.organization_unreliable_integration_repositories.clear_all()
    loaders.organization_credentials.clear_all()
    loaders.group_roots.clear_all()

    updated_repositories = (
        await loaders.organization_unreliable_integration_repositories.load(
            (org_id, None, None)
        )
    )
    assert len(updated_repositories) == 0

    with (
        mock.patch(
            "roots.validations.get_azure_token",
            side_effect=get_azure_token,
        ),
        mock.patch("roots.validations.get_token", side_effect=get_token),
        mock.patch(
            (
                "api.resolvers.credentials.integration_repositories."
                "get_credentials_repositories"
            ),
            side_effect=get_credentials_repositories,
        ),
    ):
        result = await get_result(user=email, org=org_id)
    assert "errors" not in result
    assert result["data"]["organization"]["coveredAuthors"] == 0
    assert result["data"]["organization"]["coveredRepositories"] == 1
    assert result["data"]["organization"]["missedAuthors"] == 0
    assert result["data"]["organization"]["missedRepositories"] == 0


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.mark.parametrize(
    ("email", "role", "permissions"),
    (
        ("user@gmail.com", "user", 3),
        ("user_manager@gmail.com", "user_manager", 29),
        ("vulnerability_manager@gmail.com", "user", 3),
        ("hacker@gmail.com", "user", 3),
        ("reattacker@gmail.com", "user", 3),
        ("resourcer@gmail.com", "user", 3),
        ("reviewer@gmail.com", "user", 3),
        ("customer_manager@fluidattacks.com", "customer_manager", 26),
    ),
)
async def test_get_organization_ver_3(
    populate: bool, email: str, role: str, permissions: int
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    org_name: str = "orgtest"
    org_groups: list[str] = [
        "group1",
    ]
    with (
        mock.patch(
            "roots.validations.get_azure_token",
            side_effect=get_azure_token,
        ),
        mock.patch("roots.validations.get_token", side_effect=get_token),
        mock.patch(
            (
                "api.resolvers.credentials.integration_repositories."
                "get_credentials_repositories"
            ),
            side_effect=get_credentials_repositories,
        ),
    ):
        result: dict[str, Any] = await get_result(user=email, org=org_id)
    groups: list[str] = [
        group["name"] for group in result["data"]["organization"]["groups"]
    ]
    assert result["data"]["organization"]["id"] == org_id
    assert result["data"]["organization"]["inactivityPeriod"] == 180
    assert result["data"]["organization"]["maxAcceptanceDays"] == 90
    assert result["data"]["organization"]["maxAcceptanceSeverity"] == 7
    assert result["data"]["organization"]["maxNumberAcceptances"] == 4
    assert result["data"]["organization"]["minAcceptanceSeverity"] == 3
    assert result["data"]["organization"]["minBreakingSeverity"] == 2
    assert result["data"]["organization"]["vulnerabilityGracePeriod"] == 5
    assert result["data"]["organization"]["name"] == org_name.lower()
    assert org_groups[0] in groups
    assert len(result["data"]["organization"]["permissions"]) == permissions
    assert result["data"]["organization"]["userRole"] == role


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.mark.parametrize(
    ("email", "role", "permissions"),
    (("admin@gmail.com", "admin", 27),),
)
async def test_get_organization_default_values(
    populate: bool, email: str, role: str, permissions: int
) -> None:
    assert populate
    org_id: str = "ORG#8a7c8089-92df-49ec-8c8b-ee83e4ff3256"
    org_name: str = "acme"
    org_stakeholders: list[str] = [
        "admin@gmail.com",
    ]
    with (
        mock.patch(
            "roots.validations.get_azure_token",
            side_effect=get_azure_token,
        ),
        mock.patch("roots.validations.get_token", side_effect=get_token),
        mock.patch(
            (
                "api.resolvers.credentials.integration_repositories."
                "get_credentials_repositories"
            ),
            side_effect=get_credentials_repositories,
        ),
    ):
        result: dict[str, Any] = await get_result(user=email, org=org_id)
    groups: list[str] = [
        group["name"] for group in result["data"]["organization"]["groups"]
    ]
    stakeholders: list[str] = [
        stakeholder["email"]
        for stakeholder in result["data"]["organization"]["stakeholders"]
    ]
    assert "errors" not in result
    assert result["data"]["organization"]["id"] == org_id
    assert result["data"]["organization"]["inactivityPeriod"] == 90
    assert result["data"]["organization"]["maxAcceptanceDays"] is None
    assert result["data"]["organization"]["maxAcceptanceSeverity"] == 10.0
    assert result["data"]["organization"]["maxNumberAcceptances"] is None
    assert result["data"]["organization"]["minAcceptanceSeverity"] == 0.0
    assert result["data"]["organization"]["minBreakingSeverity"] is None
    assert result["data"]["organization"]["vulnerabilityGracePeriod"] == 0
    assert result["data"]["organization"]["name"] == org_name.lower()
    assert sorted(groups) == []
    assert sorted(stakeholders) == org_stakeholders
    assert len(result["data"]["organization"]["permissions"]) == permissions
    assert result["data"]["organization"]["userRole"] == role
    assert len(result["data"]["organization"]["credentials"]) == 0


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.mark.parametrize(
    ("email", "verification_code"),
    (
        ("admin@gmail.com", None),
        ("admin@gmail.com", "123123"),
    ),
)
async def test_get_org_vulnerabilities_url(
    populate: bool, email: str, verification_code: str | None
) -> None:
    assert populate
    org_id: str = "ORG#8a7c8089-92df-49ec-8c8b-ee83e4ff3256"
    result: dict[str, Any] = await get_vulnerabilities_url(
        user=email,
        org_id=org_id,
        verification_code=verification_code,
        session_jwt=None,
    )
    if verification_code:
        assert "errors" not in result
        assert (
            result["data"]["organization"]["vulnerabilitiesUrl"]
            == "https://test.com"
        )
    else:
        assert "errors" in result
        assert result["errors"][0]["message"] == str(
            RequiredVerificationCode()
        )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.mark.parametrize(
    ("email", "verification_code"),
    (("admin@gmail.com", None),),
)
async def test_get_org_vulnerabilities_url_api(
    populate: bool, email: str, verification_code: str | None
) -> None:
    assert populate
    org_id: str = "ORG#8a7c8089-92df-49ec-8c8b-ee83e4ff3256"
    result_1: dict[str, Any] = await get_vulnerabilities_url(
        user=email,
        org_id=org_id,
        verification_code=verification_code,
        session_jwt=None,
    )
    assert "errors" in result_1
    assert result_1["errors"][0]["message"] == str(RequiredVerificationCode())

    ts_expiration_time: int = int(
        (datetime.utcnow() + timedelta(weeks=8)).timestamp()
    )
    result_jwt = await get_access_token(
        user=email,
        expiration_time=ts_expiration_time,
    )
    assert "errors" not in result_jwt
    assert result_jwt["data"]["updateAccessToken"]["success"]

    session_jwt: str = result_jwt["data"]["updateAccessToken"]["sessionJwt"]
    result_2: dict[str, Any] = await get_vulnerabilities_url(
        user=email,
        org_id=org_id,
        verification_code=verification_code,
        session_jwt=session_jwt,
    )

    assert "errors" not in result_2
    assert (
        result_2["data"]["organization"]["vulnerabilitiesUrl"]
        == "https://test.com"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.mark.parametrize(
    ["email", "org_name"],
    [
        [
            "admin@gmail.com",
            "orgtest",
        ],
    ],
)
async def test_get_org_events(
    populate: bool, email: str, org_name: str
) -> None:
    assert populate
    result: dict[str, Any] = await get_organization_events(
        user=email, org_name=org_name
    )
    groups = result["data"]["organizationId"]["groups"]
    group1_events = groups[0]["events"][0]
    group3_events = groups[1]["events"][0]
    unittesting_events = groups[2]["events"][0]
    assert "errors" not in result
    assert len(groups) == 3
    assert group1_events["groupName"] == "group1"
    assert group1_events["eventStatus"] == "OPEN"
    assert group1_events["eventDate"] == "2018-06-29 07:00:00"
    assert group3_events["groupName"] == "group3"
    assert group3_events["eventStatus"] == "SOLVED"
    assert group3_events["eventDate"] == "2018-06-30 07:00:00"
    assert unittesting_events["groupName"] == "unittesting"
    assert unittesting_events["eventStatus"] == "CREATED"
    assert unittesting_events["eventDate"] == "2018-08-27 07:00:00"
