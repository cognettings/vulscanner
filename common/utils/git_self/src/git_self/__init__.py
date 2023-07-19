# pylint: disable=import-outside-toplevel,import-error
import asyncio
import base64
from contextlib import (
    suppress,
)
from datetime import (
    datetime,
    timezone,
)
from git import (
    GitError,
)
from git.cmd import (
    Git,
)
from git.exc import (
    GitCommandError,
)
from git.repo import (
    Repo,
)
import logging
import os
from pathlib import (
    Path,
)
import shutil
import tarfile
import tempfile
from typing import (
    Iterable,
    Iterator,
    NamedTuple,
)
from urllib.parse import (
    ParseResult,
    quote,
    quote_plus,
    urlparse,
)
import uuid

# Constants
LOGGER = logging.getLogger(__name__)


class CommitInfo(NamedTuple):
    hash: str
    author: str
    modified_date: datetime


class RebaseResult(NamedTuple):
    path: str
    line: int
    rev: str


class InvalidParameter(Exception):
    """Exception to control empty required parameters"""

    def __init__(self, field: str = "") -> None:
        """Constructor"""
        if field:
            msg = f"Exception - Field {field} is invalid"
        else:
            msg = "Exception - Error value is not valid"
        super().__init__(msg)


def _get_as_utc_iso_format(date: datetime) -> str:
    return date.astimezone(tz=timezone.utc).isoformat()


async def disable_quotepath(git_path: str) -> None:
    await asyncio.create_subprocess_exec(
        "git",
        f"--git-dir={git_path}",
        "config",
        "core.quotepath",
        "off",
    )


async def get_last_commit_author(repo: Repo, filename: str) -> str:
    """Get the last commiter's email of a file"""
    return str(
        repo.git.log("--max-count", "1", "--format=%ce", "--", filename)
    )


async def get_last_commit_info(repo: Repo, filename: str) -> CommitInfo:
    """Get last hash of a file in the repo"""
    git_log = str(
        repo.git.log(
            "--max-count",
            "1",
            "--format=%H%n%ce%n%cI",
            "--",
            filename,
        )
    ).splitlines()
    return CommitInfo(
        hash=git_log[0],
        author=git_log[1],
        modified_date=datetime.fromisoformat(git_log[2]),
    )


async def get_last_commit_hash(repo: Repo, filename: str) -> str:
    """Get last hash of a file in the repo"""
    return str(repo.git.log("--max-count", "1", "--format=%H", "--", filename))


async def get_last_modified_date(repo: Repo, filename: str) -> str:
    """Get last modified date of a file in the repo"""
    return _get_as_utc_iso_format(
        datetime.fromisoformat(
            repo.git.log(
                "--max-count",
                "1",
                "--format=%cI",
                "--",
                filename,
            )
        )
    )


async def ssh_ls_remote(
    repo_url: str,
    credential_key: str,
    branch: str = "HEAD",
) -> str | None:
    raw_root_url = repo_url
    if not (
        "source.developers.google" in raw_root_url or "FLUID" in raw_root_url
    ):
        parsed_url = urlparse(repo_url)
        raw_root_url = repo_url.replace(f"{parsed_url.scheme}://", "")

    with tempfile.TemporaryDirectory() as temp_dir:
        ssh_file_name: str = os.path.join(temp_dir, str(uuid.uuid4()))
        with open(
            os.open(ssh_file_name, os.O_CREAT | os.O_WRONLY, 0o400),
            "w",
            encoding="utf-8",
        ) as ssh_file:
            ssh_file.write(base64.b64decode(credential_key).decode())

        proc = await asyncio.create_subprocess_exec(
            "git",
            "ls-remote",
            raw_root_url,
            branch,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            env={
                **os.environ.copy(),
                "GIT_SSH_COMMAND": (
                    f"ssh -i {ssh_file_name}"
                    " -o UserKnownHostsFile=/dev/null"
                    " -o StrictHostKeyChecking=no"
                    " -o IdentitiesOnly=yes"
                    " -o HostkeyAlgorithms=+ssh-rsa"
                    " -o PubkeyAcceptedAlgorithms=+ssh-rsa"
                ),
            },
        )
        stdout, stderr = await proc.communicate()

        if stderr and proc.returncode != 0:
            LOGGER.error(
                "failed git ls-remote",
                extra=dict(
                    extra={
                        "error": stderr.decode(),
                        "repo_url": repo_url,
                    }
                ),
            )

        os.remove(ssh_file_name)

        if proc.returncode != 0:
            return None

        return stdout.decode().split("\t")[0]


