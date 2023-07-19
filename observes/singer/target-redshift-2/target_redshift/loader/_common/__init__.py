from ._base import (
    Cmd,
    dataclass,
    Dict,
    FrozenDict,
    logging,
    Maybe,
    S3URI,
    SchemaId,
    SingerSchema,
    SingerState,
    Table,
    TableClient,
    TableId,
    ThreadPool,
    Tuple,
)
from ._records import (
    record_handler,
    SingerHandlerOptions,
    StreamTables,
)
from ._schema import (
    schema_handler,
)
from ._state import (
    save_to_s3,
)
from redshift_client.core.id_objs import (
    DbTableId,
    Identifier,
)
from target_redshift.data_schema import (
    extract_table,
)
from target_redshift.grouper import (
    PackagedSinger,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class MutableTableMap:
    _table_map: Dict[str, Tuple[DbTableId, Table]]

    def update(
        self, items: FrozenDict[str, Tuple[DbTableId, Table]]
    ) -> Cmd[None]:
        return Cmd.from_cmd(lambda: self._table_map.update(items))

    def freeze(self) -> Cmd[StreamTables]:
        return Cmd.from_cmd(lambda: FrozenDict(self._table_map))


@dataclass(frozen=True)
class CommonSingerHandler:
    schema: SchemaId
    client: TableClient
    options: SingerHandlerOptions
    s3_state: Maybe[S3URI]
    thread_pool: ThreadPool

    def update_stream_tables(
        self, table_map: StreamTables, schema: SingerSchema
    ) -> StreamTables:
        table_id = DbTableId(
            self.schema, TableId(Identifier.new(schema.stream))
        )
        table = extract_table(schema).unwrap()
        return (
            FrozenDict(dict(table_map) | {schema.stream: (table_id, table)})
            if schema.stream not in table_map
            else table_map
        )

    def state_handler(self, state: SingerState) -> Cmd[None]:
        nothing = Cmd.from_cmd(lambda: None)
        return self.s3_state.map(lambda f: save_to_s3(f, state)).value_or(
            nothing
        )

    def handle(
        self, state: MutableTableMap, item: PackagedSinger
    ) -> Cmd[None]:
        return item.map(
            lambda records: state.freeze().bind(
                lambda t: record_handler(
                    self.client, self.thread_pool, self.options, t, records
                )
            ),
            lambda schema: state.freeze().bind(
                lambda t: schema_handler(self.client, self.schema, schema)
                + state.update(self.update_stream_tables(t, schema))
            ),
            self.state_handler,
        )


__all__ = [
    "SingerHandlerOptions",
]
