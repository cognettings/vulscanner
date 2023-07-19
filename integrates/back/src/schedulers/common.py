from aioextensions import (
    schedule,
)
from collections.abc import (
    Callable,
)
from dataloaders import (
    Dataloaders,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from typing import (
    Any,
)

# FP: local testing
logging.config.dictConfig(LOGGING)  # NOSONAR
LOGGER = logging.getLogger(__name__)

# Constants
MAX_COMMENT_LENGTH = 500


def info(*args: Any, extra: Any = None) -> None:
    LOGGER.info(*args, extra=dict(extra=extra))


def error(*args: Any, extra: Any = None) -> None:
    LOGGER.error(*args, extra=dict(extra=extra))


def scheduler_send_mail(
    loaders: Dataloaders,
    send_mail_function: Callable,
    mail_to: list[str],
    mail_context: dict[str, Any],
) -> None:
    schedule(send_mail_function(loaders, mail_to, mail_context))


def format_comment(comment: str) -> str:
    if len(comment) > MAX_COMMENT_LENGTH:
        comment = f"{comment[:MAX_COMMENT_LENGTH]}..."

    return comment
