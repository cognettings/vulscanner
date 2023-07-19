from back.test.unit.src.utils import (
    get_module_at_test,
)
from custom_exceptions import (
    ErrorUploadingFileS3,
    UnavailabilityError,
)
import os
import pytest
from s3.operations import (
    remove_file,
    sign_url,
    sing_upload_url,
    upload_memory_file,
)
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
)
from unittest.mock import (
    AsyncMock,
    Mock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)


pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["file_name"],
    [["test-file-records.csv"]],
)
@patch(MODULE_AT_TEST + "get_s3_resource", new_callable=AsyncMock)
async def test_upload_memory_file(
    mock_get_s3_resource: AsyncMock,
    file_name: str,
    mocked_data_for_module: Dict[str, Dict[str, Any]],
    get_mocked_data: Any,
) -> None:
    mock_client = mock_get_s3_resource.return_value
    mock_client.upload_fileobj.side_effect = get_mocked_data(
        mocked_data=mocked_data_for_module,
        mocked_functionality_path="client.upload_fileobj",
        mock_key="test_upload_memory_file",
        module_at_test=MODULE_AT_TEST,
    )

    file_location = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(file_location, "mock/" + file_name)
    with open(file_location, "rb") as data:
        test_file = UploadFile(data)  # type: ignore
        await upload_memory_file(test_file, file_name)
    assert mock_get_s3_resource.return_value.upload_fileobj.call_count == 1

    with pytest.raises(ErrorUploadingFileS3):
        with open(file_location, "rb") as data:
            await upload_memory_file(data, file_name)
    assert mock_get_s3_resource.return_value.upload_fileobj.call_count == 1


@pytest.mark.parametrize(
    ["file_name"],
    [["unittesting-test-file.csv"]],
)
@patch(MODULE_AT_TEST + "get_s3_resource", new_callable=AsyncMock)
async def test_upload_memory_file_client_error(
    mock_get_s3_resource: AsyncMock,
    file_name: str,
    mocked_data_for_module: Dict[str, Dict[str, Any]],
    get_mocked_data: Any,
) -> None:
    mock_client = mock_get_s3_resource.return_value
    mock_client.upload_fileobj.side_effect = get_mocked_data(
        mocked_data=mocked_data_for_module,
        mocked_functionality_path="client.upload_fileobj",
        mock_key="test_upload_memory_file_client_error",
        module_at_test=MODULE_AT_TEST,
    )
    file_location = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(file_location, "mock/" + file_name)
    with pytest.raises(UnavailabilityError):
        with open(file_location, "rb") as data:
            test_file = UploadFile(data)  # type: ignore
            await upload_memory_file(test_file, file_name)


@patch(MODULE_AT_TEST + "get_s3_resource", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "LOGGER.exception")
async def test_remove_file_catches_client_error(
    mock_logger_exception: Mock,
    mock_get_s3_resource: AsyncMock,
    assert_raises_unavailability_error: Callable[
        [Mock, AsyncMock, AsyncMock, Awaitable], None
    ],
) -> None:
    mock_client = mock_get_s3_resource.return_value
    await assert_raises_unavailability_error(
        mock_logger_exception,
        mock_get_s3_resource,
        mock_client.delete_object,
        lambda: remove_file(name="non_existent_file.txt"),  # type: ignore
    )


@patch(MODULE_AT_TEST + "get_s3_resource", new_callable=AsyncMock)
async def test_remove_file_raises_unavailability_error(
    mock_get_s3_resource: AsyncMock,
    mocked_data_for_module: Dict[str, Dict[str, Any]],
    get_mocked_data: Any,
) -> None:
    mock_client = mock_get_s3_resource.return_value
    mock_client.delete_object.return_value = get_mocked_data(
        mocked_data=mocked_data_for_module,
        mocked_functionality_path="client.delete_object",
        mock_key="test_remove_file_raises_unavailability_error",
        module_at_test=MODULE_AT_TEST,
    )
    with pytest.raises(UnavailabilityError):
        await remove_file(name="non_existent_file.txt")
    mock_get_s3_resource.assert_called_once()
    mock_client.delete_object.assert_called_once()


@patch(MODULE_AT_TEST + "get_s3_resource", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "LOGGER.exception")
async def test_sign_url_raises_unavailability_error(
    mock_logger_exception: Mock,
    mock_get_s3_resource: AsyncMock,
    assert_raises_unavailability_error: Callable[
        [Mock, AsyncMock, AsyncMock, Awaitable], None
    ],
) -> None:
    mock_client = mock_get_s3_resource.return_value

    await assert_raises_unavailability_error(
        mock_logger_exception,
        mock_get_s3_resource,
        mock_client.generate_presigned_url,
        lambda: sign_url(  # type: ignore
            file_name="non_existent_file.txt", expire_mins=100
        ),
    )


@patch(MODULE_AT_TEST + "get_s3_resource", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "LOGGER.exception")
async def test_sign_upload_url_raises_unavailability_error(
    mock_logger_exception: Mock,
    mock_get_s3_resource: AsyncMock,
    assert_raises_unavailability_error: Callable[
        [Mock, AsyncMock, AsyncMock, Awaitable], None
    ],
) -> None:
    mock_client = mock_get_s3_resource.return_value
    await assert_raises_unavailability_error(
        mock_logger_exception,
        mock_get_s3_resource,
        mock_client.generate_presigned_post,
        lambda: sing_upload_url(  # type: ignore
            file_name="non_existent_file.txt", expire_mins=100
        ),
    )
