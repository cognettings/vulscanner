from ..types import (
    UPD_SCA_TABLE_STR,
)
from git.exc import (
    GitError,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from schedulers.update_sca_table import (
    clone_repo,
)
from schedulers.update_sca_table.repositories.advisory_database import (
    URL_ADVISORY_DATABASE,
)


@pytest.mark.skims_test_group("unittesting")
def test_clone_repo(mocker: MockerFixture) -> None:
    mocker.patch("builtins.print")
    clone_mock = mocker.patch(f"{UPD_SCA_TABLE_STR}.Repo.clone_from")
    result_clone = clone_repo(URL_ADVISORY_DATABASE)
    assert clone_mock.call_count == 1
    assert isinstance(result_clone, str)


@pytest.mark.skims_test_group("unittesting")
def test_clone_repo_error(mocker: MockerFixture) -> None:
    mocker.patch("builtins.print")
    mocker.patch(f"{UPD_SCA_TABLE_STR}.log_blocking")
    mocked = mocker.patch(
        f"{UPD_SCA_TABLE_STR}.Repo.clone_from",
        side_effect=GitError(),
    )
    result_clone = clone_repo("invalid_repo_url/")
    assert mocked.call_count == 1
    assert result_clone is None
