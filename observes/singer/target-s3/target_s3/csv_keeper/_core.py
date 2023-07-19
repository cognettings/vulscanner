from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    PureIter,
)
from target_s3.core import (
    RecordGroup,
    TempReadOnlyFile,
)
from typing import (
    Callable,
    Generic,
    TypeVar,
)

_T = TypeVar("_T", TempReadOnlyFile, PureIter[TempReadOnlyFile])


@dataclass(frozen=True)
class CsvKeeper(Generic[_T]):
    save: Callable[[RecordGroup], Cmd[_T]]
