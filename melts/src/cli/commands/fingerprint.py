import asyncclick as click
from datetime import (
    datetime,
)
from git.repo import (
    Repo,
)
import os
from pathlib import (
    Path,
)
from src.logger import (
    LOGGER,
)


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
def get_fingerprint(group_name: str, git_root_nickname: str | None) -> bool:
    """Get the hash and date of every folder in the group"""
    results = []
    max_hash = ""
    max_date = datetime.fromtimestamp(0)
    path = Path("groups") / group_name
    if not os.path.exists(path):
        LOGGER.error("There is no project with the name: %s", group_name)
        LOGGER.info("Please run fingerprint inside a project or use subs")
        return False
    for repo in (
        r
        for r in os.listdir(path)
        if os.path.isdir(path / r)
        if (r == git_root_nickname if git_root_nickname else True)
    ):
        git_repo = Repo(
            os.path.join(path, repo), search_parent_directories=True
        )
        hashr = git_repo.head.commit.hexsha
        date = datetime.fromtimestamp(git_repo.head.commit.authored_date)
        max_date = max_date or date
        if date >= max_date:
            max_date = date
            max_hash = hashr
        results.append((repo, hashr, date.isoformat()))
    if not results:
        LOGGER.error(
            "There is not any folder in fusion - Subs: %s", group_name
        )
        return False
    output_bar = "-" * 84
    output_fmt = "{:^59} {:^7} {:^16}"
    LOGGER.info(output_bar)
    LOGGER.info(output_fmt.format("Repository", "Hash", "Date"))
    LOGGER.info(output_bar)
    for params in sorted(results):
        LOGGER.info(output_fmt.format(*params))
    LOGGER.info(output_bar)
    LOGGER.info(
        output_fmt.format(len(results), max_hash, max_date.isoformat())
    )
    return True
