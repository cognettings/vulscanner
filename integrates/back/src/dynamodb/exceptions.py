# pylint: disable=super-with-arguments
from botocore.exceptions import (
    ClientError,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
import sys
from typing import (
    Any,
)

# Constants
logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


class DynamoDbBaseException(Exception):
    pass


class ConditionalCheckFailedException(DynamoDbBaseException):
    pass


class UnavailabilityError(DynamoDbBaseException):
    def __init__(self) -> None:
        msg = "Service unavailable, please retry"
        super(UnavailabilityError, self).__init__(msg)


class ValidationException(DynamoDbBaseException):
    pass


def handle_error(*, error: ClientError, **kwargs: Any) -> None:
    code: str = error.response["Error"]["Code"]
    custom_exception: Exception | None = getattr(
        sys.modules[__name__], code, None
    )

    # sending message as argument will allow bugsnag group related errors
    # (see settings.logger)
    if kwargs.get("message"):
        LOGGER.error(
            kwargs["message"], extra=dict(extra={**kwargs, "exception": error})
        )
    else:
        LOGGER.exception(error, extra=dict(extra=kwargs))

    if custom_exception:
        raise custom_exception from error

    raise UnavailabilityError()
