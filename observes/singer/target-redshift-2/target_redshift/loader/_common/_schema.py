from ._base import (
    SchemaId,
    SingerSchema,
    TableClient,
    TableId,
)
from fa_purity import (
    Cmd,
)
from redshift_client.core.id_objs import (
    DbTableId,
    Identifier,
)
from redshift_client.core.table import (
    Table,
    TableAttrs,
)
from target_redshift import (
    _utils,
)
from target_redshift.data_schema import (
    extract_table,
)


def _handle_new_columns(
    client: TableClient, singer_table: Table, current_table: DbTableId
) -> Cmd[None]:
    nothing = Cmd.from_cmd(lambda: None)
    return client.get(current_table).bind(
        lambda t: _utils.add_missing_columns(
            client, singer_table, (current_table, t)
        )
        if singer_table != t
        else nothing
    )


def _create_table(
    client: TableClient, table_id: DbTableId, schema: SingerSchema
) -> Cmd[None]:
    singer_table = extract_table(schema).unwrap()
    return client.exist(table_id).bind(
        lambda exist: _handle_new_columns(client, singer_table, table_id)
        if exist
        else client.new(table_id, singer_table, TableAttrs.auto(), False)
    )


def schema_handler(
    client: TableClient, schema: SchemaId, data_schema: SingerSchema
) -> Cmd[None]:
    table_id = DbTableId(schema, TableId(Identifier.new(data_schema.stream)))
    return _create_table(client, table_id, data_schema)
