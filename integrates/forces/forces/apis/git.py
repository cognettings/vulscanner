from contextlib import (
    suppress,
)
from datetime import (
    timezone,
)
from forces.apis.integrates.api import (
    get_git_remotes,
)
from forces.model import (
    ForcesConfig,
)
from forces.utils.logs import (
    log,
)
from git.exc import (
    InvalidGitRepositoryError,
)
from git.objects.commit import (
    Commit,
)
from git.repo import (
    Repo,
)
import os
import re

# Contants
DEFAULT_COLUMN_VALUE: str = "unable to retrieve"
REGEXES_GIT_REPO_FROM_ORIGIN = [
    # https://xxxx.visualstudio.com/xxx/_git/repo_name
    re.compile(r"^.*visualstudio.com\/.*\/_git\/(.*)$"),
    # git@ssh.dev.azure.com:v3/xxx/repo_name
    re.compile(r"^.*azure.com:.*\/(.*)"),
    # https://xxx@gitlab.com/xxx/repo_name.git
    re.compile(
        (
            r"^.*(?:gitlab|github|bitbucket).(?:com|org)"
            r"(?::|\/).*\/(?:(.*?)(?:\.git)?)$"
        )
    ),
]


def get_repo_name_from_vars() -> str | None:
    common_names = {
        "BUILD_REPOSITORY_NAME",  # Azure devops
        "CI_PROJECT_NAME",  # gitlab-ci
        "CIRCLE_PROJECT_REPONAME",  # circleci
        "BITBUCKET_REPO_FULL_NAME",  # bitbucket
        "REPO_NAME",  # google cloud
    }
    for var in common_names:
        if name := os.environ.get(var):
            return name
    return None


def extract_repo_name(pattern: str) -> str | None:
    for regex in REGEXES_GIT_REPO_FROM_ORIGIN:
        match = regex.match(pattern)
        if match and match.group(1):
            return match.group(1)

    with suppress(IndexError):
        return pattern.split("/")[-1].split(".")[0]

    return None


def get_repository_metadata(repo_path: str = ".") -> dict[str, str]:
    git_branch = DEFAULT_COLUMN_VALUE
    git_commit = DEFAULT_COLUMN_VALUE
    git_commit_author = DEFAULT_COLUMN_VALUE
    git_commit_authored_date = DEFAULT_COLUMN_VALUE
    git_origin = DEFAULT_COLUMN_VALUE
    git_repo = DEFAULT_COLUMN_VALUE

    if name := get_repo_name_from_vars():
        # Repository name obtained from environment
        git_repo = name

    with suppress(InvalidGitRepositoryError):
        repo = Repo(repo_path, search_parent_directories=True)
        # Repository detected
        head_commit: Commit = repo.head.commit

        with suppress(TypeError):
            git_branch = repo.active_branch.name

        git_commit = head_commit.hexsha
        git_commit_author = (
            f"{head_commit.author.name} <{head_commit.author.email}>"
        )
        git_commit_authored_date = head_commit.authored_datetime.astimezone(
            timezone.utc
        ).isoformat()

        origins = list(repo.remote().urls)
        with suppress(IndexError):
            git_origin = origins[0]

        if git_repo == DEFAULT_COLUMN_VALUE and (
            name := extract_repo_name(git_origin)
        ):
            # Repository name obtained from origin
            git_repo = name
        elif git_repo == DEFAULT_COLUMN_VALUE:
            with suppress(IndexError):
                # Repository name obtained from current dir"
                git_repo = os.path.basename(os.path.split(repo.git_dir)[0])

    return {
        "git_branch": git_branch,
        "git_commit": git_commit,
        "git_commit_author": git_commit_author,
        "git_commit_authored_date": git_commit_authored_date,
        "git_repo": git_repo,
        "git_origin": git_origin,
    }


async def check_remotes(config: ForcesConfig) -> bool:
    if not config.repository_name:
        # if the repo is not specified, it is not required to validate
        # the remotes
        return True

    api_remotes = await get_git_remotes(config.group)

    match_remotes = tuple(
        remote
        for remote in api_remotes
        if config.repository_name
        in {extract_repo_name(remote["url"]), remote["nickname"]}
    )
    if not match_remotes:
        await log(
            "error",
            "The %s repository has not been registered in ARM",
            f"[bright_yellow]{config.repository_name}[/]",
        )
        return bool(match_remotes)

    has_active_remotes = any(
        remote for remote in match_remotes if remote["state"] == "ACTIVE"
    )
    if not has_active_remotes:
        await log(
            "error",
            "The %s repository is inactive",
            f"[bright_yellow]{config.repository_name}[/]",
        )

    return has_active_remotes
