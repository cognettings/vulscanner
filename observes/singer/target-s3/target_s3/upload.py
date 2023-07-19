from . import (
    _utils,
)
from ._s3 import (
    S3URI,
)
from .core import (
    RecordGroup,
)
from .csv_keeper import (
    CsvKeeper,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    PureIter,
)
import logging
from mypy_boto3_s3.client import (
    S3Client,
)
from target_s3._parallel import (
    ThreadPool,
)
from target_s3.core import (
    TempReadOnlyFile,
)

LOG = logging.getLogger(__name__)


def _msg_wrapper(cmd: Cmd[None], stream: str, s3_file: S3URI) -> Cmd[None]:
    msg = _utils.log_cmd(
        lambda: LOG.info(
            "Uploading stream `%s` -> %s",
            stream,
            s3_file.uri,
        ),
        None,
    )
    end = _utils.log_cmd(
        lambda: LOG.info(
            "%s uploaded!",
            s3_file.uri,
        ),
        None,
    )
    return msg + cmd + end


@dataclass(frozen=True)
class S3FileUploader:
    _pool: ThreadPool
    _client: S3Client
    _bucket: str
    _prefix: str

    def _upload(
        self, file: TempReadOnlyFile, stream: str, target: S3URI
    ) -> Cmd[None]:
        return file.over_binary(
            lambda f: _msg_wrapper(
                Cmd.from_cmd(
                    lambda: self._client.upload_fileobj(
                        f, target.bucket, target.file_obj
                    )
                ),
                stream,
                target,
            )
        )

    def upload_to_s3(
        self, keeper: CsvKeeper[TempReadOnlyFile], group: RecordGroup
    ) -> Cmd[None]:
        file_object = keeper.save(group)
        file_uri = S3URI(
            self._bucket, self._prefix + group.schema.stream + ".csv"
        )

        return file_object.bind(
            lambda f: self._upload(f, group.schema.stream, file_uri)
        )

    def multifile_upload(
        self, keeper: CsvKeeper[PureIter[TempReadOnlyFile]], group: RecordGroup
    ) -> Cmd[None]:
        file_objects = keeper.save(group)

        def _part_uri(part: int) -> S3URI:
            return S3URI(
                self._bucket,
                self._prefix
                + group.schema.stream
                + ".part_"
                + _utils.int_to_str(part)
                + ".csv",
            )

        return file_objects.bind(
            lambda f: self._pool.in_threads(
                f.enumerate(0).map(
                    lambda t: self._upload(
                        t[1], group.schema.stream, _part_uri(t[0])
                    )
                )
            )
        )
