from ._input import (
    InputEmitter,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    Maybe,
)
from fa_purity.stream.transform import (
    consume,
    filter_opt,
)
from fa_singer_io.singer import (
    SingerSchema,
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
    S3Factory,
)
from target_redshift._utils import (
    set_queue_group,
    ThreadPool,
)
from target_redshift.grouper import (
    PackagedSinger,
)
from target_redshift.loader import (
    Loaders,
)
from utils_logger_2 import (
    start_session,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class FromS3Executor:
    db_id: DatabaseId
    db_creds: Credentials
    schema: SchemaId
    bucket: str
    prefix: str
    role: str
    ignore_failed: bool
    wlm_queue: Maybe[str]
    pool: ThreadPool

    def _upload_schema(
        self,
        client: SqlClient,
        table_client: TableClient,
        target: SchemaId,
        commit: Cmd[None],
    ) -> Cmd[None]:
        _input = InputEmitter(self.ignore_failed).input_stream
        loader = S3Factory.new_aug_client().map(
            lambda c: Loaders.s3_loader(
                c,
                client,
                table_client,
                self.pool,
                self.bucket,
                self.prefix,
                self.role,
                commit,
            )
        )
        return loader.bind(
            lambda _loader: _input.map(
                lambda m: m if isinstance(m, SingerSchema) else None
            )
            .transform(lambda s: filter_opt(s))
            .map(PackagedSinger.new)
            .map(lambda m: _loader.handle(target, m))
            .transform(lambda s: consume(s))
        )

    def _main(
        self, new_client: Cmd[SqlClient], commit: Cmd[None]
    ) -> Cmd[None]:
        _set_wlm = self.wlm_queue.map(
            lambda q: new_client.bind(lambda c: set_queue_group(c, q))
        ).value_or(Cmd.from_cmd(lambda: None))
        table_client = new_client.map(TableClient)

        return _set_wlm + table_client.bind(
            lambda tc: new_client.bind(
                lambda c: self._upload_schema(c, tc, self.schema, commit)
            )
        )

    def execute(self) -> Cmd[None]:
        return start_session() + DbConnection.connect_and_execute(
            self.db_id,
            self.db_creds,
            False,
            IsolationLvl.READ_COMMITTED,
            False,
            lambda c: self._main(new_client(c, LOG), c.commit()),
        )
