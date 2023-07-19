from ._centralize import (
    centralize,
)
from ._core import (
    CmdContext,
    new_sql_client,
    pass_ctx,
)
import click
from dynamo_etl_conf.executor import (
    Executor,
    Job,
)
import logging
from redshift_client.schema.client import (
    SchemaClient,
)
from redshift_client.sql_client.connection import (
    Credentials,
    DatabaseId,
)
import sys
from typing import (
    Any,
    NoReturn,
)

LOG = logging.getLogger(__name__)


@click.command()  # type: ignore[misc]
@click.argument(  # type: ignore[misc]
    "job", type=click.Choice([i.name for i in Job], case_sensitive=False)
)
@pass_ctx  # type: ignore[misc]
def run(ctx: CmdContext, job: str) -> NoReturn:
    Executor(new_sql_client(ctx).map(SchemaClient)).run_job(Job(job)).compute()


@click.group()  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "--db-name",
    envvar="REDSHIFT_DATABASE",
    required=True,
)
@click.option(  # type: ignore[misc]
    "--db-host",
    envvar="REDSHIFT_HOST",
    required=True,
)
@click.option(  # type: ignore[misc]
    "--db-port",
    envvar="REDSHIFT_PORT",
    type=int,
    required=True,
)
@click.option(  # type: ignore[misc]
    "--db-user",
    envvar="REDSHIFT_USER",
    required=True,
)
@click.option(  # type: ignore[misc]
    "--db-passwd",
    envvar="REDSHIFT_PASSWORD",
    required=True,
)
@click.pass_context  # type: ignore[misc]
def main(
    ctx: Any,
    db_name: str,
    db_host: str,
    db_port: int,
    db_user: str,
    db_passwd: str,
) -> None:
    if "--help" not in sys.argv[1:]:
        ctx.obj = CmdContext(  # type: ignore[misc]
            DatabaseId(db_name, db_host, db_port),
            Credentials(db_user, db_passwd),
        )


main.add_command(run)
main.add_command(centralize)
