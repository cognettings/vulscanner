from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from fa_purity import (
    Cmd,
)
from typing import (
    Callable,
    Generic,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class _Private:
    pass


@dataclass
class Mutable(Generic[_T]):
    _private: _Private = field(repr=False, hash=False, compare=False)
    _item: _T

    @staticmethod
    def new(init: _T) -> Cmd[Mutable[_T]]:
        return Cmd.from_cmd(lambda: Mutable(_Private(), init))

    def get(self) -> Cmd[_T]:
        return Cmd.from_cmd(lambda: self._item)

    def update(self, item: _T) -> Cmd[None]:
        def _action() -> None:
            self._item = item

        return Cmd.from_cmd(_action)

    def mutate(self, mutation: Callable[[_T], _T]) -> Cmd[None]:
        return self.get().map(mutation).bind(self.update)
