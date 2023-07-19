from __future__ import (
    annotations,
)

from ._chained import (
    ChainedOpenLeft,
)
from dataclasses import (
    dataclass,
    field,
)
from fa_purity import (
    FrozenList,
    PureIter,
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
    IntervalFactory,
    MIN,
    OpenLeftInterval,
)
from typing import (
    Generic,
    TypeVar,
)

_DataType = TypeVar("_DataType")
_I = TypeVar("_I")


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class ProgressInterval(Generic[_I]):
    _interval: _I
    # _I should be restricted only to ClosedInterval, OpenInterval, OpenLeftInterval, OpenRightInterval,
    completed: bool

    @property
    def interval(self) -> _I:
        return self._interval

    def change_completed(self, completed: bool) -> ProgressInterval[_I]:
        if completed != self.completed:
            return ProgressInterval(self._interval, completed)
        return self


_State = TypeVar("_State")


@dataclass(frozen=True)
class ProcessStatus(
    Generic[_DataType, _State],
):
    p_intervals: FrozenList[ProgressInterval[OpenLeftInterval[_DataType]]]
    incomplete_is_present: bool
    function_state: _State


@dataclass(frozen=True)
class FragmentedProgressInterval(Generic[_DataType]):
    _private: _Private = field(repr=False, hash=False, compare=False)
    f_interval: ChainedOpenLeft[_DataType]
    completeness: FrozenList[bool]

    @staticmethod
    def new(
        f_interval: ChainedOpenLeft[_DataType],
        completeness: FrozenList[bool],
    ) -> ResultE[FragmentedProgressInterval[_DataType]]:
        if len(f_interval.endpoints) - 1 == len(completeness):
            obj = FragmentedProgressInterval(
                _Private(), f_interval, completeness
            )
            return Result.success(obj)
        err = Exception("CannotBuild FragmentedProgressInterval")
        return Result.failure(err)

    @classmethod
    def from_progress_intervals(
        cls,
        intervals: FrozenList[ProgressInterval[OpenLeftInterval[_DataType]]],
    ) -> ResultE[FragmentedProgressInterval[_DataType]]:
        open_intervals = from_flist(intervals).map(lambda i: i.interval)
        completeness = from_flist(intervals).map(lambda i: i.completed)
        chained = ChainedOpenLeft.from_intervals(open_intervals.to_list())
        return chained.bind(lambda c: cls.new(c, completeness.to_list()))

    @property
    def progress_intervals(
        self,
    ) -> FrozenList[ProgressInterval[OpenLeftInterval[_DataType]]]:
        intervals = zip(self.f_interval.intervals, self.completeness)
        return tuple(
            ProgressInterval(item, completed) for item, completed in intervals
        )

    def change_completeness(
        self, interval: OpenLeftInterval[_DataType], completed: bool
    ) -> FragmentedProgressInterval[_DataType]:
        intervals = (
            from_flist(self.progress_intervals)
            .map(
                lambda p: p.change_completed(completed)
                if p.interval == interval
                else p
            )
            .to_list()
        )
        return self.from_progress_intervals(intervals).unwrap()

    def append(
        self, item: _DataType
    ) -> ResultE[FragmentedProgressInterval[_DataType]]:
        """item must be greater than any endpoint present in the FP interval"""
        return self.f_interval.append(item).bind(
            lambda i: self.new(i, self.completeness + (False,))
        )

    def squash(self) -> FragmentedProgressInterval[_DataType]:
        """Merges two or more adjacent intervals that share the same completeness into one"""
        grouped = _utils.split_when(
            from_flist(self.progress_intervals),
            lambda p1, p2: p1.completed != p2.completed,
            None,
        )
        compressed: PureIter[
            ProgressInterval[OpenLeftInterval[_DataType]]
        ] = grouped.map(
            lambda g: ProgressInterval(
                IntervalFactory(self.f_interval.greater).new_left_open(
                    g[0].interval.lower, g[-1].interval.upper
                ),
                g[0].completed,
            )
        )
        return self.from_progress_intervals(compressed.to_list()).unwrap()
