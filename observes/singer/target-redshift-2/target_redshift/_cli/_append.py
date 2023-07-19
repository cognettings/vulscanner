from ._core import (
    CmdContext,
    pass_ctx,
)
import click
from fa_purity import (
    Cmd,
    Maybe,
)
from fa_purity.union import (
    Coproduct,
)
from redshift_client.core.id_objs import (
    Identifier,
    SchemaId,
)
from target_redshift._s3 import (
    S3URI,
)
from target_redshift._utils import (
    ThreadPool,
)
from target_redshift.executor import (
    GenericExecutor,
)
from target_redshift.loader import (
    SingerHandlerOptions,
)
from target_redshift.strategy import (
    Strategies,
)
from typing import (
    NoReturn,
    Optional,
)


@click.command()  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "-s",
    "--schema-name",
    type=str,
    required=True,
    help="Schema name in your warehouse",
)
# -- Optional --
@click.option(  # type: ignore[misc]
    "--records-limit",
    type=int,
    required=False,
    default=1000000,
    help="Max # of records per group",
)
@click.option(  # type: ignore[misc]
    "--records-per-query",
    type=int,
    required=False,
    default=1000,
    help="Max # of records per sql query",
)
@click.option(  # type: ignore[misc]
    "--s3-state",
    type=str,
    required=False,
    default=None,
    help="S3 file obj URI to upload the state; e.g. s3://mybucket/folder/state.json",
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
# -- Flags --
@click.option(  # type: ignore[misc]
    "--ignore-failed",
    type=bool,
    is_flag=True,
    help="ignore json items that does not decode to a singer message",
)
@click.option(  # type: ignore[misc]
    "--truncate",
    type=bool,
    is_flag=True,
    help="Truncate records that exceed column size?",
)
@pass_ctx  # type: ignore[misc]
def only_append(
    ctx: CmdContext,
    schema_name: str,
    records_limit: int,
    records_per_query: int,
    s3_state: Optional[str],
    threads: int,
    wlm_queue: str | None,
    ignore_failed: bool,
    truncate: bool,
) -> NoReturn:
    target = SchemaId(Identifier.new(schema_name))
    options = SingerHandlerOptions(
        truncate,
        records_per_query,
    )
    state = (
        Maybe.from_optional(s3_state)
        .map(S3URI.from_raw)
        .map(lambda r: r.unwrap())
    )
    pool = ThreadPool.new(threads)

    executor = pool.map(
        lambda p: GenericExecutor(
            ctx.db_id,
            ctx.creds,
            target,
            options,
            records_limit,
            state,
            Maybe.from_optional(wlm_queue),
            ignore_failed,
            lambda c, t: Coproduct.inr(Strategies.only_append(c, t, True)),
            p,
        )
    )
    cmd: Cmd[None] = executor.bind(lambda e: e.execute())
    cmd.compute()
