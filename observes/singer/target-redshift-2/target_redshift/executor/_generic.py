from __future__ import (
    annotations,
)

from ._input import (
    InputEmitter,
)
from ._output import (
    OutputEmitter,
)
from collections.abc import (
    Callable,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    Maybe,
)
from fa_purity.union import (
    Coproduct,
)
import logging
from redshift_client.client.table import (
    TableClient,
)
from redshift_client.core.id_objs import (
    SchemaId,
)
from redshift_client.sql_client import (
    DbConnection,
    new_client,
    SqlClient,
)
from redshift_client.sql_client.connection import (
    Credentials,
    DatabaseId,
    IsolationLvl,
)
from target_redshift._s3 import (
    S3URI,
)
from target_redshift._utils import (
    set_queue_group,
    ThreadPool,
)
from target_redshift.loader import (
    Loaders,
    SingerHandlerOptions,
)
from target_redshift.strategy import (
    LoadingStrategy,
)
from utils_logger_2 import (
    start_session,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class GenericExecutor:
    db_id: DatabaseId
    db_creds: Credentials
    target: SchemaId
    options: SingerHandlerOptions
    records_limit: int
    s3_state: Maybe[S3URI]
    wlm_queue: Maybe[str]
    ignore_failed: bool
    strategy: Callable[
        [SqlClient, SchemaId], Coproduct[LoadingStrategy, Cmd[LoadingStrategy]]
    ]
    thread_pool: ThreadPool

    def _upload(
        self,
        client: SqlClient,
        table_client: TableClient,
        s3_state: Maybe[S3URI],
    ) -> Cmd[None]:
        _input = InputEmitter(self.ignore_failed).input_stream
        loader = Loaders.common_loader(
            self.thread_pool, table_client, self.options, s3_state
        )
        return self.strategy(client, self.target).map(
            lambda s: OutputEmitter(
                _input,
                loader,
                s,
                self.records_limit,
            ).main(),
            lambda s: s.bind(
                lambda st: OutputEmitter(
                    _input,
                    loader,
                    st,
                    self.records_limit,
                ).main()
            ),
        )

    def _main(self, new_client: Cmd[SqlClient]) -> Cmd[None]:
        _set_wlm = self.wlm_queue.map(
            lambda q: new_client.bind(lambda c: set_queue_group(c, q))
        ).value_or(Cmd.from_cmd(lambda: None))
        table_client = new_client.map(TableClient)
        return _set_wlm + new_client.bind(
            lambda sql: table_client.bind(
                lambda table: self._upload(sql, table, self.s3_state)
            )
        )

    def execute(self) -> Cmd[None]:
        return start_session() + DbConnection.connect_and_execute(
            self.db_id,
            self.db_creds,
            False,
            IsolationLvl.READ_COMMITTED,
            True,
            lambda c: self._main(new_client(c, LOG)),
        )
