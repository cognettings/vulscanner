from collections.abc import (
    Iterator,
)
from git.cmd import (
    Git,
)
from git.repo import (
    Repo,
)
import os
import pytest
import tempfile


@pytest.fixture(autouse=True, scope="session")
def test_clone_repo() -> Iterator[str]:
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo_path: str = os.path.join(tmp_dir, "requests")
        repo_url: str = "https://github.com/psf/requests.git"
        repo_version: str = "v2.24.0"
        Repo.clone_from(repo_url, repo_path)
        git_repo: Git = Git(repo_path)
        git_repo.checkout(repo_version)
        yield tmp_dir


@pytest.fixture(autouse=True, name="test_token_fluidattacks", scope="session")
def fixture_test_token_fluidattacks() -> Iterator[str]:
    yield os.environ["SORTS_TOKEN_FLUIDATTACKS"]