def _format_token(
    parsed_url: ParseResult,
    token: str,
    host: str,
    provider: str | None,
) -> str:
    url = (parsed_url._replace(netloc=f"{token}@{host}")).geturl()
    if provider:
        url = (parsed_url._replace(netloc=f"oauth2:{token}@{host}")).geturl()
        if provider == "BITBUCKET":
            url = (
                parsed_url._replace(netloc=f"x-token-auth:{token}@{host}")
            ).geturl()

    return url


def _format_https_url(
    *,
    repo_url: str,
    user: str | None = None,
    password: str | None = None,
    token: str | None = None,
    provider: str | None = None,
) -> str:
    user = quote_plus(user) if user is not None else user
    password = quote_plus(password) if password is not None else password

    parsed_url = urlparse(repo_url)
    parsed_url = parsed_url._replace(path=quote(parsed_url.path))
    host = parsed_url.netloc
    if "@" in host:
        host = host.split("@")[-1]

    if token is not None:
        url = _format_token(parsed_url, token, host, provider)
    elif user is not None and password is not None:
        url = (
            parsed_url._replace(netloc=f"{user}:{password}@{host}")
        ).geturl()
    else:
        # The https public repositories can be cloned without credentials
        url = parsed_url.geturl()

    return url


async def https_ls_remote(  # pylint: disable=too-many-arguments
    repo_url: str,
    user: str | None = None,
    password: str | None = None,
    token: str | None = None,
    branch: str = "HEAD",
    is_oauth: bool = False,  # pylint: disable=unused-argument # NOSONAR
    provider: str | None = None,
) -> str | None:
    url = _format_https_url(
        repo_url=repo_url,
        user=user,
        password=password,
        token=token,
        provider=provider,
    )

    proc = await asyncio.create_subprocess_exec(
        "git",
        "-c",
        "http.sslVerify=false",
        "-c",
        "http.followRedirects=true",
        "ls-remote",
        url,
        branch,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL,
    )
    try:
        stdout, _stderr = await asyncio.wait_for(proc.communicate(), 20)
        if _stderr and proc.returncode != 0:
            LOGGER.error(
                "failed git ls-remote",
                extra=dict(
                    extra={
                        "error": _stderr.decode(),
                        "repo_url": repo_url,
                    }
                ),
            )
    except asyncio.exceptions.TimeoutError:
        LOGGER.warning(
            "git remote-ls time out",
            extra={"extra": {"repo_url": repo_url}},
        )
        return None

    if proc.returncode != 0:
        return None

    return stdout.decode().split("\t")[0]


async def ssh_clone(
    *, branch: str, credential_key: str, repo_url: str, temp_dir: str
) -> tuple[str | None, str | None]:
    raw_root_url = repo_url
    if not (
        "source.developers.google" in raw_root_url or "FLUID" in raw_root_url
    ):
        raw_root_url = repo_url.replace(f"{urlparse(repo_url).scheme}://", "")
    ssh_file_name: str = os.path.join(temp_dir, str(uuid.uuid4()))
    with open(
        os.open(ssh_file_name, os.O_CREAT | os.O_WRONLY, 0o400),
        "w",
        encoding="utf-8",
    ) as ssh_file:
        ssh_file.write(base64.b64decode(credential_key).decode())

    folder_to_clone_root = f"{temp_dir}/{uuid.uuid4()}"
    proc = await asyncio.create_subprocess_exec(
        "git",
        "clone",
        "--branch",
        branch,
        "--single-branch",
        raw_root_url,
        folder_to_clone_root,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        env={
            **os.environ.copy(),
            "GIT_SSH_COMMAND": (
                f"ssh -i {ssh_file_name}"
                " -o UserKnownHostsFile=/dev/null"
                " -o StrictHostKeyChecking=no"
                " -o IdentitiesOnly=yes"
                " -o HostkeyAlgorithms=+ssh-rsa"
                " -o PubkeyAcceptedAlgorithms=+ssh-rsa"
            ),
        },
        cwd=temp_dir,
    )
    _, stderr = await proc.communicate()

    os.remove(ssh_file_name)

    if proc.returncode == 0:
        return (folder_to_clone_root, None)

    LOGGER.error(
        "Repo cloning failed", extra={"extra": {"message": stderr.decode()}}
    )

    return (None, stderr.decode("utf-8"))


