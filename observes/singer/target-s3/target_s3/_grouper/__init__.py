from ._core import (
    GroupedRecords,
    Grouper,
    GrouperResult,
    SchemasMap,
)
from fa_purity import (
    Cmd,
    Stream,
)
from fa_singer_io.singer import (
    SingerMessage,
    SingerRecord,
)
from fa_singer_io.singer.schema import (
    SingerSchema,
)
import logging
from target_s3._parallel import (
    ThreadPool,
)

LOG = logging.getLogger(__name__)


def singer_handler(
    schemas: SchemasMap, grouper: Grouper, singer: SingerMessage
) -> Cmd[None]:
    if isinstance(singer, SingerRecord):
        return grouper.write_record(singer)
    if isinstance(singer, SingerSchema):
        return schemas.add_schema(singer)
    return Cmd.from_cmd(lambda: None)


def _freeze_result(
    schemas: SchemasMap, grouper: Grouper
) -> Cmd[GrouperResult]:
    return schemas.freeze().bind(
        lambda s: grouper.freeze().map(
            lambda g: GrouperResult(
                s, tuple(GroupedRecords(k, v) for k, v in g.items())
            )
        )
    )


def group_records(
    pool: ThreadPool,
    data: Stream[SingerMessage],
) -> Cmd[GrouperResult]:
    start = Cmd.from_cmd(lambda: LOG.info("Grouping records..."))
    end = Cmd.from_cmd(lambda: LOG.info("Records grouping completed!"))
    return start + SchemasMap.new().bind(
        lambda sm: Grouper.new().bind(
            lambda g: pool.in_threads(
                data.map(lambda m: singer_handler(sm, g, m))
            )
            + end
            + _freeze_result(sm, g)
        )
    )


__all__ = ["GroupedRecords"]
