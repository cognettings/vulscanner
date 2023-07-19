from botocore.exceptions import (
    ClientError,
)
from custom_exceptions import (
    UnavailabilityError,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
    Callable,
    Dict,
)
from unittest.mock import (
    AsyncMock,
    Mock,
)

BUCKET_NAME = "test_bucket"


MOCKED_DATA: Dict[str, Dict[str, Any]] = {
    "s3.operations.client.upload_fileobj": {
        "test_upload_memory_file": None,
        "test_upload_memory_file_client_error": [
            ClientError(
                {
                    "Error": {
                        "Code": "SomeServiceException",
                        "Message": "Details/context around the exception or error",  # noqa: E501 pylint: disable=line-too-long
                    },
                    "ResponseMetadata": {
                        "RequestId": "1234567890ABCDEF",
                        "HostId": "host ID data will appear here as a hash",
                        "HTTPStatusCode": 400,
                        "HTTPHeaders": {
                            "header metadata key/values will appear here"
                        },
                        "RetryAttempts": 0,
                    },
                },
                "upload_fileobj",
            )
        ],
    },
    "s3.operations.client.delete_object": {
        "test_remove_file_raises_unavailability_error": {
            "ResponseMetadata": {"HTTPStatusCode": 403}
        },
    },
}


@pytest.fixture(scope="session")
def mocked_data_for_module() -> Dict[str, Dict[str, Any]]:
    return MOCKED_DATA


@pytest_asyncio.fixture(scope="session")
async def assert_raises_unavailability_error() -> Any:
    async def common_test_setup(
        mock_logger_exception: Mock,
        mock_get_s3_resource: AsyncMock,
        client_method: AsyncMock,
        function_to_test: Callable[..., Any],
    ) -> None:
        mock_logger_exception.side_effect = None
        client_method.side_effect = ClientError({}, "testing")
        with pytest.raises(UnavailabilityError):
            await function_to_test()
        client_method.assert_called_once()
        mock_logger_exception.assert_called_once()
        mock_get_s3_resource.assert_called_once()

    return common_test_setup
