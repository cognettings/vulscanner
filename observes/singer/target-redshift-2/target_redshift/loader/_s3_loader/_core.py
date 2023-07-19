from collections.abc import (
    Callable,
)
from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from fa_purity import (
    Cmd,
)
from typing import (
    Generic,
    TypeVar,
)

_T = TypeVar("_T")


class UploadState(Enum):
    PENDING = "PENDING"
    STARTED = "STARTED"
    COMPLETED = "COMPLETED"


@dataclass(frozen=True)
class UploadStateClient(Generic[_T]):
    get: Callable[[_T], Cmd[UploadState]]
    save: Callable[[_T, UploadState], Cmd[None]]
