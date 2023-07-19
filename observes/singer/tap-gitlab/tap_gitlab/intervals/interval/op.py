from tap_gitlab.intervals.interval._objs import (
    Interval,
)
from typing import (
    TypeVar,
)

_P = TypeVar("_P")


def are_disjoin(interval_1: Interval[_P], interval_2: Interval[_P]) -> bool:
    return not (
        interval_1.lower in interval_2
        or interval_1.upper in interval_2
        or interval_2.lower in interval_1
        or interval_2.upper in interval_1
    )
