from ._staging import (
    StagingSchemas,
)
from fa_purity import (
    Cmd,
)
from fa_purity.pure_iter.factory import (
    pure_map,
)
from fa_purity.pure_iter.transform import (
    consume,
)
from redshift_client.client.schema import (
    SchemaClient,
)
from redshift_client.client.table import (
    TableClient,
)
from redshift_client.core.id_objs import (
    DbTableId,
)
from target_redshift import (
    _utils,
)
from typing import (
    FrozenSet,
    Literal,
)


def _add_missing_columns(
    client: TableClient, source: DbTableId, target: DbTableId
) -> Cmd[None]:
    nothing = Cmd.from_cmd(lambda: None)
    return client.get(source).bind(
        lambda s: client.get(target).bind(
            lambda t: _utils.add_missing_columns(client, s, (target, t))
            if s != t
            else nothing
        )
    )


def move_data(
    sh_client: SchemaClient,
    tb_client: TableClient,
    persistent_tables: FrozenSet[str] | Literal["ALL"],
    schemas: StagingSchemas,
) -> Cmd[None]:
    """
    loading -> target
    - migrate non-persistent tables
    - move persistent tables
    """

    def _to_target(table: DbTableId) -> Cmd[None]:
        target = DbTableId(schemas.target, table.table)
        if (
            persistent_tables == "ALL"
            or table.table.name.to_str() in persistent_tables
        ):
            return _add_missing_columns(
                tb_client, table, target
            ) + tb_client.move(table, target)
        return tb_client.migrate(table, target)

    return sh_client.table_ids(schemas.loading).bind(
        lambda tables: consume(pure_map(_to_target, tuple(tables)))
    )
