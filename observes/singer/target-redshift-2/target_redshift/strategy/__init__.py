from ._core import (
    LoadingStrategy,
)
from ._only_append import (
    OnlyAppend,
)
from ._per_stream import (
    RecreatePerStream,
)
from ._recreate_all import (
    RecreateAll,
)
from ._staging import (
    common_pre_upload,
    StagingProcedure,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from redshift_client.client.schema import (
    SchemaClient,
)
from redshift_client.client.table import (
    TableClient,
)
from redshift_client.core.id_objs import (
    Identifier,
    SchemaId,
)
from redshift_client.sql_client import (
    SqlClient,
)
from typing import (
    FrozenSet,
)


@dataclass(frozen=True)
class Strategies:
    """namespace for supported strategies"""

    @staticmethod
    def recreate_all_schema(
        client: SqlClient, target: SchemaId
    ) -> LoadingStrategy:
        """
        - executes loading procedure on a pristine (empty) staging schema
        - saves `target` as backup
        - sets staging schema as the new `target`
        """
        _client = SchemaClient(client)
        _client_2 = TableClient(client)
        _staging = common_pre_upload(
            target, _client, _client_2, frozenset(), True
        )
        return RecreateAll(_staging, _client).strategy

    @staticmethod
    def recreate_per_stream(
        client: SqlClient, target: SchemaId, persistent_tables: FrozenSet[str]
    ) -> LoadingStrategy:
        """
        - executes loading procedure on a pristine (empty) staging schema
        - migrates (overrides) all NON `persistent_tables` on staging over the `target`
        - appends/moves data of `persistent_tables` on staging over the `target`
        """
        _client = SchemaClient(client)
        _client_2 = TableClient(client)
        _persistent_tables = frozenset(
            Identifier.new(i) for i in persistent_tables
        )
        _staging = common_pre_upload(
            target, _client, _client_2, _persistent_tables, True
        )
        return RecreatePerStream(
            _staging, _client, _client_2, persistent_tables
        ).strategy

    @staticmethod
    def only_append(
        client: SqlClient, target: SchemaId, pristine: bool
    ) -> Cmd[LoadingStrategy]:
        """
        - executes loading procedure on a pristine (if enabled) staging schema
        - appends/moves data of staging over the `target`
        """
        _client = SchemaClient(client)
        _client_2 = TableClient(client)
        _target_tables = _client.table_ids(target).map(
            lambda s: from_flist(tuple(s)).map(lambda t: t.table.name)
        )
        _staging = _target_tables.map(
            lambda persistent: common_pre_upload(
                target, _client, _client_2, frozenset(persistent), pristine
            )
        )
        return _staging.map(
            lambda s: OnlyAppend(s, _client, _client_2).strategy
        )


__all__ = [
    "LoadingStrategy",
]
