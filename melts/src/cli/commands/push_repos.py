from aioextensions import (
    collect,
)
import aiohttp
import asyncclick as click
from git import (
    GitError,
)
from git.repo import (
    Repo,
)
import os
from pathlib import (
    Path,
)
from src.api.integrates import (
    get_git_root_upload_url,
    get_group_git_roots,
    update_git_root_cloning_status,
)
from src.logger import (
    LOGGER,
)
import tarfile
import tempfile
from uuid import (
    uuid4,
)


def create_git_root_tar_file(
    root_nickname: str, repo_path: str, output_path: str | None = None
) -> bool:
    git_dir = os.path.normpath(f"{repo_path}/.git")
    with tarfile.open(
        output_path or f"{root_nickname}.tar.gz", "w:gz"
    ) as tar_handler:
        if os.path.exists(git_dir):
            tar_handler.add(
                git_dir, arcname=f"{root_nickname}/.git", recursive=True
            )
            return True
        return False


async def _push_repo(group_name: str, git_root: dict) -> bool:
    upload_url = await get_git_root_upload_url(group_name, git_root["id"])
    if not upload_url:
        LOGGER.error("Upload URL not found")
        return False

    repo_path: Path = Path("groups") / group_name / git_root["nickname"]
    try:
        Repo(repo_path)
    except GitError:
        LOGGER.error("Repo not found: %s", repo_path.absolute().as_uri())
        return False

    current_commit = Repo(
        str(repo_path.absolute()), search_parent_directories=True
    ).head.object.hexsha

    if current_commit == git_root["cloningStatus"]["commit"]:
        await update_git_root_cloning_status(
            group_name,
            git_root["id"],
            "OK",
            commit=current_commit,
            message=(
                "The repository was not cloned as no new changes were detected"
            ),
        )
        LOGGER.info("No changes detected, no need to update the repository")
        return True

    with tempfile.TemporaryDirectory(
        prefix=f"integrates_clone_{group_name}_", ignore_cleanup_errors=True
    ) as temp_dir:
        tar_path = Path(temp_dir) / f"{uuid4().hex}.tar.gz"
        create_git_root_tar_file(
            git_root["nickname"],
            str(repo_path.absolute()),
            str(tar_path.absolute()),
        )
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(
                total=3600, sock_connect=30, sock_read=600
            )
        ) as session:
            with open(tar_path, "rb") as handler:
                file_size = handler.seek(0, 2)
                handler.seek(0)
                request = await session.put(
                    upload_url,
                    data=handler,
                    headers={
                        "Content-Type": "application/octet-stream",
                        "Content-Length": str(file_size),
                    },
                )

                if request.status != 200:
                    response = await request.text()
                    raise Exception(f"Error uploading file: {response}")

        await update_git_root_cloning_status(
            group_name,
            git_root["id"],
            "OK",
            commit=current_commit,
            message="Cloned successfully",
        )
    return True


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
async def push_repos(
    group_name: str, git_root_nickname: str | None = None
) -> bool:
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
    await collect(
        (_push_repo(group_name, git_root) for git_root in git_roots), workers=5
    )
    return True
