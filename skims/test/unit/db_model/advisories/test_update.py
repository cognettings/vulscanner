from ..types import (
    ADVISORY_TEST,
    PRIMARY_KEY_TEST,
    STR_MDL_UPDATE,
    TABLE,
)
from custom_exceptions import (
    _SingleMessageException,
    AdvisoryDoesNotExist,
    AdvisoryNotModified,
    InvalidSeverity,
    InvalidVulnerableVersion,
)
from db_model.advisories.update import (
    _check_update,
    _update,
    ACTION,
    update,
)
from dynamodb.types import (
    Item,
)
from importlib import (
    import_module,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from s3.model.types import (
    Advisory,
)
from unittest.mock import (
    Mock,
)


@pytest.fixture(name="mock_inner_update")
def fixture_inner_update(mocker: MockerFixture) -> Mock:
    return mocker.patch(f"{STR_MDL_UPDATE}._update")


@pytest.fixture(name="mock_builtins_print")
def fixture_builtins_print(mocker: MockerFixture) -> Mock:
    return mocker.patch("builtins.print")


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "checked",
    [
        True,
        False,
    ],
)
async def test_inner_update(
    mocker: MockerFixture,
    mock_builtins_print: Mock,
    checked: bool,
) -> None:
    mock_format_advisory = mocker.patch(
        f"{STR_MDL_UPDATE}.format_advisory", return_value=ADVISORY_TEST
    )
    mocker.patch.object(import_module(STR_MDL_UPDATE), "TABLE", TABLE)
    mock_build_key = mocker.patch(
        f"{STR_MDL_UPDATE}.keys.build_key", return_value=PRIMARY_KEY_TEST
    )
    mock_check_update = mocker.patch(
        f"{STR_MDL_UPDATE}._check_update", return_value=ADVISORY_TEST
    )
    mock_update_item = mocker.patch(f"{STR_MDL_UPDATE}.operations.update_item")
    await _update(advisory=ADVISORY_TEST, checked=checked)
    assert mock_format_advisory.call_count == 1
    assert mock_check_update.await_count == int(not checked)
    assert mock_update_item.call_args.kwargs == {
        "item": ADVISORY_TEST._asdict(),
        "key": mock_build_key.return_value,
        "table": TABLE,
    }
    assert mock_builtins_print.call_args.args == (
        f"Updated ( {PRIMARY_KEY_TEST.partition_key} "
        f"{PRIMARY_KEY_TEST.sort_key} )",
    )


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "items",
    [
        [
            {
                "vulnerable_version": "1.0.0",
                "severity": "high",
                "cwe_ids": None,
                "created_at": "2022-01-01T00:00:00Z",
            }
        ],
        [
            {
                "vulnerable_version": "2.0.0",
                "created_at": "2022-01-01T00:00:00Z",
            }
        ],
        [
            {
                "vulnerable_version": "1.0.0",
                "severity": "low",
                "created_at": "2022-01-01T00:00:00Z",
            }
        ],
    ],
)
async def test_check_update(mocker: MockerFixture, items: list[Item]) -> None:
    response = mocker.Mock(items=items)
    mock_query = mocker.patch(
        f"{STR_MDL_UPDATE}.operations.query", return_value=response
    )
    result = await _check_update(
        advisory=ADVISORY_TEST, advisory_key=PRIMARY_KEY_TEST
    )
    assert mock_query.await_count == 1
    assert result.created_at == items[0].get("created_at")


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "items, expected_error",
    [
        (
            [
                {
                    "vulnerable_version": "1.0.0",
                    "severity": "high",
                    "cwe_ids": ["CWE-123"],
                }
            ],
            AdvisoryNotModified,
        ),
        (
            [],
            AdvisoryDoesNotExist,
        ),
    ],
)
async def test_check_update_error(
    mocker: MockerFixture,
    items: list[Item],
    expected_error: _SingleMessageException,
) -> None:
    response = mocker.Mock(items=items)
    mocker.patch(f"{STR_MDL_UPDATE}.operations.query", return_value=response)
    with pytest.raises(expected_error):  # type: ignore
        await _check_update(
            advisory=ADVISORY_TEST, advisory_key=PRIMARY_KEY_TEST
        )


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "to_storage",
    [[], None],
)
async def test_update(
    mock_inner_update: Mock,
    to_storage: list[Advisory] | None,
) -> None:
    await update(advisory=ADVISORY_TEST, checked=False, to_storage=to_storage)
    assert mock_inner_update.await_count == 1
    if to_storage:
        assert to_storage[0] == ADVISORY_TEST


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "class_error",
    [
        AdvisoryDoesNotExist,
        AdvisoryNotModified,
        InvalidSeverity,
        InvalidVulnerableVersion,
    ],
)
async def test_update_error(
    mocker: MockerFixture,
    mock_inner_update: Mock,
    class_error: _SingleMessageException,
) -> None:
    mock_inner_update.side_effect = class_error
    mock_print_exc = mocker.patch(f"{STR_MDL_UPDATE}.print_exc")
    await update(advisory=ADVISORY_TEST)
    print_exc_args = mock_print_exc.call_args.args
    arg_error = print_exc_args[0]
    assert print_exc_args[1] == ACTION
    assert print_exc_args[2] == ADVISORY_TEST
    if isinstance(arg_error, InvalidSeverity):
        assert print_exc_args[3] == f" ({ADVISORY_TEST.severity})"
    elif isinstance(arg_error, InvalidVulnerableVersion):
        assert print_exc_args[3] == f" ({ADVISORY_TEST.vulnerable_version})"
