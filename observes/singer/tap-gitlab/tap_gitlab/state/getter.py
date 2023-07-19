from __future__ import (
    annotations,
)

import boto3
from dataclasses import (
    dataclass,
    field,
)
from fa_purity import (
    Cmd,
    Result,
    ResultE,
)
from fa_purity.json_2.value import (
    JsonValueFactory,
)
from io import (
    TextIOWrapper,
)
from mypy_boto3_s3.client import (
    S3Client,
)
from tap_gitlab.state._objs import (
    EtlState,
)
from tap_gitlab.state.decoder import (
    decode_etl_state,
)
import tempfile


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class S3URI:
    bucket: str
    obj_key: str

    @staticmethod
    def from_uri(uri: str) -> ResultE[S3URI]:
        s3_prefix = "s3://"
        if uri.startswith(s3_prefix):
            parts = uri.removeprefix(s3_prefix).split("/", 1)
            return Result.success(S3URI(parts[0], parts[1]))
        return Result.failure(Exception(f"invalid s3 URI i.e. {uri}"))


def _obj_exist(s3_client: S3Client, uri: S3URI) -> Cmd[bool]:
    def _action() -> bool:
        try:
            s3_client.get_object(Bucket=uri.bucket, Key=uri.obj_key)
            return True
        except (
            s3_client.exceptions.NoSuchBucket,
            s3_client.exceptions.NoSuchKey,
        ):
            return False

    return Cmd.from_cmd(_action)


def _new_s3_client() -> Cmd[S3Client]:
    def _action() -> S3Client:
        return boto3.client("s3")

    return Cmd.from_cmd(_action)


@dataclass(frozen=True)
class StateGetter:
    _private: _Private = field(repr=False, hash=False, compare=False)
    s3_client: S3Client

    @staticmethod
    def new() -> Cmd[StateGetter]:
        return _new_s3_client().map(lambda c: StateGetter(_Private(), c))

    def _get(self, uri: S3URI) -> Cmd[ResultE[EtlState]]:
        """
        WARNING: partial function. Ensure that the s3 object exist.
        """

        def _action() -> ResultE[EtlState]:
            with tempfile.TemporaryFile("w+b") as temp:
                self.s3_client.download_fileobj(uri.bucket, uri.obj_key, temp)
                temp.seek(0)
                with TextIOWrapper(temp, encoding="utf-8") as temp_2:
                    raw = JsonValueFactory.loads(temp_2.read())
                    return raw.bind(decode_etl_state)

        return Cmd.from_cmd(_action)

    def get(self, uri: S3URI) -> Cmd[ResultE[EtlState]]:
        return _obj_exist(self.s3_client, uri).bind(
            lambda b: self._get(uri)
            if b
            else Cmd.from_cmd(
                lambda: Result.failure(Exception(f"Not found {uri}"))
            )
        )
