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
    "--persistent-tables",
    type=str,
    required=False,
    default=None,
    help="set of table names (separated by comma) that would not be recreated but will also receive new data",
)
@click.option(  # type: ignore[misc]
    "--wlm-queue",
    type=str,
    required=False,
    default=None,
    help="redshift wlm queue group for the executed queries",
)
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
def destroy_and_upload(
    ctx: CmdContext,
    schema_name: str,
    records_limit: int,
    records_per_query: int,
    s3_state: Optional[str],
    threads: int,
    persistent_tables: Optional[str],
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
    persistent = (
        Maybe.from_optional(persistent_tables)
        .map(lambda raw: frozenset(raw.split(",")))
        .bind_optional(lambda f: f if f else None)
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
            lambda c, t: Coproduct.inl(
                persistent.map(
                    lambda pt: Strategies.recreate_per_stream(c, t, pt)
                ).value_or(Strategies.recreate_all_schema(c, t))
            ),
            p,
        )
    )
    cmd: Cmd[None] = executor.bind(lambda e: e.execute())
    cmd.compute()
