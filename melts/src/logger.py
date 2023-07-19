import logging
from src import (
    constants,
)
import sys

_FORMAT: str = "[%(levelname)s] %(message)s"
_LOGGER_FORMATTER: logging.Formatter = logging.Formatter(_FORMAT)
_LOGGER_HANDLER: logging.Handler = logging.StreamHandler(sys.stdout)

if constants.LOGGER_DEBUG:
    _LOGGER_HANDLER.setLevel(logging.DEBUG)
else:
    _LOGGER_HANDLER.setLevel(logging.INFO)

_LOGGER_HANDLER.setFormatter(_LOGGER_FORMATTER)
LOGGER: logging.Logger = logging.getLogger("melts")
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(_LOGGER_HANDLER)
