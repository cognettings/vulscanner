from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    PureIter,
    Stream,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
    new_cmd,
)
from fa_purity.pure_iter.factory import (
    unsafe_from_cmd,
)
from fa_purity.stream.factory import (
    unsafe_from_cmd as unsafe_build_stream,
)
import logging
from tempfile import (
    NamedTemporaryFile,
)
from typing import (
    Callable,
    IO,
    Iterable,
    TypeVar,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


@dataclass(frozen=True)
class _Inner:
    file_path: str


@dataclass(frozen=True)
class TempFile:
    _inner: _Inner

    @staticmethod
    def new() -> Cmd[TempFile]:
        def _action() -> TempFile:
            with NamedTemporaryFile("w", delete=False) as file_object:
                return TempFile(_Inner(file_object.name))

        return Cmd.from_cmd(_action)

    def append(self, write_cmd: Callable[[IO[str]], Cmd[None]]) -> Cmd[None]:
        """
        - opens file in append mode and executes `write_cmd`
        [WARNING] executing concurrent `append` commands on the same `TempFile`
        would result in unexpected behavior.
        Wrap this command using `execute_with_lock` from a common `Lock` object
        if concurrency is required.
        """

        def _action(unwrapper: CmdUnwrapper) -> None:
            with open(self._inner.file_path, "a", encoding="utf-8") as file:
                unwrapper.act(write_cmd(file))

        return Cmd.new_cmd(_action)

    def read(self, write_cmd: Callable[[IO[str]], Cmd[_T]]) -> Cmd[_T]:
        def _action(unwrapper: CmdUnwrapper) -> _T:
            with open(self._inner.file_path, "r", encoding="utf-8") as file:
                return unwrapper.act(write_cmd(file))

        return Cmd.new_cmd(_action)


@dataclass(frozen=True)
class TempReadOnlyFile:
    _inner: _Inner

    def over_binary(self, cmd_fx: Callable[[IO[bytes]], Cmd[_T]]) -> Cmd[_T]:
        def _action(act: CmdUnwrapper) -> _T:
            with open(self._inner.file_path, "rb") as file:
                return act.unwrap(cmd_fx(file))

        return new_cmd(_action)

    def read(self) -> PureIter[str]:
        def _new_iter() -> Iterable[str]:
            with open(self._inner.file_path, "r", encoding="utf-8") as file:
                line = file.readline()
                while line:
                    yield line
                    line = file.readline()

        return unsafe_from_cmd(Cmd.from_cmd(_new_iter))

    @staticmethod
    def new(content: PureIter[str]) -> Cmd[TempReadOnlyFile]:
        def _action() -> TempReadOnlyFile:
            with NamedTemporaryFile("w", delete=False) as file_object:
                file_object.writelines(content)
                return TempReadOnlyFile(_Inner(file_object.name))

        return Cmd.from_cmd(_action)

    @staticmethod
    def from_cmd(
        write_cmd: Callable[[IO[str]], Cmd[None]]
    ) -> Cmd[TempReadOnlyFile]:
        """
        `write_cmd` initializes the file content. It has write-only access to file
        """

        def _action(act: CmdUnwrapper) -> TempReadOnlyFile:
            with NamedTemporaryFile("w", delete=False) as file_object:
                act.unwrap(write_cmd(file_object))
                return TempReadOnlyFile(_Inner(file_object.name))

        return new_cmd(_action)

    @staticmethod
    def save(content: Stream[str]) -> Cmd[TempReadOnlyFile]:
        def _action(act: CmdUnwrapper) -> TempReadOnlyFile:
            with NamedTemporaryFile("w", delete=False) as file_object:
                LOG.debug("Saving stream into %s", file_object.name)
                file_object.writelines(act.unwrap(content.unsafe_to_iter()))
                return TempReadOnlyFile(_Inner(file_object.name))

        return new_cmd(_action)

    @classmethod
    def freeze_io(cls, file: IO[str]) -> Cmd[TempReadOnlyFile]:
        def _action() -> Iterable[str]:
            file.seek(0)
            line = file.readline()
            while line:
                yield line
                line = file.readline()

        start = Cmd.from_cmd(lambda: LOG.debug("Freezing file"))
        end = Cmd.from_cmd(lambda: LOG.debug("Freezing completed!"))
        stream = unsafe_build_stream(Cmd.from_cmd(_action))
        return start + cls.save(stream).bind(lambda f: end.map(lambda _: f))

    @classmethod
    def freeze(cls, file_path: str) -> Cmd[TempReadOnlyFile]:
        def _action(unwrapper: CmdUnwrapper) -> TempReadOnlyFile:
            with open(file_path, "r", encoding="utf-8") as file:
                return unwrapper.act(cls.freeze_io(file))

        return Cmd.new_cmd(_action)
