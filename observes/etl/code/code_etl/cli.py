from ._utils import (
    Date,
)
import click
from code_etl import (
    amend,
    upload_repo,
)
from code_etl.arm import (
    ArmClient,
    ArmToken,
)
from code_etl.client import (
    Tables,
)
from code_etl.compute_bills import (
    main as bill_reports,
)
from code_etl.init_tables import (
    init_tables,
)
from code_etl.mailmap import (
    Mailmap,
    MailmapFactory,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from fa_purity.cmd import (
    unsafe_unwrap,
)
from fa_purity.maybe import (
    Maybe,
)
from os.path import (
    abspath,
)
from pathlib import (
    Path,
)
from redshift_client.sql_client.connection import (
    Credentials,
    DatabaseId,
)
import sys
from typing import (
    Any,
    NoReturn,
    Optional,
    Tuple,
)
from utils_logger_2 import (
    start_session,
)


@dataclass(frozen=True)
class CmdContext:
    db_id: DatabaseId
    creds: Credentials


mailmap_file = click.Path(
    exists=True,
    file_okay=True,
    dir_okay=False,
    writable=False,
    readable=True,
    resolve_path=True,
    allow_dash=False,
    path_type=str,
)
pass_ctx = click.make_pass_decorator(CmdContext)  # type: ignore[misc]


def _get_mailmap(path: Optional[str]) -> Maybe[Mailmap]:
    return Maybe.from_optional(path).map(MailmapFactory.from_file_path)


@click.command()  # type: ignore[misc]
@click.option("--mailmap", type=mailmap_file)  # type: ignore[misc]
@click.option("--namespace", type=str, required=True)  # type: ignore[misc]
@click.pass_obj  # type: ignore[misc]
def amend_authors(
    ctx: CmdContext,
    mailmap: Optional[str],
    namespace: str,
) -> NoReturn:
    cmd: Cmd[None] = amend.amend_users(
        ctx.db_id,
        ctx.creds,
        namespace,
        _get_mailmap(mailmap),
    )
    cmd.compute()


@click.command()  # type: ignore[misc]
@click.option("--namespace", type=str, required=True)  # type: ignore[misc]
@click.pass_obj  # type: ignore[misc]
def re_calc_hash(
    ctx: CmdContext,
    namespace: str,
) -> NoReturn:
    cmd: Cmd[None] = amend.re_calc_fa_hash(
        ctx.db_id,
        ctx.creds,
        namespace,
    )
    cmd.compute()


@click.command()  # type: ignore[misc]
@click.argument("folder", type=str)  # type: ignore[misc]
@click.argument("year", type=int)  # type: ignore[misc]
@click.argument("month", type=int)  # type: ignore[misc]
@click.argument("integrates_token", type=str)  # type: ignore[misc]
def compute_bills(
    folder: str, year: int, month: int, integrates_token: str
) -> NoReturn:
    token = ArmToken.new(integrates_token)
    cmd: Cmd[None] = ArmClient.new(token).bind(
        lambda c: bill_reports(
            c, Path(folder), Date.new(year, month, 1).unwrap()
        )
    )
    cmd.compute()


@click.command()  # type: ignore[misc]
@click.option("--namespace", type=str, required=True)  # type: ignore[misc]
@click.option("--arm-token", type=str, required=True)  # type: ignore[misc]
@click.option("--mailmap", type=mailmap_file)  # type: ignore[misc]
@click.argument("repositories", type=str, nargs=-1)  # type: ignore[misc]
@pass_ctx  # type: ignore[misc]
def upload_code(
    ctx: CmdContext,
    namespace: str,
    arm_token: str,
    repositories: Tuple[str, ...],
    mailmap: Optional[str],
) -> NoReturn:
    # pylint: disable=too-many-arguments
    repos = tuple(Path(abspath(r)) for r in repositories)
    token = ArmToken.new(arm_token)
    upload_repo.upload_repos(
        ctx.db_id, ctx.creds, token, namespace, repos, _get_mailmap(mailmap)
    ).compute()


@click.group()  # type: ignore[misc]
def migration() -> None:
    # migration cli group
    pass


@click.command()  # type: ignore[misc]
@click.option(
    "--table",
    type=click.Choice([i.name for i in Tables], case_sensitive=False),
    required=True,
)  # type: ignore[misc]
@pass_ctx  # type: ignore[misc]
def init_table(
    ctx: CmdContext,
    table: str,
) -> NoReturn:
    # pylint: disable=too-many-arguments
    init_tables(
        ctx.db_id, ctx.creds, Tables.from_raw(table).unwrap()
    ).compute()


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
    unsafe_unwrap(start_session())
    if "--help" not in sys.argv[1:]:
        ctx.obj = CmdContext(  # type: ignore[misc]
            DatabaseId(db_name, db_host, db_port),
            Credentials(db_user, db_passwd),
        )


main.add_command(amend_authors)
main.add_command(compute_bills)
main.add_command(init_table)
main.add_command(re_calc_hash)
main.add_command(upload_code)
main.add_command(migration)
