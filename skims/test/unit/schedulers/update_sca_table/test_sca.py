from ..types import (
    UPD_SCA_TABLE_STR,
)
from aioextensions import (
    run,
)
from importlib import (
    import_module,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from schedulers.update_sca_table import (
    main as sca_table_main,
    update_sca,
)
from types import (
    ModuleType,
)


@pytest.mark.skims_test_group("unittesting")
def test_sca_table_main(mocker: MockerFixture) -> None:
    mocked = mocker.patch(f"{UPD_SCA_TABLE_STR}.update_sca")
    run(sca_table_main())
    assert mocked.await_count == 1


@pytest.mark.skims_test_group("unittesting")
def test_update_sca(mocker: MockerFixture) -> None:
    mocker.patch(f"{UPD_SCA_TABLE_STR}.s3_shutdown")
    mocker.patch(f"{UPD_SCA_TABLE_STR}.s3_start_resource")
    mocker.patch(f"{UPD_SCA_TABLE_STR}.fix_advisory")
    log_mock = mocker.patch(f"{UPD_SCA_TABLE_STR}.log_blocking")
    module_test: ModuleType = import_module(UPD_SCA_TABLE_STR)
    get_repo_mock = mocker.Mock(
        side_effect=lambda advs, pat: advs.append("test_advisory")
    )
    repos_mock = mocker.patch.object(
        module_test, "REPOSITORIES", [(get_repo_mock, "test")]
    )
    clone_repo_mock = mocker.patch(
        f"{UPD_SCA_TABLE_STR}.clone_repo", return_value="test_dir/"
    )
    model_add_mock = mocker.patch(f"{UPD_SCA_TABLE_STR}.advisories_model.add")
    upload_advs_mock = mocker.patch(f"{UPD_SCA_TABLE_STR}.upload_advisories")
    run(update_sca())
    advisories_list = get_repo_mock.call_args.args[0]
    assert clone_repo_mock.call_count == len(repos_mock)
    assert get_repo_mock.call_count == len(repos_mock)
    assert model_add_mock.call_count == len(advisories_list)
    assert upload_advs_mock.call_count == 1
    assert log_mock.call_count == 4
