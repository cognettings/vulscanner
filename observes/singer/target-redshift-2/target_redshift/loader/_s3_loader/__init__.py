from . import (
    _upload,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    Maybe,
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
    SqlClient,
)
from target_redshift._s3 import (
    AugmentedS3Client,
    S3URI,
)
from target_redshift._utils import (
    ThreadPool,
)
from target_redshift.grouper import (
    PackagedSinger,
)
from target_redshift.loader._common import (
    CommonSingerHandler,
    MutableTableMap,
    SingerHandlerOptions,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class S3Handler:
    _schema: SchemaId
    _s3_client: AugmentedS3Client
    _db_client: SqlClient
    _table_client: TableClient
    _pool: ThreadPool
    _bucket: str
    _prefix: str
    _iam_role: str
    _commit: Cmd[None]

    def _upload(self, schema: SingerSchema, data_file: S3URI) -> Cmd[None]:
        return _upload.upload_to_redshift(
            self._db_client, self._schema, self._iam_role, schema, data_file
        )

    def _handle_schema(self, schema: SingerSchema) -> Cmd[None]:
        single_file_uri = S3URI(
            self._bucket, self._prefix + schema.stream + ".csv"
        )
        multi_file_uri = S3URI(
            self._bucket, self._prefix + schema.stream + ".part_"
        )
        target: Cmd[Maybe[S3URI]] = (
            self._s3_client.exist_prefix(multi_file_uri)
            .map(lambda b: Maybe.from_optional(multi_file_uri if b else None))
            .bind(
                lambda m: m.map(
                    lambda u: Cmd.from_cmd(lambda: Maybe.from_value(u))
                ).or_else_call(
                    lambda: self._s3_client.exist_file(single_file_uri).map(
                        lambda b: Maybe.from_optional(
                            single_file_uri if b else None
                        )
                    )
                )
            )
        )

        def _action(file_uri: S3URI) -> Cmd[None]:
            start = Cmd.from_cmd(
                lambda: LOG.info(
                    "Appending data: %s -> %s.%s",
                    file_uri.uri,
                    self._schema.name.to_str(),
                    schema.stream,
                )
            )
            end = Cmd.from_cmd(
                lambda: LOG.info(
                    "S3 data uploaded into %s.%s",
                    self._schema.name.to_str(),
                    schema.stream,
                )
            )
            return start + self._upload(schema, file_uri) + end

        skip = Cmd.from_cmd(
            lambda: LOG.warning(
                "Ignoring nonexistent S3 file (.csv) or prefix (.part_): %s",
                S3URI(self._bucket, self._prefix + schema.stream),
            )
        )

        return target.bind(lambda m: m.map(_action).value_or(skip))

    def handle(self, item: PackagedSinger) -> Cmd[None]:
        ignored_records = Cmd.from_cmd(
            lambda: LOG.warning(
                "S3 loader ignores `PureIter[SingerRecord]` items"
            )
        )
        ignored_state = Cmd.from_cmd(
            lambda: LOG.warning("S3 loader ignores `SingerState` items")
        )
        mock_options = SingerHandlerOptions(True, 1)
        handler = CommonSingerHandler(
            self._schema,
            self._table_client,
            mock_options,
            Maybe.empty(),
            self._pool,
        )
        return item.map(
            lambda _: ignored_records,
            lambda s: handler.handle(
                MutableTableMap({}), PackagedSinger.new(s)
            )
            + self._commit
            + self._handle_schema(s)
            + self._commit,
            lambda _: ignored_state,
        )
