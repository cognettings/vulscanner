from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    FrozenList,
)
from fa_purity.cmd.transform import (
    serial_merge,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_singer_io.singer import (
    SingerRecord,
    SingerSchema,
)
from fa_singer_io.singer.emitter import (
    emit,
)
import logging
from target_s3._parallel import (
    ThreadLock,
)
from target_s3._utils import (
    MutableMap,
)
from target_s3.core import (
    TempFile,
    TempReadOnlyFile,
)
from typing import (
    Tuple,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class GroupedRecords:
    stream: str
    file: TempReadOnlyFile


@dataclass(frozen=True)
class SchemasMap:
    _schemas: MutableMap[str, SingerSchema]

    @staticmethod
    def new() -> Cmd[SchemasMap]:
        _schemas: Cmd[MutableMap[str, SingerSchema]] = MutableMap.new()
        return _schemas.map(lambda m: SchemasMap(m))

    def add_schema(self, schema: SingerSchema) -> Cmd[None]:
        return self._schemas.override(schema.stream, schema)

    def freeze(self) -> Cmd[FrozenDict[str, SingerSchema]]:
        return self._schemas.freeze()


@dataclass(frozen=True)
class Grouper:
    _streams: MutableMap[str, TempFile]
    _locks: MutableMap[str, ThreadLock]

    @staticmethod
    def new() -> Cmd[Grouper]:
        _streams: Cmd[MutableMap[str, TempFile]] = MutableMap.new()
        _locks: Cmd[MutableMap[str, ThreadLock]] = MutableMap.new()
        return _streams.bind(
            lambda s: _locks.map(lambda locks: Grouper(s, locks))
        )

    def get_or_create(self, stream: str) -> Cmd[Tuple[ThreadLock, TempFile]]:
        return self._streams.get_or_create(stream, TempFile.new()).bind(
            lambda f: self._locks.get_or_create(stream, ThreadLock.new()).map(
                lambda lk: (lk, f)
            )
        )

    def write_record(self, record: SingerRecord) -> Cmd[None]:
        return self.get_or_create(record.stream).bind(
            lambda t: t[0].execute_with_lock(
                t[1].append(lambda io: emit(io, record))
            )
        )

    def freeze(self) -> Cmd[FrozenDict[str, TempReadOnlyFile]]:
        return (
            self._streams.freeze()
            .map(
                lambda d: from_flist(tuple(d.items())).map(
                    lambda t: t[1]
                    .read(TempReadOnlyFile.freeze_io)
                    .map(lambda f: (t[0], f))
                )
            )
            .bind(
                lambda pairs: serial_merge(pairs.to_list()).map(
                    lambda t: FrozenDict(dict(t))
                )
            )
        )


@dataclass(frozen=True)
class GrouperResult:
    schemas: FrozenDict[str, SingerSchema]
    groups: FrozenList[GroupedRecords]
