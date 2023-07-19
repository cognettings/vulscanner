from alive_progress import (
    alive_bar,
)
import asyncclick as click
import asyncio
from contextlib import (
    suppress,
)
from datetime import (
    datetime,
    UTC,
)
from git import (
    GitError,
)
from git_self import (
    download_repo_from_s3,
    get_head_commit,
)
from more_itertools import (
    mark_ends,
)
import os
from pathlib import (
    Path,
)
from src.api.integrates import (
    get_git_root_download_url,
    get_group_git_roots,
)
from src.logger import (
    LOGGER,
)
from typing import (
    Any,
)


def calculate_days_ago(date: datetime) -> int:
    """
    Return passed days after a provided date

    param: date: provided date to calculate passed days
    """
    passed_days = datetime.utcnow().replace(tzinfo=UTC) - date.replace(
        tzinfo=UTC
    )

    return passed_days.days


def notify_out_of_scope(
    nickname: str,
    gitignore: str,
) -> None:
    LOGGER.info("Please remember the scope for : %s", nickname)

    for _, is_last, line in mark_ends(gitignore):
        if is_last:
            LOGGER.info("    - %s\n", line)
        else:
            LOGGER.info("    - %s", line)


def _repo_already_exists(root: dict[str, Any], repo_path: str) -> bool:
    with suppress(GitError):
        if (
            (commit := root.get("cloningStatus", {}).get("commit"))
            and (branch := root.get("branch"))
            and (local_commit := get_head_commit(Path(repo_path), branch))
            and (local_commit == commit)
        ):
            LOGGER.debug("%s repository already exists", root["nickname"])
            return True
    return False


def _delete_file_repo(file_path: str) -> None:
    if os.path.isfile(file_path):
        os.remove(file_path)


async def download_repo(
    group_name: str,
    root: dict[str, Any],
    progress_bar: Any,
) -> bool:
    url = await get_git_root_download_url(group_name, root["id"])
    if not url:
        LOGGER.error(
            "Cannot find download url for %s repository", root["nickname"]
        )
        return False

    repo_path = Path("groups") / group_name / root["nickname"]
    config_file_path = repo_path / ".git" / "config"
    os.makedirs(repo_path.parent, exist_ok=True)

    if _repo_already_exists(root, str(repo_path.absolute())):
        if progress_bar:
            progress_bar()
        _delete_file_repo(str(config_file_path.absolute()))
        return True

    if await download_repo_from_s3(url, repo_path, root["gitignore"]):
        if progress_bar:
            progress_bar()
        _delete_file_repo(str(config_file_path.absolute()))
        return True
    return False


@click.command()
@click.option(
    "--group",
    "group_name",
    required=True,
    help="Specify the name of the group you want to clone.",
)
@click.option(
    "--root",
    "git_root_nickname",
    required=False,
    help=(
        "Clone a specific repository. Provide the name"
        " of the repository you want to clone."
    ),
)
async def pull_repos(group_name: str, git_root_nickname: str | None) -> None:
    """Get group repositories"""
    git_roots = await get_group_git_roots(group_name)
    git_roots = [
        git_root
        for git_root in git_roots
        if git_root.get("state") == "ACTIVE"
        and (
            git_root["nickname"] == git_root_nickname
            if git_root_nickname is not None
            else True
        )
    ]
    with alive_bar(len(git_roots), enrich_print=False) as progress_bar:
        results: list[bool] = await asyncio.gather(
            *[
                download_repo(group_name, root, progress_bar=progress_bar)
                for root in git_roots
            ]
        )
        for root, result in zip(git_roots, results):
            if result:
                notify_out_of_scope(root["nickname"], root["gitignore"])
            if date := root.get("lastCloningStatusUpdate"):
                LOGGER.info(
                    "Data for %s was uploaded to S3 %i days ago",
                    root["nickname"],
                    calculate_days_ago(datetime.fromisoformat(date)),
                )
            else:
                LOGGER.info(
                    "root %s does not have repos uploaded to s3",
                    root["nickname"],
                )
