from os.path import (
    join,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from utils.repositories import (
    DEFAULT_COMMIT,
    get_repo_head_hash,
)


@pytest.mark.skims_test_group("unittesting")
def test_get_repo_head_hash(mocker: MockerFixture) -> None:
    base = "../universe"
    head = get_repo_head_hash(base)
    assert head != DEFAULT_COMMIT
    mocker.patch("utils.repositories.log_blocking")

    for path, commit_hash in (
        # Not a repository
        ("/", DEFAULT_COMMIT),
        # Not exist
        ("/path-not-exists", DEFAULT_COMMIT),
        # Inside a repository, file
        ("skims/test/data/config/lib_http.yaml", head),
        # Inside a repository, directory
        ("skims/test/data/lib_path", head),
        # Inside a repsitory, not exists
        ("skims/test/path-not-exists", DEFAULT_COMMIT),
    ):
        assert get_repo_head_hash(join(base, path)) == commit_hash, path
