from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from tap_gitlab.intervals.interval._objs import (
    ClosedInterval,
    Comparison,
    MAX,
    MIN,
    OpenInterval,
    OpenLeftInterval,
    OpenRightInterval,
)
from typing import (
    Generic,
    TypeVar,
    Union,
)

_P = TypeVar("_P")


def greater_int(_x: int, _y: int) -> bool:
    return _x > _y


def greater_datetime(_x: datetime, _y: datetime) -> bool:
    return _x > _y


@dataclass(frozen=True)
class IntervalFactory(Generic[_P]):
    """
    [WARNING] remember to use the same `greater` function instance,
    otherwise, the factory and its sub-products (interval objects)
    would never be equal even if the function is equivalent.
    """

    greater: Comparison[_P]

    @classmethod
    def int_default(cls) -> IntervalFactory[int]:
        return IntervalFactory(greater_int)

    @classmethod
    def datetime_default(cls) -> IntervalFactory[datetime]:
        return IntervalFactory(greater_datetime)

    def new_closed(self, lower: _P, upper: _P) -> ClosedInterval[_P]:
        return ClosedInterval.new(self.greater, lower, upper).unwrap()

    def new_open(
        self, lower: Union[_P, MIN], upper: Union[_P, MAX]
    ) -> OpenInterval[_P]:
        return OpenInterval.new(self.greater, lower, upper).unwrap()

    def new_right_open(
        self, lower: _P, upper: Union[_P, MAX]
    ) -> OpenRightInterval[_P]:
        return OpenRightInterval.new(self.greater, lower, upper).unwrap()

    def new_left_open(
        self, lower: Union[_P, MIN], upper: _P
    ) -> OpenLeftInterval[_P]:
        return OpenLeftInterval.new(self.greater, lower, upper).unwrap()
