import asyncclick as click
import asyncio
from git_self import (
    clone as _clone_from_client,
)
import os
from pathlib import (
    Path,
)
import shutil
from src.api.integrates import (
    get_git_root_credentials,
    get_group_git_roots,
)
from src.logger import (
    LOGGER,
)


async def _clone_repo(
    group_name: str,
    git_root_id: str,
    git_root_nickname: str,
    repo_url: str,
    repo_branch: str,
) -> None:
    repo_path = Path("groups") / group_name / git_root_nickname
    os.makedirs(repo_path, exist_ok=True)
    credentials = await get_git_root_credentials(group_name, git_root_id)
    if not credentials:
        LOGGER.error("no credentials found for %s", git_root_nickname)
        return None

    folder_to_clone_root, stderr = await _clone_from_client(
        repo_url,
        repo_branch,
        credential_key=credentials.get("key"),
        user=credentials.get("user"),
        password=credentials.get("password"),
        provider=credentials.get("oauthType"),
        token=credentials.get("token"),
        temp_dir=str(repo_path.parent.absolute()),
    )
    shutil.rmtree(repo_path, ignore_errors=True)
    if folder_to_clone_root:
        os.rename(folder_to_clone_root, repo_path)
    else:
        LOGGER.error("failed to clone: %s", stderr)


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
async def clone(group_name: str, git_root_nickname: str | None) -> bool:
    """Allows you to clone repositories from the client's servers."""
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
    await asyncio.gather(
        *[
            _clone_repo(
                group_name,
                root["id"],
                root["nickname"],
                root["url"],
                root["branch"],
            )
            for root in git_roots
        ]
    )
    return True
