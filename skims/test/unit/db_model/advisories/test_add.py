from ..types import (
    ADVISORY_TEST,
    PRIMARY_KEY_TEST,
    STR_MDL_ADD,
    TABLE,
)
from custom_exceptions import (
    _SingleMessageException,
    AdvisoryAlreadyCreated,
    InvalidSeverity,
    InvalidVulnerableVersion,
)
from db_model.advisories.add import (
    _add,
    add,
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


@pytest.fixture(name="mock_inner_add")
def fixture_inner_add(mocker: MockerFixture) -> Mock:
    return mocker.patch(f"{STR_MDL_ADD}._add")


@pytest.fixture(name="mock_builtins_print")
def fixture_builtins_print(mocker: MockerFixture) -> Mock:
    return mocker.patch("builtins.print")


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "to_storage",
    [[], None],
)
async def test_add(
    mock_inner_add: Mock,
    to_storage: list[Advisory] | None,
) -> None:
    await add(
        advisory=ADVISORY_TEST, no_overwrite=False, to_storage=to_storage
    )
    assert mock_inner_add.await_count == 1
    assert mock_inner_add.call_args.kwargs == {
        "advisory": ADVISORY_TEST,
        "no_overwrite": False,
    }
    if to_storage:
        assert to_storage[0] == ADVISORY_TEST


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "class_error",
    [
        AdvisoryAlreadyCreated,
        InvalidSeverity,
        InvalidVulnerableVersion,
    ],
)
async def test_add_error(
    mocker: MockerFixture,
    mock_inner_add: Mock,
    class_error: _SingleMessageException,
) -> None:
    mock_inner_add.side_effect = class_error
    mock_print_exc = mocker.patch(f"{STR_MDL_ADD}.print_exc")
    await add(advisory=ADVISORY_TEST)
    print_exc_args = mock_print_exc.call_args.args
    arg_error = print_exc_args[0]
    assert print_exc_args[1] == "added"
    assert print_exc_args[2] == ADVISORY_TEST
    if isinstance(arg_error, InvalidSeverity):
        assert print_exc_args[3] == f" ({ADVISORY_TEST.severity})"
    elif isinstance(arg_error, InvalidVulnerableVersion):
        assert print_exc_args[3] == f" ({ADVISORY_TEST.vulnerable_version})"


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_items",
    [
        [],
        [
            {
                "associated_advisory": "ADV-123",
                "package_name": "test_package",
                "package_manager": "test_manager",
                "vulnerable_version": "3.0.0",
                "source": "test_source",
                "cwe_ids": ["CWE-123"],
                "severity": "high",
                "created_at": "created_date",
            }
        ],
    ],
)
async def test_inner_add(
    mocker: MockerFixture,
    mock_builtins_print: Mock,
    response_items: list[Advisory],
) -> None:
    mock_format_advisory = mocker.patch(
        f"{STR_MDL_ADD}.format_advisory", return_value=ADVISORY_TEST
    )
    mocker.patch.object(import_module(STR_MDL_ADD), "TABLE", TABLE)
    key_structure = TABLE.primary_key
    mock_build_key = mocker.patch(
        f"{STR_MDL_ADD}.keys.build_key", return_value=PRIMARY_KEY_TEST
    )
    mock_query = mocker.patch(
        f"{STR_MDL_ADD}.operations.query",
        return_value=mocker.Mock(items=response_items),
    )
    mock_update = mocker.patch(f"{STR_MDL_ADD}.update")
    items = {
        key_structure.partition_key: PRIMARY_KEY_TEST.partition_key,
        key_structure.sort_key: PRIMARY_KEY_TEST.sort_key,
        **ADVISORY_TEST._asdict(),
    }
    mock_batch_put_item = mocker.patch(
        f"{STR_MDL_ADD}.operations.batch_put_item"
    )
    await _add(advisory=ADVISORY_TEST, no_overwrite=False)
    assert mock_format_advisory.call_count == 1
    assert mock_query.await_count == 1
    assert mock_build_key.call_count == 1
    if response_items:
        assert mock_update.call_args.kwargs == {
            "advisory": ADVISORY_TEST._replace(created_at="created_date"),
            "checked": True,
        }
    else:
        assert mock_batch_put_item.call_args.kwargs == {
            "items": (items,),
            "table": TABLE,
        }
        assert mock_builtins_print.call_args.args == (
            f"Added ( {PRIMARY_KEY_TEST.partition_key} "
            f"{PRIMARY_KEY_TEST.sort_key} )",
        )


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_inner_add_error(
    mocker: MockerFixture,
) -> None:
    mocker.patch(f"{STR_MDL_ADD}.format_advisory", return_value=ADVISORY_TEST)
    mocker.patch.object(import_module(STR_MDL_ADD), "TABLE", TABLE)
    mocker.patch(
        f"{STR_MDL_ADD}.keys.build_key", return_value=PRIMARY_KEY_TEST
    )
    mocker.patch(
        f"{STR_MDL_ADD}.operations.query",
        return_value=mocker.Mock(items=[ADVISORY_TEST._asdict()]),
    )
    with pytest.raises(AdvisoryAlreadyCreated):
        await _add(advisory=ADVISORY_TEST, no_overwrite=True)
