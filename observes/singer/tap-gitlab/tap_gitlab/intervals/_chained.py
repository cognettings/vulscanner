from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from fa_purity import (
    FrozenList,
    Result,
    ResultE,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from tap_gitlab import (
    _utils,
)
from tap_gitlab.intervals.interval import (
    Comparison,
    greater_ipoint,
    IntervalFactory,
    IntervalPoint,
    InvalidInterval,
    MAX,
    MIN,
    OpenLeftInterval,
)
from typing import (
    Generic,
    Optional,
    TypeVar,
)

_P = TypeVar("_P")


@dataclass(frozen=True)
class _Private:
    pass


class InvalidEndpoints(Exception):
    pass


def _to_endpoints(
    intervals: FrozenList[OpenLeftInterval[_P]],
) -> FrozenList[IntervalPoint[_P]]:
    endpoints: FrozenList[IntervalPoint[_P]] = tuple()
    if not intervals:
        raise InvalidInterval("Empty intervals")
    for interval in intervals:
        if not endpoints:
            endpoints = endpoints + (interval.lower, interval.upper)
        else:
            if endpoints[-1] == interval.lower:
                endpoints = endpoints + (interval.upper,)
            else:
                raise InvalidInterval(
                    f"discontinuous: {endpoints[-1]} + {interval}"
                )
    return endpoints


def _to_intervals(
    factory: IntervalFactory[_P],
    endpoints: FrozenList[IntervalPoint[_P]],
) -> FrozenList[OpenLeftInterval[_P]]:
    def _new_interval(
        p_1: Optional[IntervalPoint[_P]],
        p_2: Optional[IntervalPoint[_P]],
    ) -> OpenLeftInterval[_P]:
        if (
            p_1
            and p_2
            and not isinstance(p_1, MAX)
            and not isinstance(p_2, (MIN, MAX))
        ):
            return factory.new_left_open(p_1, p_2)
        raise InvalidEndpoints()

    return tuple(
        _new_interval(p_1, p_2)
        for p_1, p_2 in _utils.in_pairs(from_flist(endpoints))
    )


@dataclass(frozen=True)
class ChainedOpenLeft(Generic[_P]):
    _private: _Private = field(repr=False, hash=False, compare=False)
    greater: Comparison[_P]
    endpoints: FrozenList[IntervalPoint[_P]]
    intervals: FrozenList[OpenLeftInterval[_P]]

    @staticmethod
    def new(
        greater: Comparison[_P],
        endpoints: FrozenList[IntervalPoint[_P]],
    ) -> ResultE[ChainedOpenLeft[_P]]:
        """
        - endpoints must be in acesendent order **up to** the greater funcion
        - avoid providing different instances of the greater function.
        Even if equivalent two functions are not equal if they are not the
        same instance e.g. using a lambda expresion
        ```
            f = lambda x: x
            g = lambda x: x # same definition as f but a different instance
            h = f
            g == f # False
            h == f # True
        ```
        """
        illegal = (
            _utils.in_pairs(from_flist(endpoints))
            .map(lambda t: (greater_ipoint(greater, t[0], t[1]), t))
            .find_first(lambda p: p[0])
        )

        def _fail(
            a: IntervalPoint[_P], b: IntervalPoint[_P]
        ) -> ResultE[ChainedOpenLeft[_P]]:
            err = Exception(
                f"Break points are not in ascendent order i.e. {a} > {b}"
            )
            return Result.failure(err)

        return illegal.map(lambda i: _fail(i[1][0], i[1][1])).or_else_call(
            lambda: Result.success(
                ChainedOpenLeft(
                    _Private(),
                    greater,
                    endpoints,
                    _to_intervals(IntervalFactory(greater), endpoints),
                )
            )
        )

    @classmethod
    def from_intervals(
        cls, intervals: FrozenList[OpenLeftInterval[_P]]
    ) -> ResultE[ChainedOpenLeft[_P]]:
        """
        - intervals should not be an empty list
        - intervals must share the same greater funcion instance
        - interval end must coincide with the start of the next interval
        - intervals must be in acesendent order **up to** the greater funcion
        """
        try:
            base = intervals[0]
        except KeyError as err:
            return Result.failure(Exception(err))
        common_greater = all(
            from_flist(intervals).map(lambda i: i.greater == base.greater)
        )
        if not common_greater:
            return Result.failure(
                Exception(
                    f"Not all intervals share the same greater function **reference** i.e. {intervals}"
                )
            )
        endpoints = _to_endpoints(intervals)
        return cls.new(base.greater, endpoints)

    def append(self, item: _P) -> ResultE[ChainedOpenLeft[_P]]:
        """item must be greater than any endpoint present in the chained interval"""
        return self.new(self.greater, self.endpoints + (item,))
