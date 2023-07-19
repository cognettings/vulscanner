from dynamodb.resource import (
    dynamo_shutdown,
    dynamo_startup,
    get_resource,
    get_table_resource,
)
from dynamodb.types import (
    PrimaryKey,
    Table,
)
from importlib import (
    import_module,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from types import (
    ModuleType,
)

# Constants
STR_DB_RESOURCE = "dynamodb.resource"


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize("resource", [None, "resource"])
async def test_get_resource(
    mocker: MockerFixture,
    resource: str | None,
) -> None:
    new_resource = "new_resource"
    module_test: ModuleType = import_module(STR_DB_RESOURCE)
    mocker.patch.object(module_test, "RESOURCE", resource)
    mock_s3_start_resource = mocker.patch(
        f"{STR_DB_RESOURCE}.dynamo_startup",
        side_effect=lambda: mocker.patch.object(
            module_test, "RESOURCE", new_resource
        ),
    )
    result = await get_resource()
    if resource:
        assert mock_s3_start_resource.await_count == 0
        assert result == resource
    else:
        assert mock_s3_start_resource.await_count == 1
        assert result == new_resource


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize("bool_context", [True, False])
async def test_dynamo_shutdown(
    mocker: MockerFixture,
    bool_context: bool,
) -> None:
    mock_context_stack = mocker.patch(f"{STR_DB_RESOURCE}.CONTEXT_STACK")
    mock_context_stack.__bool__.return_value = bool_context
    mock_context_stack.aclose = mocker.AsyncMock()
    await dynamo_shutdown()
    assert mock_context_stack.aclose.await_count == int(bool_context)
    assert mock_context_stack.__bool__.call_count == 1


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_dynamo_startup(
    mocker: MockerFixture,
) -> None:
    module_test: ModuleType = import_module(STR_DB_RESOURCE)
    mocker.patch(f"{STR_DB_RESOURCE}.CONTEXT_STACK", None)
    mocker.patch.object(module_test, "RESOURCE", mocker.AsyncMock())
    mocker.patch.object(module_test, "TABLE_RESOURCES", {})
    mock_resource_options = mocker.patch.object(
        module_test, "RESOURCE_OPTIONS", {"resource": "resource_options"}
    )
    mock_table = mocker.AsyncMock()
    mock_session_resource = mocker.patch(
        f"{STR_DB_RESOURCE}.SESSION.resource",
        return_value=mocker.AsyncMock(
            Table=mock_table,
        ),
    )
    mock_enter_async_context = mocker.AsyncMock(
        return_value=mock_session_resource.return_value
    )
    mocker.patch(
        f"{STR_DB_RESOURCE}.AsyncExitStack",
        return_value=mocker.AsyncMock(
            enter_async_context=mock_enter_async_context
        ),
    )

    await dynamo_startup()
    assert mock_session_resource.call_args.kwargs == (mock_resource_options)
    assert mock_table.call_args.args[0] == "skims_sca"
    assert (
        mock_enter_async_context.call_args.args[0]
        == mock_session_resource.return_value
    )
    assert mock_session_resource.call_count == 1
    assert mock_enter_async_context.await_count == 1


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize("table", [{"table": "table_test"}, {}])
async def test_get_table_resource(
    mocker: MockerFixture,
    table: dict[str, str],
) -> None:
    mocker.patch(f"{STR_DB_RESOURCE}.TABLE_RESOURCES", table)
    table_class = Table(
        facets={}, indexes={}, name="table", primary_key=PrimaryKey("", "")
    )
    mock_get_resource = mocker.patch(
        f"{STR_DB_RESOURCE}.get_resource",
    )
    mock_get_resource.return_value.Table.return_value = "returned_Table"
    result = await get_table_resource(table=table_class)
    if table != {}:
        assert result == "table_test"
        assert mock_get_resource.await_count == 0
    else:
        assert (
            mock_get_resource.return_value.Table.call_args.args[0] == "table"
        )
        assert result == "returned_Table"
        assert mock_get_resource.await_count == 1
