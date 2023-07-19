from ._common import (
    CommonSingerHandler,
    MutableTableMap,
    SingerHandlerOptions,
)
from ._core import (
    SingerLoader,
)
from ._s3_loader import (
    S3Handler,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    Maybe,
)
from redshift_client.client.table import (
    TableClient,
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


@dataclass(frozen=True)
class Loaders:
    @staticmethod
    def common_loader(
        thread_pool: ThreadPool,
        client: TableClient,
        options: SingerHandlerOptions,
        s3_state: Maybe[S3URI],
    ) -> SingerLoader:
        """
        - upload singer records into redshift
        - transforms singer schemas into redshift tables
        - saves singer states into a s3 file
        """
        state = MutableTableMap({})
        return SingerLoader(
            lambda s, p: CommonSingerHandler(
                s, client, options, s3_state, thread_pool
            ).handle(state, p)
        )

    @staticmethod
    def s3_loader(
        client: AugmentedS3Client,
        db_client: SqlClient,
        table_client: TableClient,
        thread_pool: ThreadPool,
        bucket: str,
        prefix: str,
        iam_role: str,
        commit: Cmd[None],
    ) -> SingerLoader:
        """
        - transforms singer schemas into redshift tables
        and uploads the corresponding s3 data file into redshift
        - [WARNING] ignores singer records
        - [WARNING] ignores singer states
        """
        return SingerLoader(
            lambda s, p: S3Handler(
                s,
                client,
                db_client,
                table_client,
                thread_pool,
                bucket,
                prefix,
                iam_role,
                commit,
            ).handle(p)
        )
