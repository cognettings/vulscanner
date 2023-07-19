from __future__ import (
    annotations,
)

from collections.abc import (
    Iterable,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    PureIter,
    Stream,
)
from fa_purity.cmd import (
    unsafe_unwrap,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
)
from pathos.threading import (
    ThreadPool as _RawThreadPool,
)
from threading import (
    Lock as _Lock,
)
from typing import (
    cast,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)  # type: ignore[misc]
class _ThreadPool:  # type: ignore[no-any-unimported]
    pool: _RawThreadPool  # type: ignore[no-any-unimported]


@dataclass(frozen=True)
class ThreadPool:
    _inner: _ThreadPool

    @staticmethod
    def new(nodes: int) -> Cmd[ThreadPool]:
        return Cmd.from_cmd(
            lambda: ThreadPool(_ThreadPool(_RawThreadPool(nodes=nodes)))  # type: ignore[misc]
        )

    def in_threads(
        self, commands: PureIter[Cmd[None]] | Stream[Cmd[None]]
    ) -> Cmd[None]:
        def _action(act: CmdUnwrapper) -> None:
            def _iter_obj() -> Iterable[Cmd[None]]:
                if isinstance(commands, PureIter):
                    return commands
                return act.unwrap(commands.unsafe_to_iter())

            results: Iterable[None] = cast(
                Iterable[None],
                self._inner.pool.imap(lambda c: act.unwrap(c), _iter_obj()),  # type: ignore[misc]
            )
            for _ in results:
                # compute ThreadPool jobs
                pass

        return Cmd.new_cmd(_action)


@dataclass(frozen=True)
class ThreadLock:
    _inner: _Lock

    @staticmethod
    def new() -> Cmd[ThreadLock]:
        return Cmd.from_cmd(lambda: ThreadLock(_Lock()))

    def execute_with_lock(self, cmd: Cmd[_T]) -> Cmd[_T]:
        def _action(unwrapper: CmdUnwrapper) -> _T:
            with self._inner:
                return unwrapper.act(cmd)

        return Cmd.new_cmd(_action)
