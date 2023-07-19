from ._core import (
    LoadingStrategy,
    LoadProcedure,
)
from ._move_data import (
    move_data,
)
from ._staging import (
    StagingProcedure,
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
from redshift_client.client.table import (
    TableClient,
)


@dataclass(frozen=True)
class OnlyAppend:
    _staging: StagingProcedure
    _client: SchemaClient
    _client_2: TableClient

    def _main(self, procedure: LoadProcedure) -> Cmd[None]:
        return self._staging.main(
            procedure,
            lambda s: self._client.create(s.target, True)
            + move_data(self._client, self._client_2, "ALL", s),
        )

    @property
    def strategy(self) -> LoadingStrategy:
        return LoadingStrategy(self._main)
