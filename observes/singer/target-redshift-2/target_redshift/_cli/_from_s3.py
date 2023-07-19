from ._core import (
    CmdContext,
    pass_ctx,
)
import click
from fa_purity import (
    Cmd,
    Maybe,
)
from redshift_client.core.id_objs import (
    Identifier,
    SchemaId,
)
from target_redshift._utils import (
    ThreadPool,
)
from target_redshift.executor import (
    FromS3Executor,
)
from typing import (
    NoReturn,
)


@click.command()  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "--bucket",
    type=str,
    required=True,
    help="S3 bucket name",
)
@click.option(  # type: ignore[misc]
    "--prefix",
    type=str,
    required=True,
    help="S3 target files prefix",
)
@click.option(  # type: ignore[misc]
    "--role",
    type=str,
    required=True,
    help="arn of an iam role for S3 access",
)
@click.option(  # type: ignore[misc]
    "--schema-name",
    type=str,
    required=True,
    help="Schema name in your warehouse",
)
# -- Optional --
@click.option(  # type: ignore[misc]
    "--ignore-failed",
    type=bool,
    is_flag=True,
    help="ignore json items that does not decode to a singer message",
)
@click.option(  # type: ignore[misc]
    "--threads",
    type=int,
    required=False,
    default=1000,
    help="max number of threads",
)
@click.option(  # type: ignore[misc]
    "--wlm-queue",
    type=str,
    required=False,
    default=None,
    help="redshift wlm queue group for the executed queries",
)
@pass_ctx  # type: ignore[misc]
def from_s3(
    ctx: CmdContext,
    bucket: str,
    prefix: str,
    role: str,
    schema_name: str,
    threads: int,
    ignore_failed: bool,
    wlm_queue: str | None,
) -> NoReturn:
    pool = ThreadPool.new(threads)
    executor = pool.map(
        lambda p: FromS3Executor(
            ctx.db_id,
            ctx.creds,
            SchemaId(Identifier.new(schema_name)),
            bucket,
            prefix,
            role,
            ignore_failed,
            Maybe.from_optional(wlm_queue),
            p,
        )
    )
    cmd: Cmd[None] = executor.bind(lambda e: e.execute())
    cmd.compute()
