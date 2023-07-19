from back.test.unit.src.utils import (
    get_module_at_test,
)
from cli.invoker import (
    main as invoker_main,
)
import pytest
import sys
from typing import (
    Any,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)


@pytest.mark.asyncio
@patch(MODULE_AT_TEST + "importlib.import_module")
@patch(MODULE_AT_TEST + "sqs_shutdown")
@patch(MODULE_AT_TEST + "dynamo_shutdown")
@patch(MODULE_AT_TEST + "sqs_startup")
@patch(MODULE_AT_TEST + "dynamo_startup")
async def test_invoker(
    # pylint: disable=too-many-arguments
    mock_dynamo_startup: AsyncMock,
    mock_sqs_startup: AsyncMock,
    mock_dynamo_shutdown: AsyncMock,
    mock_importlib_import_module: AsyncMock,
    mock_sqs_shutdown: AsyncMock,
    mocked_data_for_module: Any,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_dynamo_startup,
            "dynamo_startup",
            [],
        ),
        (
            mock_sqs_startup,
            "sqs_startup",
            [],
        ),
        (
            mock_dynamo_shutdown,
            "dynamo_shutdown",
            [],
        ),
        (
            mock_dynamo_shutdown,
            "sqs_shutdown",
            [],
        ),
        (
            mock_importlib_import_module,
            "importlib.import_module",
            [],
        ),
        (
            mock_sqs_shutdown,
            "importlib.import_module",
            [],
        ),
    ]
    # Set up mocks' results using mocked_data_for_module fixture
    for mock_item in mocks_setup_list:
        mock, path, arguments = mock_item
        mock.return_value = mocked_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    test_args = ["dev", "schedulers.missing_environment_alert.main"]
    with patch.object(sys, "argv", test_args) as mock_sys:
        await invoker_main()

    mocks_list = [mock[0] for mock in mocks_setup_list]
    assert all(mock_object.called is True for mock_object in mocks_list)
    assert mock_sys[0] == "dev"
