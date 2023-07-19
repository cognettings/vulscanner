import click
from fa_purity.cmd import (
    Cmd,
)
import sys
from tap_csv import (
    receiver,
)
from typing import (
    IO,
    NoReturn,
)


@click.command()  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "--tap-input", help="tap inputs", type=click.File("r"), default=sys.stdin
)
def main(tap_input: IO[str]) -> NoReturn:
    cmd: Cmd[None] = receiver.process_file(tap_input)
    cmd.compute()
