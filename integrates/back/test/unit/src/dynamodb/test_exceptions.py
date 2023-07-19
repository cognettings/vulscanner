from back.test.unit.src.utils import (
    get_module_at_test,
)
from botocore.exceptions import (
    ClientError,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
    handle_error,
    UnavailabilityError,
)
import pytest
from unittest.mock import (
    MagicMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)


@pytest.mark.parametrize(
    ["client_error", "raised_error", "message"],
    [
        [
            ClientError(
                {"Error": {"Code": "ConditionalCheckFailedException"}},
                operation_name="test",
            ),
            ConditionalCheckFailedException,
            "conditional error",
        ],
        [
            ClientError(
                {"Error": {"Code": "connection"}}, operation_name="test"
            ),
            UnavailabilityError,
            "retry",
        ],
    ],
)
@patch(MODULE_AT_TEST + "LOGGER.error", new_callable=MagicMock)
def test_handle_error(
    mock_logger: MagicMock,
    client_error: ClientError,
    raised_error: type[Exception],
    message: str,
) -> None:
    with pytest.raises(raised_error):
        handle_error(
            error=client_error,
            message=message,
            argument="this is a test argument",
        )

    mock_logger.assert_called_with(
        message,
        extra=dict(
            extra={
                "message": message,
                "argument": "this is a test argument",
                "exception": client_error,
            }
        ),
    )
