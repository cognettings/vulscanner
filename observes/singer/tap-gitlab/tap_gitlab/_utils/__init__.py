from collections.abc import (
    Iterator,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from dateutil.parser import (
    isoparse,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    FrozenList,
    Maybe,
    PureIter,
    Result,
    ResultE,
    Stream,
    UnfoldedJVal,
)
from fa_purity.cmd.core import (
    unsafe_unwrap,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.pure_iter.factory import (
    unsafe_from_cmd as piter_unsafe,
)
from fa_purity.stream.factory import (
    unsafe_from_cmd,
)
from fa_purity.utils import (
    raise_exception,
)
from logging import (
    Logger,
)
from more_itertools import (
    split_when as _split_when,
    windowed,
)
from typing import (
    Callable,
    cast,
    Dict,
    Iterable,
    List,
    NoReturn,
    Tuple,
    TypeVar,
)

_K = TypeVar("_K")
_T = TypeVar("_T")
_S = TypeVar("_S")
_F = TypeVar("_F")


@dataclass(frozen=True)
class AppBug(Exception):
    traceback: Exception

    def __str__(self) -> str:
        return f"If raised then there is a logic bug in the `tap_gitlab` program i.e. {self.traceback}"


def to_unfolded(item: UnfoldedJVal) -> UnfoldedJVal:
    return item


def merge_dicts(items: FrozenList[FrozenDict[_K, _T]]) -> FrozenDict[_K, _T]:
    result: Dict[_K, _T] = {}
    for i in items:
        result = result | dict(i)
    return freeze(result)


def chain_maybe_dicts(
    items: FrozenList[Maybe[FrozenDict[_K, _T]]]
) -> FrozenDict[_K, _T]:
    empty: Dict[_K, _T] = {}
    return merge_dicts(tuple(i.value_or(freeze(empty)) for i in items))


def raise_and_log(log: Logger, err: Exception, at_input: str) -> NoReturn:
    log.error("Error at input %s", at_input)
    raise_exception(err)


def str_to_int(raw: str) -> ResultE[int]:
    try:
        return Result.success(int(raw))
    except ValueError as err:
        return Result.failure(Exception(err))


def str_to_datetime(raw: str) -> ResultE[datetime]:
    try:
        return Result.success(isoparse(raw))
    except ValueError as err:
        return Result.failure(Exception(err))


def merge_maybe_result(item: Maybe[Result[_S, _F]]) -> Result[Maybe[_S], _F]:
    _empty: Result[Maybe[_S], _F] = Result.success(Maybe.empty())
    return item.map(lambda r: r.map(lambda x: Maybe.from_value(x))).value_or(
        _empty
    )


def append_to_stream(
    stream: Stream[_T], calc_item: Callable[[Maybe[_T]], Maybe[Cmd[_T]]]
) -> Stream[_T]:
    def _iter(prev: Iterable[_T]) -> Iterable[_T]:
        last: Maybe[_T] = Maybe.empty()
        for i in prev:
            last = Maybe.from_value(i)
            yield i
        result = calc_item(last)
        if result.map(lambda _: True).value_or(False):
            yield unsafe_unwrap(result.unwrap())

    return unsafe_from_cmd(stream.unsafe_to_iter().map(_iter))


def until_condition(
    stream: Stream[_T], condition: Callable[[_T], bool]
) -> Stream[_T]:
    def _iter(prev: Iterable[_T]) -> Iterable[_T]:
        for i in prev:
            yield i
            if condition(i):
                break

    return unsafe_from_cmd(stream.unsafe_to_iter().map(_iter))


def int_to_str(num: int) -> str:
    # It is better no to use str function directly
    # since the argument is equivalent to Any
    return str(num)


def squash_cmd_stream(stream: Cmd[Stream[_T]]) -> Stream[_T]:
    return unsafe_from_cmd(stream.bind(lambda s: s.unsafe_to_iter()))


def to_stream(items: PureIter[_T]) -> Stream[_T]:
    def _new_iter() -> Iterable[_T]:
        return items

    new_iter: Cmd[Iterable[_T]] = Cmd.from_cmd(lambda: _new_iter())
    return unsafe_from_cmd(new_iter)


def split_when(
    items: PureIter[_T],
    condition: Callable[[_T, _T], bool],
    max_split: int | None,
) -> PureIter[FrozenList[_T]]:
    def _new_iter() -> Iterable[FrozenList[_T]]:
        _iter: Iterator[List[_T]] = (
            _split_when(items, condition, max_split)
            if max_split
            else _split_when(items, condition)
        )
        for i in _iter:
            yield tuple(i)

    return piter_unsafe(Cmd.from_cmd(_new_iter))


def in_pairs(items: PureIter[_T]) -> PureIter[Tuple[_T, _T]]:
    new_iter = Cmd.from_cmd(
        lambda: cast(
            Iterable[Tuple[_T, _T]],
            windowed(items, 2),
        )
    )
    return piter_unsafe(new_iter)
