from enum import (
    IntEnum,
)


class StatusCode(IntEnum):
    SUCCESS = 0
    ERROR = 1
    BREAK_BUILD = 66
