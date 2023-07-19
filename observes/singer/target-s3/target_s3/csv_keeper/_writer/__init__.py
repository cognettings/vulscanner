from __future__ import (
    annotations,
)

from ._core import (
    CsvWriter,
)
from fa_purity import (
    Cmd,
    FrozenList,
    PureIter,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
)
from fa_purity.cmd.transform import (
    serial_merge,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    from_range,
)
import logging
from target_s3._parallel import (
    ThreadLock,
    ThreadPool,
)
from target_s3.core import (
    TempFile,
    TempReadOnlyFile,
)
from target_s3.csv_keeper._format import (
    RawFormatedRecord,
)
from typing import (
    TypeVar,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


def _wrap_exception(cmd: Cmd[_T]) -> Cmd[_T]:
    def _action(unwrapper: CmdUnwrapper) -> _T:
        try:
            return unwrapper.act(cmd)
        except Exception as err:
            LOG.error("writerow(s) error: %s", str(err))
            raise err

    return Cmd.new_cmd(_action)


def _write_row_with_lock(
    lock: ThreadLock, writer: CsvWriter, row: RawFormatedRecord
) -> Cmd[None]:
    _wrapped = _wrap_exception(writer.write_row(row.record))
    return lock.execute_with_lock(_wrapped)


def save_raw(
    pool: ThreadPool, data: PureIter[RawFormatedRecord]
) -> Cmd[TempReadOnlyFile]:
    def write_cmd(lock: ThreadLock, writer: CsvWriter) -> Cmd[None]:
        return pool.in_threads(
            data.map(lambda r: _write_row_with_lock(lock, writer, r)),
        )

    return ThreadLock.new().bind(
        lambda lock: TempReadOnlyFile.from_cmd(
            lambda io: CsvWriter.new(io).bind(lambda w: write_cmd(lock, w))
        )
    )


def _write_rows_with_lock(
    lock: ThreadLock, file: TempFile, row: FrozenList[RawFormatedRecord]
) -> Cmd[None]:
    return lock.execute_with_lock(
        file.append(
            lambda io: _wrap_exception(
                CsvWriter.new(io).bind(
                    lambda w: w.write_rows(tuple(r.record for r in row))
                )
            )
        )
    )


def multifile_save(
    pool: ThreadPool,
    data: PureIter[RawFormatedRecord],
    chunks: int,
    parts: int,
) -> Cmd[FrozenList[TempReadOnlyFile]]:
    def _upload(
        files: FrozenList[TempFile], locks: FrozenList[ThreadLock]
    ) -> Cmd[None]:
        def _next_state(n: int) -> int:
            # Generator of cyclic group Z_parts
            # i.e. 0 1 2 ... (parts-1) 0 1 ... (parts-1)...
            if n + 1 >= parts:
                return 0
            return n + 1

        upload_cmds = data.chunked(chunks).generate(
            lambda n, r: (
                _next_state(n),
                _write_rows_with_lock(locks[n], files[n], r),
            ),
            0,
        )
        return pool.in_threads(upload_cmds)

    def _freeze(
        files: FrozenList[TempFile],
    ) -> Cmd[FrozenList[TempReadOnlyFile]]:
        return (
            from_flist(files)
            .map(lambda t: t.read(TempReadOnlyFile.freeze_io))
            .transform(lambda i: serial_merge(i.to_list()))
        )

    locks = serial_merge(tuple(ThreadLock.new() for _ in range(parts)))
    files = (
        from_range(range(parts))
        .map(lambda _: TempFile.new())
        .transform(lambda i: serial_merge(i.to_list()))
    )
    return files.bind(
        lambda f: locks.bind(lambda lks: _upload(f, lks)) + _freeze(f)
    )
