import click
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
import logging
from redshift_client.sql_client import (
    new_client,
    SqlClient,
)
from redshift_client.sql_client.connection import (
    connect,
    Credentials,
    DatabaseId,
    IsolationLvl,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class CmdContext:
    db_id: DatabaseId
    creds: Credentials


pass_ctx = click.make_pass_decorator(CmdContext)  # type: ignore[misc]


def new_sql_client(ctx: CmdContext) -> Cmd[SqlClient]:
    conn = connect(
        ctx.db_id,
        ctx.creds,
        False,
        IsolationLvl.AUTOCOMMIT,
    )
    return conn.bind(lambda c: new_client(c, LOG))
