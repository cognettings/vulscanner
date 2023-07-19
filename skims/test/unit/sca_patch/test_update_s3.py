from .types import (
    ADVISORIES_TEST_OBJECTS,
    SCA_PATCH,
)
from aioextensions import (
    run,
)
from custom_exceptions import (
    UnavailabilityError,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from sca_patch import (
    ADD,
    REMOVE,
    UPDATE,
    update_s3,
)


@pytest.mark.skims_test_group("unittesting")
def test_update_s3_error(mocker: MockerFixture) -> None:
    s3_start_mock = mocker.patch(f"{SCA_PATCH}.s3_start_resource")
    s3_down_mock = mocker.patch(f"{SCA_PATCH}.s3_shutdown")

    log_mock = mocker.patch(f"{SCA_PATCH}.log_blocking")
    download_advs_mock = mocker.patch(
        f"{SCA_PATCH}.download_advisories_dict",
        side_effect=UnavailabilityError(),
    )
    run(update_s3(list(ADVISORIES_TEST_OBJECTS), ADD, ("npm", "gem")))
    assert s3_start_mock.await_count == 1
    assert download_advs_mock.await_count == 1
    assert log_mock.call_count == 1
    assert s3_down_mock.await_count == 1


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "action",
    [ADD, REMOVE, UPDATE],
)
def test_update_s3(mocker: MockerFixture, action: str) -> None:
    s3_start_mock = mocker.patch(f"{SCA_PATCH}.s3_start_resource")
    s3_down_mock = mocker.patch(f"{SCA_PATCH}.s3_shutdown")
    download_advs_mock = mocker.patch(
        f"{SCA_PATCH}.download_advisories_dict", return_value=({}, {})
    )
    upload_advisories = mocker.patch(f"{SCA_PATCH}.upload_advisories")
    rmv_s3_mock = mocker.patch(f"{SCA_PATCH}.remove_from_s3")
    run(update_s3(list(ADVISORIES_TEST_OBJECTS), action, ()))
    assert s3_start_mock.await_count == 1
    assert download_advs_mock.await_count == 1
    assert s3_down_mock.await_count == 1
    if action == REMOVE:
        assert upload_advisories.await_count == 2
        assert rmv_s3_mock.call_count == len(ADVISORIES_TEST_OBJECTS)
    else:
        assert upload_advisories.await_count == 1
