from git.cmd import (
    Git,
)
from git.exc import (
    GitCommandError,
    GitCommandNotFound,
)
from numpy import (
    ndarray,
)
import os
import re
from sorts.constants import (
    RENAME_REGEX,
    STAT_REGEX,
)
from sorts.utils.logs import (
    log_exception,
)
from typing import (
    TypedDict,
)


class GitMetrics(TypedDict):
    author_email: list[str]
    commit_hash: list[str]
    date_iso_format: list[str]
    stats: list[str]


def get_bad_repos(fusion_path: str) -> list[str]:
    """Filters repositories which have issues running git commands"""
    return [
        repo
        for repo in os.listdir(fusion_path)
        if not test_repo(os.path.join(fusion_path, repo))
    ]


def _validate_change(
    changed_name: bool, file_info: str, line: str
) -> tuple[bool, str]:
    if "=>" in line:
        match = re.match(RENAME_REGEX, line.strip("\n").split("\t")[2])
        if match:
            path_info: dict[str, str] = match.groupdict()
            if file_info == (
                f'{path_info["pre_path"]}{path_info["new_name"]}'
                f'{path_info["post_path"]}'
            ):
                changed_name = True
                file_info = (
                    f'{path_info["pre_path"]}'
                    f'{path_info["old_name"]}'
                    f'{path_info["post_path"]}'
                )
    return changed_name, file_info


def get_log_file_metrics(
    logs_dir: str, repo: str, file_info: str
) -> GitMetrics:
    """Read the log file and extract the author, hash, date and diff"""
    git_metrics: GitMetrics = GitMetrics(
        author_email=[], commit_hash=[], date_iso_format=[], stats=[]
    )
    cursor: str = ""
    with open(
        os.path.join(logs_dir, f"{repo}.log"),
        "r",
        encoding="utf8",
    ) as log_file:
        for line in log_file:
            # An empty line marks the start of a new commit diff
            if not line.strip("\n"):
                cursor = "info"
                continue
            # Next, there is a line with the format 'Hash,Author,Date'
            if cursor == "info":
                info: list[str] = line.strip("\n").split(",")
                commit: str = info[0]
                author: str = info[1]
                date: str = info[2]
                cursor = "diff"
                continue
            # Next, there is a list of changed files and the changed lines
            # with the format 'Additions    Deletions   File'
            if cursor == "diff":
                changed_name: bool = False
                # Keeps track of the file if its name was changed
                changed_name, file_info = _validate_change(
                    changed_name, file_info, line
                )
                if file_info in line or changed_name:
                    git_metrics["author_email"].append(author)
                    git_metrics["commit_hash"].append(commit)
                    git_metrics["date_iso_format"].append(date)

                    stats: list[str] = line.strip("\n").split("\t")
                    git_metrics["stats"].append(
                        f"1 file changed, {stats[0]} insertions (+), "
                        f"{stats[1]} deletions (-)"
                    )
    return git_metrics


def get_repositories_log(dir_: str, repos_paths: ndarray) -> None:
    """Gets the complete log of the repositories and saves them to files"""
    for repo_path in repos_paths:
        repo: str = os.path.basename(repo_path)
        try:
            git_repo: Git = Git(repo_path)
            Git().execute(
                [
                    "git",
                    "config",
                    "--global",
                    "--add",
                    "safe.directory",
                    str(repo_path),
                ]
            )
            git_log: str = git_repo.log(
                "--no-merges", "--numstat", "--pretty=%n%H,%ae,%aI%n"
            ).replace("\n\n\n", "\n")
            with open(
                os.path.join(dir_, f"{repo}.log"),
                "w",
                encoding="utf8",
            ) as log_file:
                log_file.write(git_log)
        except GitCommandNotFound as exc:
            log_exception("warning", exc, message=f"Repo {repo} doesn't exist")


def get_repository_files(repo_path: str) -> list[str]:
    """lists all the files inside a repository relative to the repository"""
    ignore_dirs: list[str] = [".git"]
    return [
        os.path.join(path, filename).replace(
            f"{os.path.dirname(repo_path)}/", ""
        )
        for path, _, files in os.walk(repo_path)
        for filename in files
        if all(  # pylint: disable=use-a-generator
            [dir_ not in path for dir_ in ignore_dirs]
        )
    ]


def parse_git_shortstat(stat: str) -> tuple[int, int]:
    insertions: int = 0
    deletions: int = 0
    match = re.match(STAT_REGEX, stat.strip())
    if match:
        groups: dict[str, str] = match.groupdict()
        if groups["insertions"]:
            insertions = int(groups["insertions"])
        if groups["deletions"]:
            deletions = int(groups["deletions"])
    return insertions, deletions


def test_repo(repo_path: str) -> bool:
    """Checks correct configuration of a repository by running `git log`"""
    git_repo: Git = Git(repo_path)
    is_repo_ok: bool = True
    try:
        git_repo.log()
    except GitCommandError:
        is_repo_ok = False
    return is_repo_ok
