from __future__ import (
    annotations,
)

from ._core import (
    LoadingStrategy,
    LoadProcedure,
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
from redshift_client.client.schema import (
    SchemaClient,
)
from redshift_client.core.id_objs import (
    SchemaId,
)


@dataclass(frozen=True)
class RecreateAll:
    _staging: StagingProcedure
    _client: SchemaClient

    def _post_upload(self, schemas: StagingSchemas) -> Cmd[None]:
        _do_nothing = Cmd.from_cmd(lambda: None)
        drop_backup = self._client.exist(schemas.backup).bind(
            lambda b: self._client.delete_cascade(schemas.backup)
            if b
            else _do_nothing
        )
        rename_old = self._client.exist(schemas.target).bind(
            lambda b: self._client.rename(schemas.target, schemas.backup)
            if b
            else _do_nothing
        )
        rename_loading = self._client.exist(schemas.loading).bind(
            lambda b: self._client.rename(schemas.loading, schemas.target)
            if b
            else _do_nothing
        )
        return drop_backup + rename_old + rename_loading

    def _main(self, procedure: LoadProcedure) -> Cmd[None]:
        return self._staging.main(procedure, self._post_upload)

    @property
    def strategy(self) -> LoadingStrategy:
        return LoadingStrategy(self._main)
