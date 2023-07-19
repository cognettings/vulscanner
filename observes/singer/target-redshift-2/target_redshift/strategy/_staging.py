from __future__ import (
    annotations,
)

from ._core import (
    LoadProcedure,
)
from collections.abc import (
    Callable,
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
    Identifier,
    SchemaId,
    TableId,
)
from typing import (
    FrozenSet,
)


@dataclass(frozen=True)
class StagingSchemas:
    backup: SchemaId
    loading: SchemaId
    target: SchemaId


@dataclass(frozen=True)
class StagingProcedure:
    """
    Procedure that adds pre upload operations for
    the supplied `LoadProcedure`.
    """

    _main: Callable[
        [LoadProcedure, Callable[[StagingSchemas], Cmd[None]]], Cmd[None]
    ]

    def main(
        self,
        procedure: LoadProcedure,
        post_upload: Callable[[StagingSchemas], Cmd[None]],
    ) -> Cmd[None]:
        return self._main(procedure, post_upload)


def common_pre_upload(
    target: SchemaId,
    client: SchemaClient,
    client_2: TableClient,
    persistent_tables: FrozenSet[Identifier],
    pristine_loading: bool,
) -> StagingProcedure:
    _schemas = StagingSchemas(
        SchemaId(Identifier.new(target.name.to_str() + "_backup")),
        SchemaId(Identifier.new(target.name.to_str() + "_loading")),
        target,
    )

    def _mirror_table(table: Identifier) -> Cmd[None]:
        blueprint = DbTableId(_schemas.target, TableId(table))
        mirror = client_2.create_like(
            blueprint, DbTableId(_schemas.loading, TableId(table))
        )
        nothing = Cmd.from_cmd(lambda: None)
        return client_2.exist(blueprint).bind(
            lambda b: mirror if b else nothing
        )

    _mirror_persistent = consume(
        from_flist(tuple(persistent_tables)).map(_mirror_table)
    )

    def _main(
        procedure: LoadProcedure,
        post_upload: Callable[[StagingSchemas], Cmd[None]],
    ) -> Cmd[None]:
        recreate = (
            client.recreate_cascade(_schemas.loading)
            if pristine_loading
            else Cmd.from_cmd(lambda: None)
        )
        upload = procedure(_schemas.loading)
        return recreate + _mirror_persistent + upload + post_upload(_schemas)

    return StagingProcedure(_main)
