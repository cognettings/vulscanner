import aioboto3
import configparser
from context import (
    FI_AWS_S3_CONTINUOUS_REPOSITORIES,
    FI_AWS_S3_PATH_PREFIX,
)
from db_model.roots.get import (
    get_download_url,
)
from git import (
    NoSuchPathError,
)
from git.repo import (
    Repo,
)
from git_self import (
    download_repo_from_s3,
)
import logging
import os
from os import (
    path,
)
from pathlib import (
    Path,
)
from s3.resource import (
    get_s3_resource,
)
from settings.logger import (
    LOGGING,
)
import tarfile
import tempfile

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
SESSION = aioboto3.Session()


def create_git_root_tar_file(
    root_nickname: str, repo_path: str, output_path: str | None = None
) -> bool:
    git_dir = path.normpath(f"{repo_path}/.git")
    config_path = path.join(git_dir, "config")
    if path.exists(config_path):
        clean_git_config_file(config_path)
    with tarfile.open(
        output_path or f"{root_nickname}.tar.gz", "w:gz"
    ) as tar_handler:
        if path.exists(git_dir):
            tar_handler.add(
                git_dir, arcname=f"{root_nickname}/.git", recursive=True
            )
            return True
        return False


async def upload_cloned_repo_to_s3_tar(
    *, repo_path: str, group_name: str, nickname: str
) -> bool:
    success: bool = False

    _, zip_output_path = tempfile.mkstemp()
    create_git_root_tar_file(nickname, repo_path, zip_output_path)

    if not create_git_root_tar_file(nickname, repo_path, zip_output_path):
        LOGGER.error(
            "Failed to compress root %s",
            nickname,
            extra=dict(extra=locals()),
        )
        os.remove(zip_output_path)
        return False

    s3_client = await get_s3_resource()
    await s3_client.upload_file(
        zip_output_path,
        FI_AWS_S3_CONTINUOUS_REPOSITORIES,
        f"{FI_AWS_S3_PATH_PREFIX}{group_name}/{nickname}.tar.gz",
    )
    success = True

    os.remove(zip_output_path)
    return success


async def download_repo(
    group_name: str,
    git_root_nickname: str,
    path_to_extract: str,
    gitignore: list[str] | None = None,
) -> Repo | None:
    repo_path = os.path.join(path_to_extract, git_root_nickname)
    if (
        download_url := await get_download_url(group_name, git_root_nickname)
    ) and await download_repo_from_s3(
        download_url, Path(repo_path), gitignore
    ):
        try:
            return Repo(repo_path)
        except NoSuchPathError as error:
            LOGGER.error(
                error,
                extra=dict(
                    group_name=group_name,
                    repo_nickname=git_root_nickname,
                ),
            )
    return None


def clean_git_config_file(git_config_path: str) -> bool:
    # Read the contents of the .git/config file
    config = configparser.ConfigParser()
    config.read(git_config_path)

    # Remove the URL sections
    if 'remote "origin"' in config.sections():
        config.remove_section('remote "origin"')

    # Save the modified config file
    with open(git_config_path, "w", encoding="utf-8") as config_file:
        config.write(config_file)

    return True
