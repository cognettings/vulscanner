from botocore.exceptions import (
    ClientError,
)
from dynamodb.exceptions import (
    DynamoDbBaseException,
    handle_error,
    UnavailabilityError,
)
import pytest
from pytest_mock import (
    MockerFixture,
)


@pytest.mark.skims_test_group("unittesting")
def test_handle_error(mocker: MockerFixture) -> None:
    error_code = "DynamoDbBaseException"
    error_message = "Custom error message"
    client_error = ClientError(
        {
            "Error": {
                "Code": error_code,
                "Message": error_message,
            }
        },
        operation_name="custom_operation",
    )
    mocker.patch("dynamodb.exceptions.log_blocking")
    with pytest.raises(DynamoDbBaseException):
        handle_error(error=client_error)
    with pytest.raises(UnavailabilityError):
        handle_error(
            error=ClientError(
                {"Error": {"Code": "UnknownCode"}},
                operation_name="test_operation",
            )
        )
