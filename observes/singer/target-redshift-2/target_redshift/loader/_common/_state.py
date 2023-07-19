from ._base import (
    Cmd,
    S3URI,
    SingerState,
)
import boto3
from fa_purity.json.transform import (
    dumps,
)
import logging
from mypy_boto3_s3 import (
    S3Client,
)
from tempfile import (
    TemporaryFile,
)

LOG = logging.getLogger(__name__)


def _new_s3_client() -> Cmd[S3Client]:
    return Cmd.from_cmd(lambda: boto3.client("s3"))


def _save(client: S3Client, file: S3URI, state: SingerState) -> Cmd[None]:
    def _action() -> None:
        LOG.info("Uploading new state")
        LOG.debug("Uploading state to %s", file)
        with TemporaryFile() as data:
            data.write(dumps(state.value).encode("UTF-8"))
            data.seek(0)
            client.upload_fileobj(data, file.bucket, file.file_path)

    return Cmd.from_cmd(_action)


def save_to_s3(file: S3URI, state: SingerState) -> Cmd[None]:
    return _new_s3_client().bind(lambda c: _save(c, file, state))