async def https_clone(
    *,
    branch: str,
    repo_url: str,
    temp_dir: str,
    password: str | None = None,
    token: str | None = None,
    user: str | None = None,
    is_oauth: bool = False,  # pylint: disable=unused-argument # NOSONAR
    provider: str | None = None,
) -> tuple[str | None, str | None]:
    url = _format_https_url(
        repo_url=repo_url,
        user=user,
        password=password,
        token=token,
        provider=provider,
    )
    folder_to_clone_root = f"{temp_dir}/{uuid.uuid4()}"
    proc = await asyncio.create_subprocess_exec(
        "git",
        "-c",
        "http.sslVerify=false",
        "-c",
        "http.followRedirects=true",
        "clone",
        "--branch",
        branch,
        "--single-branch",
        url,
        folder_to_clone_root,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        cwd=temp_dir,
    )
    _, stderr = await proc.communicate()

    if proc.returncode == 0:
        return (folder_to_clone_root, None)

    LOGGER.error(
        "Repo cloning failed", extra={"extra": {"message": stderr.decode()}}
    )

    return (None, stderr.decode("utf-8"))


def rebase(
    repo: Repo,
    *,
    path: str,
    line: int,
    rev_a: str,
    rev_b: str,
) -> RebaseResult | None:
    try:
        result: list[str] = repo.git.blame(
            f"{rev_a}..{rev_b}",
            "--",
            path,
            L=f"{line},+1",
            l=True,
            p=True,
            show_number=True,
            reverse=True,
            show_name=True,
        ).splitlines()
    except GitCommandError:
        return None

    new_rev = result[0].split(" ")[0]
    new_line = int(result[0].split(" ")[1])
    new_path = next(
        (
            row.split(" ", maxsplit=1)[1]
            for row in result
            if row.startswith("filename ")
        ),
        path,
    )
    new_path = (
        new_path.encode("latin-1")
        .decode("unicode-escape")
        .encode("latin-1")
        .decode("utf-8")
    ).strip('"')

    if new_rev == rev_a or (new_line == line and new_path == path):
        # We did not rebase anything
        return None

    return RebaseResult(path=new_path, line=new_line, rev=new_rev)


def make_group_dir(tmpdir: str, group_name: str) -> None:
    group_dir = os.path.join(tmpdir, "groups", group_name, "fusion")
    os.makedirs(group_dir, exist_ok=True)


def pull_repositories(
    tmpdir: str, group_name: str, optional_repo_nickname: str | None
) -> None:
    make_group_dir(tmpdir, group_name)
    call_melts = [
        "CI=true",
        "CI_COMMIT_REF_NAME=trunk",
        f"melts --init pull-repos --group {group_name}",
    ]
    if optional_repo_nickname:
        call_melts.append(f"--root {optional_repo_nickname}")
    os.system(" ".join(call_melts))  # nosec
    os.system(f"chmod -R +r {os.path.join(tmpdir, 'groups')}")  # nosec


def reset_repo(repo_path: str) -> bool:
    try:
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
    except GitError as exc:
        LOGGER.error("Failed to add safe directory:")
        LOGGER.error("Repository: %s", repo_path)
        LOGGER.error(exc)
        LOGGER.error("\n")

    try:
        repo = Repo(repo_path)
        repo.git.reset("--hard", "HEAD")
    except GitError as exc:
        LOGGER.error("Expand repositories has failed:")
        LOGGER.error("Repository: %s", repo_path)
        LOGGER.error(exc)
        LOGGER.error("\n")
        return False

    if repo.working_dir:
        remove_symlinks_in_directory(str(repo.working_dir))
    return True


def get_head_commit(path_to_repo: Path, branch: str) -> str | None:
    try:
        return (
            Repo(path_to_repo.resolve(), search_parent_directories=True)
            .heads[branch]
            .object.hexsha
        )
    except GitError:
        return None


async def ls_remote(
    repo_url: str,
    repo_branch: str,
    *,
    credential_key: str | None = None,
    user: str | None = None,
    password: str | None = None,
    token: str | None = None,
    provider: str | None = None,
) -> str | None:
    last_commit: str | None = None
    if credential_key is not None:
        last_commit = await ssh_ls_remote(
            repo_url=repo_url,
            credential_key=credential_key,
            branch=repo_branch,
        )
    elif user is not None and password is not None:
        last_commit = await https_ls_remote(
            repo_url=repo_url,
            user=user,
            password=password,
            branch=repo_branch,
        )
    elif token is not None:
        last_commit = await https_ls_remote(
            repo_url=repo_url,
            token=token,
            branch=repo_branch,
            provider=provider or "",
        )
    elif repo_url.startswith("http"):
        last_commit = await https_ls_remote(
            repo_url=repo_url,
            branch=repo_branch,
        )
    else:
        raise InvalidParameter()

    return last_commit


