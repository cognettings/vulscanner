from . import (
    _append,
    _from_s3,
    _recreate,
)
from ._core import (
    CmdContext,
)
import click
from redshift_client.sql_client.connection import (
    Credentials,
    DatabaseId,
)
import sys
from typing import (
    Any,
)


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


main.add_command(_append.only_append)
main.add_command(_from_s3.from_s3)
main.add_command(_recreate.destroy_and_upload)
