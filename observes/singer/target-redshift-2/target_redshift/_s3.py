from __future__ import (
    annotations,
)

import boto3
from botocore.exceptions import (
    ClientError,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    Result,
    ResultE,
)
from mypy_boto3_s3 import (
    S3Client,
    S3ServiceResource,
)


@dataclass(frozen=True)
class S3URI:
    bucket: str
    file_path: str

    @staticmethod
    def from_raw(raw: str) -> ResultE[S3URI]:
        try:
            if raw.startswith("s3://"):
                _raw = raw.removeprefix("s3://")
                _splitted = _raw.split("/")
                bucket = _splitted[0]
                obj_file = "/".join(_splitted[1:])
                if obj_file:
                    return Result.success(S3URI(bucket, obj_file), Exception)
            return Result.failure(
                ValueError("Invalid s3 file obj URI"), S3URI
            ).alt(Exception)
        except IndexError as err:
            return Result.failure(err, S3URI).alt(Exception)

    @property
    def uri(self) -> str:
        return "s3://" + "/".join([self.bucket, self.file_path])


@dataclass(frozen=True)
class AugmentedS3Client:
    client: S3Client
    client_2: S3ServiceResource

    def exist_file(self, uri: S3URI) -> Cmd[bool]:
        def _action() -> bool:
            try:
                self.client_2.Object(uri.bucket, uri.file_path).load()
            except ClientError as e:  # type: ignore[misc]
                if e.response["Error"]["Code"] == "404":  # type: ignore[misc]
                    return False
                else:
                    raise Exception(f"S3 error: {e.response}")  # type: ignore[misc]
            else:
                return True

        return Cmd.from_cmd(_action)

    def exist_prefix(self, uri: S3URI) -> Cmd[bool]:
        def _action() -> bool:
            response = self.client.list_objects_v2(
                Bucket=uri.bucket, Prefix=uri.file_path, MaxKeys=1
            )
            return "Contents" in response

        return Cmd.from_cmd(_action)


@dataclass(frozen=True)
class S3Factory:
    @staticmethod
    def new_s3_client() -> Cmd[S3Client]:
        return Cmd.from_cmd(lambda: boto3.client("s3"))

    @staticmethod
    def new_s3_resource() -> Cmd[S3ServiceResource]:
        return Cmd.from_cmd(lambda: boto3.resource("s3"))

    @classmethod
    def new_aug_client(cls) -> Cmd[AugmentedS3Client]:
        return cls.new_s3_client().bind(
            lambda c1: cls.new_s3_resource().map(
                lambda c2: AugmentedS3Client(c1, c2)
            )
        )