async def clone(
    repo_url: str,
    repo_branch: str,
    *,
    temp_dir: str,
    credential_key: str | None = None,
    user: str | None = None,
    password: str | None = None,
    token: str | None = None,
    provider: str | None = None,
) -> tuple[str | None, str | None]:
    stderr: str | None = None
    folder_to_clone_root: str | None = None

    if credential_key:
        folder_to_clone_root, stderr = await ssh_clone(
            branch=repo_branch,
            credential_key=credential_key,
            repo_url=repo_url,
            temp_dir=temp_dir,
        )
    elif user is not None and password is not None:
        folder_to_clone_root, stderr = await https_clone(
            branch=repo_branch,
            password=password,
            repo_url=repo_url,
            temp_dir=temp_dir,
            token=None,
            user=user,
        )
    elif token is not None:
        folder_to_clone_root, stderr = await https_clone(
            branch=repo_branch,
            password=None,
            repo_url=repo_url,
            temp_dir=temp_dir,
            token=token,
            user=None,
            provider=provider,
        )
    elif repo_url.startswith("http"):
        # it can be a public repository
        folder_to_clone_root, stderr = await https_clone(
            branch=repo_branch,
            repo_url=repo_url,
            temp_dir=temp_dir,
        )
    else:
        raise InvalidParameter()

    return folder_to_clone_root, stderr


async def _download_file(url: str, destination_path: str) -> bool:
    import aiofiles  # type: ignore
    import aiohttp

    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=3600)
    ) as session:
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(destination_path, "wb") as file:
                    while True:
                        try:
                            chunk = await response.content.read(1024)
                        except asyncio.TimeoutError:
                            LOGGER.warning("Read timeout")
                            return False
                        if not chunk:
                            break
                        await file.write(chunk)
                return os.path.exists(destination_path)

    return False


def remove_symlinks_in_directory(directory: str) -> None:
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.islink(file_path):
                os.unlink(file_path)


def _iter_full_paths(path: str) -> Iterator[str]:
    """Recursively yield full paths to files for a given starting path."""
    if os.path.isfile(path):
        yield path
    elif os.path.exists(path):
        for entry in os.scandir(path):
            full_path = entry.path
            if entry.is_dir(follow_symlinks=False):
                yield f"{entry.path}/"
                yield from _iter_full_paths(full_path)
            else:
                yield full_path


def _iter_rel_paths(starting_path: str) -> Iterator[str]:
    """Recursively yield relative paths to files for a given starting path."""
    yield from (
        path.replace(starting_path, "")[1:]
        for path in _iter_full_paths(starting_path)
    )


def _match_files(patterns: list[str], files: Iterable[str]) -> Iterator[str]:
    from pathspec import (  # pylint: disable=import-error
        PathSpec,
    )

    pattern = PathSpec.from_lines("gitwildmatch", patterns)
    yield from pattern.match_files(files)


def _delete_out_of_scope_files(git_ignore: list[str], repo_path: str) -> None:
    # Compute what files should be deleted according to the scope rules
    for file_path in _match_files(git_ignore, _iter_rel_paths(repo_path)):
        if file_path.startswith(".git/"):
            continue
        path_to_delete = os.path.join(repo_path, file_path)
        if os.path.isfile(path_to_delete):
            with suppress(FileNotFoundError):
                os.unlink(path_to_delete)

    # remove empty directories
    for root, dirs, _ in os.walk(repo_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


async def download_repo_from_s3(
    download_url: str,
    destination_path: Path,
    git_ignore: list[str] | None = None,
) -> bool:
    os.makedirs(destination_path.parent, exist_ok=True)
    file_path = destination_path.with_suffix(".tar.gz")

    result = await _download_file(download_url, str(file_path.absolute()))
    if not result:
        LOGGER.error("Failed to download repository from %s", download_url)
        return False

    try:
        shutil.rmtree(destination_path, ignore_errors=True)
        with tarfile.open(file_path, "r:gz") as tar_handler:
            tar_handler.extractall(file_path.parent, numeric_owner=True)
    except PermissionError:
        LOGGER.error("Failed to extract repository from %s", file_path)
        return False

    os.remove(file_path)
    if not reset_repo(str(destination_path.absolute())):
        shutil.rmtree(destination_path, ignore_errors=True)
        return False

    _delete_out_of_scope_files(
        git_ignore or [], str(destination_path.absolute())
    )

    return True
