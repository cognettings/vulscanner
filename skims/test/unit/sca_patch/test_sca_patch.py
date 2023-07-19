from .types import (
    ADVISORIES_TEST_DICTS,
    ADVISORIES_TEST_OBJECTS,
    SCA_PATCH,
)
from aioextensions import (
    run,
)
from collections.abc import (
    Iterable,
)
from custom_exceptions import (
    InvalidActionParameter,
    InvalidPatchItem,
    InvalidPathParameter,
    InvalidScaPatchFormat,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from sca_patch import (
    ADD,
    get_platforms,
    main as sca_patch_main,
    patch_sca,
    REMOVE,
    UPDATE,
)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "action",
    [ADD, UPDATE, REMOVE],
)
def test_sca_patch_main(mocker: MockerFixture, action: str) -> None:
    mocker.patch(f"{SCA_PATCH}.sys", argv=["test", action, "test_sca.json"])
    dyn_start_mock = mocker.patch(f"{SCA_PATCH}.dynamo_startup")
    dyn_down_mock = mocker.patch(f"{SCA_PATCH}.dynamo_shutdown")
    patch_sca_mock = mocker.patch(f"{SCA_PATCH}.patch_sca")
    mocker.patch(f"{SCA_PATCH}.os.path.exists", return_value=True)

    run(sca_patch_main())
    assert dyn_start_mock.await_count == 1
    assert patch_sca_mock.call_args.args == ("test_sca.json", action)
    assert dyn_down_mock.await_count == 1


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "action,class_error",
    [(ADD, InvalidPathParameter), ("invalid_action", InvalidActionParameter)],
)
def test_sca_patch_main_error(
    mocker: MockerFixture,
    action: str,
    class_error: InvalidPathParameter | InvalidActionParameter,
) -> None:
    mocker.patch(
        f"{SCA_PATCH}.sys", argv=["test", action, "test_path_sca.json"]
    )
    dyn_down_mock = mocker.patch(f"{SCA_PATCH}.dynamo_shutdown")
    log_blocking_mock = mocker.patch(f"{SCA_PATCH}.log_blocking")

    run(sca_patch_main())
    assert log_blocking_mock.call_args.args == ("error", "%s", class_error.msg)
    assert dyn_down_mock.await_count == 1


@pytest.mark.skims_test_group("unittesting")
def test_get_platforms() -> None:
    result: Iterable[str] = get_platforms(ADVISORIES_TEST_OBJECTS)
    assert result == ["gem", "npm"]


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "action",
    [ADD, REMOVE, UPDATE],
)
def test_patch_sca(mocker: MockerFixture, action: str) -> None:
    mocker.patch("builtins.open")
    mocker.patch(
        f"{SCA_PATCH}.json.load", return_value=list(ADVISORIES_TEST_DICTS)
    )
    model_action_mock = mocker.patch(f"{SCA_PATCH}.advisories_model.{action}")
    check_item_mock = mocker.patch(f"{SCA_PATCH}.check_item")
    get_platforms_mock = mocker.patch(f"{SCA_PATCH}.get_platforms")
    update_s3_mock = mocker.patch(f"{SCA_PATCH}.update_s3")
    run(patch_sca("fake_filename", action))
    assert model_action_mock.await_count == len(ADVISORIES_TEST_DICTS)
    assert check_item_mock.call_count == len(ADVISORIES_TEST_DICTS)
    assert get_platforms_mock.call_count == 1
    assert update_s3_mock.await_count == 1


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "json_info,class_error",
    [({}, InvalidScaPatchFormat), (["test_item"], InvalidPatchItem)],
)
def test_patch_sca_error(
    mocker: MockerFixture,
    json_info: dict | list[dict],
    class_error: InvalidPatchItem | InvalidScaPatchFormat,
) -> None:
    mocker.patch("builtins.open")
    mocker.patch(f"{SCA_PATCH}.json.load", return_value=json_info)
    mocker.patch(f"{SCA_PATCH}.check_item", side_effect=InvalidPatchItem())
    log_blocking_mock = mocker.patch(f"{SCA_PATCH}.log_blocking")
    run(patch_sca("fake_filename", ADD))
    assert log_blocking_mock.call_args.args == ("error", "%s", class_error.msg)
