from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    Maybe,
    ResultE,
)
from fa_purity.cmd import (
    CmdUnwrapper,
)
from typing import (
    Callable,
    Dict,
    Generic,
    TypeVar,
)

_T = TypeVar("_T")
_K = TypeVar("_K")
_V = TypeVar("_V")


@dataclass(frozen=True)
class _Private:
    pass


def log_cmd(log_action: Callable[[], None], item: _T) -> Cmd[_T]:
    def _action() -> _T:
        log_action()
        return item

    return Cmd.from_cmd(_action)


def int_to_str(num: int) -> str:
    return str(num)


def get_required(obj: FrozenDict[_K, _V], key: _K) -> ResultE[_V]:
    return (
        Maybe.from_optional(obj.get(key))
        .to_result()
        .alt(lambda _: KeyError(key))
        .alt(Exception)
    )


@dataclass(frozen=True)
class MutableMap(Generic[_K, _V]):
    _private: _Private = field(repr=False, hash=False, compare=False)
    _inner: Dict[_K, _V]

    @staticmethod
    def new() -> Cmd[MutableMap[_K, _V]]:
        return Cmd.from_cmd(lambda: MutableMap(_Private(), {}))

    def get(self, key: _K) -> Cmd[Maybe[_V]]:
        def _action() -> Maybe[_V]:
            if key in self._inner:
                return Maybe.from_value(self._inner[key])
            return Maybe.empty()

        return Cmd.from_cmd(_action)

    def get_or(self, key: _K, if_not_exist: Cmd[_V]) -> Cmd[_V]:
        return self.get(key).bind(
            lambda m: m.map(lambda v: Cmd.from_cmd(lambda: v)).value_or(
                if_not_exist
            )
        )

    def override(self, key: _K, value: _V) -> Cmd[None]:
        def _action() -> None:
            self._inner[key] = value

        return Cmd.from_cmd(_action)

    def get_or_create(self, key: _K, value: Cmd[_V]) -> Cmd[_V]:
        return self.get(key).bind(
            lambda m: m.map(lambda v: Cmd.from_cmd(lambda: v)).value_or(
                value.bind(lambda v: self.override(key, v).map(lambda _: v))
            )
        )

    def add_or(self, key: _K, value: _V, if_exist: Cmd[None]) -> Cmd[None]:
        def _action(unwrapper: CmdUnwrapper) -> None:
            if key not in self._inner:
                self._inner[key] = value
            else:
                unwrapper.act(if_exist)

        return Cmd.new_cmd(_action)

    def freeze(self) -> Cmd[FrozenDict[_K, _V]]:
        return Cmd.from_cmd(lambda: FrozenDict(self._inner))
