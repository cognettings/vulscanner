from importlib import (
    import_module,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from s3.resource import (
    get_s3_resource,
    s3_shutdown,
    s3_start_resource,
)
from types import (
    ModuleType,
)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize("resource", [None, "resource"])
async def test_get_s3_resource(
    mocker: MockerFixture, resource: str | None
) -> None:
    s3_resource = "s3.resource"
    new_resource = "new_resource"
    module_test: ModuleType = import_module(s3_resource)
    mocker.patch.object(module_test, "RESOURCE", resource)
    s3_start_resource_mock = mocker.patch(
        f"{s3_resource}.s3_start_resource",
        side_effect=lambda: mocker.patch.object(
            module_test, "RESOURCE", new_resource
        ),
    )
    result = await get_s3_resource()
    if resource:
        assert s3_start_resource_mock.await_count == 0
        assert result == resource
    else:
        assert s3_start_resource_mock.await_count == 1
        assert result == new_resource


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize("bool_context", [True, False])
async def test_s3_shutdown(
    mocker: MockerFixture,
    bool_context: bool,
) -> None:
    mock_context_stack = mocker.patch("s3.resource.CONTEXT_STACK")
    mock_context_stack.__bool__.return_value = bool_context
    mock_context_stack.aclose = mocker.AsyncMock()
    await s3_shutdown()
    assert mock_context_stack.aclose.await_count == int(bool_context)
    assert mock_context_stack.__bool__.call_count == 1


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize("is_public", [True, False])
async def test_s3_start_resource(
    mocker: MockerFixture, is_public: bool
) -> None:
    s3_resource = "s3.resource"
    module_test: ModuleType = import_module(s3_resource)
    mocker.patch("s3.resource.CONTEXT_STACK", None)
    mocker.patch.object(module_test, "RESOURCE", None)
    public_options_mock = mocker.patch.object(
        module_test, "PUBLIC_RESOURCE_OPTIONS", {"resource": "public_options"}
    )
    resource_options_mock = mocker.patch.object(
        module_test, "RESOURCE_OPTIONS", {"resource": "resource_options"}
    )
    enter_async_context = mocker.AsyncMock()
    mocker.patch(
        "s3.resource.AsyncExitStack",
        return_value=mocker.AsyncMock(enter_async_context=enter_async_context),
    )
    session_mock = mocker.patch(
        "s3.resource.SESSION.client",
        return_value="session_return_value",
    )
    await s3_start_resource(is_public=is_public)
    assert session_mock.call_args.kwargs == (
        public_options_mock if is_public else resource_options_mock
    )
    assert enter_async_context.call_args.args[0] == session_mock.return_value
    assert session_mock.call_count == 1
    assert enter_async_context.await_count == 1
