from ._base import (
    Cmd,
    dataclass,
    FrozenDict,
    JsonValue,
    Maybe,
    PureIter,
    Result,
    ResultE,
    RowData,
    SingerRecord,
    Table,
    TableClient,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    pure_map,
)
from fa_purity.result.transform import (
    all_ok,
)
import logging
from redshift_client.core.id_objs import (
    DbTableId,
)
from target_redshift._utils import (
    ThreadPool,
)
from target_redshift.loader import (
    _truncate,
)
from typing import (
    Tuple,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class TableAndRecords:
    table_id: DbTableId
    table: Table
    records: PureIter[SingerRecord]


@dataclass(frozen=True)
class SingerHandlerOptions:
    truncate_str: bool
    records_per_query: int


StreamTables = FrozenDict[str, Tuple[DbTableId, Table]]


def _to_row(table: Table, record: SingerRecord) -> ResultE[RowData]:
    return pure_map(
        lambda c: Maybe.from_optional(record.record.get(c.name.to_str()))
        .to_result()
        .alt(Exception)
        .lash(
            lambda _: Result.success(JsonValue(None), Exception)
            if table.columns[c].nullable
            else Result.failure(
                KeyError(f"on non-nullable column `{c.name}`", table),
                JsonValue,
            ).alt(Exception)
        )
        .bind(lambda x: Unfolder(x).to_any_primitive()),
        table.order,
    ).transform(lambda x: all_ok(tuple(x)).map(lambda d: RowData(d)))


def _upload_records(
    client: TableClient,
    pool: ThreadPool,
    options: SingerHandlerOptions,
    tar: TableAndRecords,
) -> Cmd[None]:
    chunks = tar.records.map(
        lambda r: _to_row(tar.table, r)
        .map(
            lambda d: _truncate.truncate_row(tar.table, d)
            if options.truncate_str
            else d
        )
        .unwrap()
    ).chunked(options.records_per_query)
    commands = chunks.map(
        lambda p: client.insert(
            tar.table_id,
            tar.table,
            from_flist(p),
            1000,
        )
        + Cmd.from_cmd(lambda: LOG.debug("insert done!"))
    )
    return pool.in_threads(commands)


def record_handler(
    client: TableClient,
    pool: ThreadPool,
    options: SingerHandlerOptions,
    table_map: StreamTables,
    records: PureIter[SingerRecord],
) -> Cmd[None]:
    tables = frozenset(records.map(lambda r: r.stream))
    grouped = pure_map(
        lambda t: Maybe.from_optional(table_map.get(t)).map(
            lambda u: TableAndRecords(
                u[0], u[1], records.filter(lambda r: r.stream == t)
            )
        ),
        tuple(tables),
    )
    return grouped.map(
        lambda m: m.map(
            lambda i: _upload_records(client, pool, options, i)
        ).unwrap()
    ).transform(lambda x: pool.in_threads(x))
