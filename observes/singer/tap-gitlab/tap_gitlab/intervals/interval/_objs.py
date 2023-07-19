from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from fa_purity import (
    Result,
    ResultE,
)
from typing import (
    Callable,
    Generic,
    TypeVar,
    Union,
)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class MIN:
    def __str__(self) -> str:
        return "MIN"


@dataclass(frozen=True)
class MAX:
    def __str__(self) -> str:
        return "MAX"


class InvalidInterval(Exception):
    pass


_P = TypeVar("_P")
IntervalPoint = Union[_P, MIN, MAX]
Comparison = Callable[[_P, _P], bool]


def greater_ipoint(
    greater: Comparison[_P], _x: IntervalPoint[_P], _y: IntervalPoint[_P]
) -> bool:
    if _x == _y:
        return False
    if isinstance(_x, MIN) or isinstance(_y, MAX):
        return False
    if isinstance(_x, MAX) or isinstance(_y, MIN):
        return True
    return greater(_x, _y)


@dataclass(frozen=True)
class ClosedInterval(Generic[_P]):
    _private: _Private = field(repr=False, hash=False, compare=False)
    greater: Comparison[_P]
    lower: _P
    upper: _P

    @staticmethod
    def new(
        greater_than: Comparison[_P],
        lower: _P,
        upper: _P,
    ) -> ResultE[ClosedInterval[_P]]:
        if not greater_than(upper, lower):
            err = InvalidInterval(f"{upper} <= {lower}")
            return Result.failure(Exception(err))
        obj = ClosedInterval(_Private(), greater_than, lower, upper)
        return Result.success(obj)

    def __contains__(self, point: IntervalPoint[_P]) -> bool:
        return (
            greater_ipoint(self.greater, point, self.lower)
            or point == self.lower
        ) and (
            greater_ipoint(self.greater, self.upper, point)
            or point == self.upper
        )


@dataclass(frozen=True)
class OpenInterval(Generic[_P]):
    _private: _Private = field(repr=False, hash=False, compare=False)
    greater: Comparison[_P]
    lower: Union[_P, MIN]
    upper: Union[_P, MAX]

    @staticmethod
    def new(
        greater_than: Comparison[_P],
        lower: Union[_P, MIN],
        upper: Union[_P, MAX],
    ) -> ResultE[OpenInterval[_P]]:
        if not greater_ipoint(greater_than, upper, lower):
            err = InvalidInterval(f"{upper} <= {lower}")
            return Result.failure(Exception(err))
        obj = OpenInterval(_Private(), greater_than, lower, upper)
        return Result.success(obj)

    def __contains__(self, point: IntervalPoint[_P]) -> bool:
        return greater_ipoint(
            self.greater, point, self.lower
        ) and greater_ipoint(self.greater, self.upper, point)


@dataclass(frozen=True)
class OpenLeftInterval(Generic[_P]):
    _private: _Private = field(repr=False, hash=False, compare=False)
    greater: Comparison[_P]
    lower: Union[_P, MIN]
    upper: _P

    @staticmethod
    def new(
        greater_than: Comparison[_P],
        lower: Union[_P, MIN],
        upper: _P,
    ) -> ResultE[OpenLeftInterval[_P]]:
        if not greater_ipoint(greater_than, upper, lower):
            err = InvalidInterval(f"{upper} <= {lower}")
            return Result.failure(Exception(err))
        obj = OpenLeftInterval(_Private(), greater_than, lower, upper)
        return Result.success(obj)

    def __contains__(self, point: IntervalPoint[_P]) -> bool:
        return greater_ipoint(self.greater, point, self.lower) and (
            greater_ipoint(self.greater, self.upper, point)
            or point == self.upper
        )


@dataclass(frozen=True)
class OpenRightInterval(Generic[_P]):
    _private: _Private = field(repr=False, hash=False, compare=False)
    greater: Comparison[_P]
    lower: _P
    upper: Union[_P, MAX]

    @staticmethod
    def new(
        greater_than: Comparison[_P],
        lower: _P,
        upper: Union[_P, MAX],
    ) -> ResultE[OpenRightInterval[_P]]:
        if not greater_ipoint(greater_than, upper, lower):
            err = InvalidInterval(f"{upper} <= {lower}")
            return Result.failure(Exception(err))
        obj = OpenRightInterval(_Private(), greater_than, lower, upper)
        return Result.success(obj)

    def __contains__(self, point: IntervalPoint[_P]) -> bool:
        return (
            greater_ipoint(self.greater, point, self.lower)
            or point == self.lower
        ) and greater_ipoint(self.greater, self.upper, point)


Interval = Union[
    ClosedInterval[_P],
    OpenInterval[_P],
    OpenLeftInterval[_P],
    OpenRightInterval[_P],
]
