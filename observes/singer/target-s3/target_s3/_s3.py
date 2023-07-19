import boto3
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from mypy_boto3_s3.client import (
    S3Client,
)


def new_client() -> Cmd[S3Client]:
    return Cmd.from_cmd(lambda: boto3.client("s3"))


@dataclass(frozen=True)
class S3URI:
    bucket: str
    file_obj: str

    @property
    def uri(self) -> str:
        return f"s3://{self.bucket}/{self.file_obj}"
