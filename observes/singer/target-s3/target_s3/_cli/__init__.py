from . import (
    _multifile_conf,
)
import click
from fa_purity import (
    Cmd,
    FrozenDict,
    Maybe,
)
from target_s3._parallel import (
    ThreadPool,
)
from target_s3.executor import (
    Executor,
    MultifileConf,
)
from typing import (
    IO,
    NoReturn,
)
from utils_logger_2 import (
    start_session,
)


@click.command()  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "--bucket", required=True, type=str, help="s3 bucket name"
)
@click.option(  # type: ignore[misc]
    "--prefix", required=True, type=str, help="Prefix for uploaded s3 files"
)
@click.option(  # type: ignore[misc]
    "--str-limit",
    required=False,
    default=-1,
    type=int,
    help="Max number of chars in a str field. Default -1 (no limit)",
)
@click.option(  # type: ignore[misc]
    "--bypass-input",
    is_flag=True,
    type=bool,
    help="std output stream = std input stream",
)
@click.option(  # type: ignore[misc]
    "--threads",
    type=int,
    default=1000,
    help="max number of threads",
)
@click.option(  # type: ignore[misc]
    "--multifile-streams-conf",
    type=click.File("r", "utf-8"),
    help="""
        Encoded `FrozenDict[str, MultifileConf]` as a json
        i.e. `FrozenDict[str, FrozenDict[str, int]]`
        were the key is the target stream name and its value
        is the encoded `MultifileConf` e.g. {'chunks': 2, 'parts': 2}
    """,
    default=None,
)
def main(
    bucket: str,
    prefix: str,
    str_limit: int,
    bypass_input: bool,
    threads: int,
    multifile_streams_conf: IO[str] | None,
) -> NoReturn:
    empty_conf: FrozenDict[str, MultifileConf] = FrozenDict({})
    conf = (
        Maybe.from_optional(multifile_streams_conf)
        .map(lambda f: _multifile_conf.decode_full_conf(f).unwrap())
        .value_or(empty_conf)
    )
    cmd: Cmd[None] = start_session() + ThreadPool.new(threads).bind(
        lambda p: Executor(
            bucket, prefix, str_limit, bypass_input, conf, p
        ).main
    )
    cmd.compute()
