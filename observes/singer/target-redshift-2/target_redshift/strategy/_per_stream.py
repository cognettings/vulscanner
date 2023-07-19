from ._core import (
    LoadingStrategy,
    LoadProcedure,
)
from ._move_data import (
    move_data,
)
from ._staging import (
    StagingProcedure,
    StagingSchemas,
)
from dataclasses import (
    dataclass,
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
    TableId,
)
from typing import (
    FrozenSet,
)


@dataclass(frozen=True)
class RecreatePerStream:
    _staging: StagingProcedure
    _client: SchemaClient
    _client_2: TableClient
    _persistent_tables: FrozenSet[str]

    def _backup(self, schemas: StagingSchemas) -> Cmd[None]:
        """migrate non-persistent tables, target -> backup"""

        def _migrate(table: DbTableId) -> Cmd[None]:
            if table.table.name.to_str() in self._persistent_tables:
                return Cmd.from_cmd(lambda: None)
            return self._client_2.migrate(
                table, DbTableId(schemas.backup, table.table)
            )

        create_schema = self._client.recreate_cascade(schemas.backup)
        return create_schema + self._client.table_ids(schemas.target).bind(
            lambda tables: consume(pure_map(_migrate, tuple(tables)))
        )

    def _main(self, procedure: LoadProcedure) -> Cmd[None]:
        return self._staging.main(
            procedure,
            lambda s: self._client.create(s.target, True)
            + self._backup(s)
            + move_data(
                self._client, self._client_2, self._persistent_tables, s
            ),
        )

    @property
    def strategy(self) -> LoadingStrategy:
        return LoadingStrategy(self._main)
