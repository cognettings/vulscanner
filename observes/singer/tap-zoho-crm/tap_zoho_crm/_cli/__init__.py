from . import (
    _decode,
)
import click
from fa_purity import (
    Cmd,
)
from tap_zoho_crm import (
    etl,
)
from tap_zoho_crm.api.auth import (
    AuthApiFactory,
    Credentials,
)
from typing import (
    IO,
    NoReturn,
)


@click.command()  # type: ignore[misc]
@click.argument("crm_auth_file", type=click.File("r", "utf-8"))  # type: ignore[misc]
def gen_refresh_token(crm_auth_file: IO[str]) -> NoReturn:
    # Manual refresh token generation, see:
    # https://www.zoho.com/crm/developer/docs/api/v2/auth-request.html
    creds = _decode.decode_zoho_creds(crm_auth_file).unwrap()
    cmd: Cmd[None] = AuthApiFactory.auth_api(
        creds
    ).manual_new_refresh_token.map(print)
    cmd.compute()


@click.command()  # type: ignore[misc]
def revoke_token() -> NoReturn:
    # Manual refresh token revoke
    fake_creds = Credentials("", "", "", frozenset())
    cmd: Cmd[None] = AuthApiFactory.auth_api(
        fake_creds
    ).manual_revoke_token.map(print)
    cmd.compute()


@click.command()  # type: ignore[misc]
@click.argument("db_auth_file", type=click.File("r", "utf-8"))  # type: ignore[misc]
def init_db(db_auth_file: IO[str]) -> NoReturn:
    db_id, db_creds = _decode.decode_db_conf(db_auth_file).unwrap()
    cmd: Cmd[None] = etl.initialize(db_id, db_creds)
    cmd.compute()


@click.command()  # type: ignore[misc]
@click.argument("crm_auth_file", type=click.File("r", "utf-8"))  # type: ignore[misc]
@click.argument("db_auth_file", type=click.File("r", "utf-8"))  # type: ignore[misc]
def create_jobs(crm_auth_file: IO[str], db_auth_file: IO[str]) -> NoReturn:
    crm_creds = _decode.decode_zoho_creds(crm_auth_file).unwrap()
    db_id, db_creds = _decode.decode_db_conf(db_auth_file).unwrap()
    cmd: Cmd[None] = etl.creation_phase(crm_creds, db_id, db_creds)
    cmd.compute()


@click.command()  # type: ignore[misc]
@click.argument("crm_auth_file", type=click.File("r", "utf-8"))  # type: ignore[misc]
@click.argument("db_auth_file", type=click.File("r", "utf-8"))  # type: ignore[misc]
def stream(crm_auth_file: IO[str], db_auth_file: IO[str]) -> NoReturn:
    crm_creds = _decode.decode_zoho_creds(crm_auth_file).unwrap()
    db_id, db_creds = _decode.decode_db_conf(db_auth_file).unwrap()
    cmd: Cmd[None] = etl.start_streamer(crm_creds, db_id, db_creds)
    cmd.compute()


@click.group()  # type: ignore[misc]
def main() -> None:  # decorator make it to return `NoReturn`
    # cli group entrypoint
    pass


main.add_command(create_jobs)
main.add_command(gen_refresh_token)
main.add_command(init_db)
main.add_command(revoke_token)
main.add_command(stream)
