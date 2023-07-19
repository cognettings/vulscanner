from . import (
    _grouper,
    _s3,
)
from ._grouper import (
    GroupedRecords,
)
from ._input import (
    InputEmitter,
)
from ._output import (
    OutputEmitter,
)
from ._parallel import (
    ThreadPool,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    Maybe,
    Result,
    ResultE,
    Stream,
)
from fa_purity.json.factory import (
    loads,
)
from fa_purity.pure_iter import (
    factory as PureIterFactory,
)
from fa_singer_io.singer import (
    SingerMessage,
    SingerRecord,
    SingerSchema,
)
from fa_singer_io.singer.deserializer import (
    deserialize,
)
import logging
import sys
from target_s3.core import (
    CompletePlainRecord,
    PlainRecord,
    RecordGroup,
)
from target_s3.csv_keeper import (
    CsvKeeperFactory,
)
from target_s3.upload import (
    S3FileUploader,
)
from typing import (
    Callable,
    NoReturn,
    TypeVar,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


def _complete_record(
    schemas: FrozenDict[str, SingerSchema], record: SingerRecord
) -> ResultE[CompletePlainRecord]:
    schema = Maybe.from_optional(schemas.get(record.stream))
    return PlainRecord.from_singer(record).bind(
        lambda p: schema.to_result()
        .alt(lambda _: Exception(f"Missing {record.stream} on schemas map"))
        .bind(lambda sh: CompletePlainRecord.new(sh, p))
    )


def _assert_record(item: _T) -> ResultE[SingerRecord]:
    if isinstance(item, SingerRecord):
        return Result.success(item)
    err = Exception(f"Expected `SingerRecord` got `{type(item)}`")
    return Result.failure(err)


def _process_group(
    upload_to_s3: Callable[[RecordGroup], Cmd[None]],
    schemas: FrozenDict[str, SingerSchema],
    group: GroupedRecords,
) -> Cmd[None] | NoReturn:
    records = group.file.read().map(
        lambda i: loads(i)
        .alt(Exception)
        .bind(deserialize)
        .bind(_assert_record)
    )
    completed = records.map(
        lambda r: r.bind(lambda d: _complete_record(schemas, d))
    )
    schema = schemas[group.stream]
    r_group = RecordGroup.filter(schema, completed.map(lambda x: x.unwrap()))
    return upload_to_s3(r_group)


@dataclass(frozen=True)
class MultifileConf:
    chunks: int
    parts: int


@dataclass(frozen=True)
class Executor:
    bucket: str
    prefix: str
    str_limit: int
    bypass_input: bool
    multifile_streams: FrozenDict[str, MultifileConf]
    pool: ThreadPool

    @property
    def _input(self) -> Stream[SingerMessage]:
        data = InputEmitter(False, sys.stdin.buffer).input_stream
        if self.bypass_input:
            return OutputEmitter(data, sys.stdout).re_emit()
        return data

    def _stream_uploader(
        self, uploader: S3FileUploader, group: RecordGroup
    ) -> Cmd[None]:
        stream = group.schema.stream

        def _multifile(conf: MultifileConf) -> Cmd[None]:
            keeper = CsvKeeperFactory(self.pool).keeper_2(
                self.str_limit, conf.chunks, conf.parts
            )
            return uploader.multifile_upload(keeper, group)

        return (
            Maybe.from_optional(self.multifile_streams.get(stream))
            .map(lambda c: _multifile(c))
            .or_else_call(
                lambda: uploader.upload_to_s3(
                    CsvKeeperFactory(self.pool).keeper_1(self.str_limit), group
                )
            )
        )

    @property
    def main(self) -> Cmd[None] | NoReturn:
        client = _s3.new_client()
        uploader = client.map(
            lambda c: S3FileUploader(self.pool, c, self.bucket, self.prefix)
        )
        start = Cmd.from_cmd(lambda: LOG.info("Process groups started"))
        return uploader.bind(
            lambda u: _grouper.group_records(self.pool, self._input).bind(
                lambda t: start
                + self.pool.in_threads(
                    PureIterFactory.from_flist(
                        tuple(
                            _process_group(
                                lambda r: self._stream_uploader(u, r),
                                t.schemas,
                                g,
                            )
                            for g in t.groups
                        )
                    ),
                )
            )
        )
