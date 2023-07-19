# pylint: disable=import-outside-toplevel
from aioextensions import (
    run,
)
import click
import ctx
from ctx import (
    LEGAL,
)
from functools import (
    partial,
)
import logging
import sys
import textwrap
from time import (
    time,
)
from utils.bugs import (
    add_bugsnag_data,
    initialize_bugsnag,
)
from utils.env import (
    guess_environment,
)
from utils.function import (
    shield_blocking,
)
from utils.logs import (
    log_blocking,
    log_to_remote_blocking,
    set_level,
)

# Reusable components
CONFIG_PATH = partial(
    click.argument,
    "config_path",
    type=click.Path(
        allow_dash=False,
        dir_okay=False,
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
    ),
)
STRICT_RUN = False


@click.group(
    help="Deterministic vulnerability analysis and reporting tool.",
    epilog=textwrap.dedent(
        f"""
            For legal information read {LEGAL}
        """
    ),
)
@click.option(
    "--strict",
    help="Enable strict mode.",
    is_flag=True,
)
def cli(
    strict: bool,
) -> None:
    # pylint: disable=global-statement
    global STRICT_RUN
    STRICT_RUN = strict


@cli.command(help="Perform vulnerability detection.", name="scan")
@CONFIG_PATH()
def cli_scan(
    config_path: str,
) -> None:
    start_time: float = time()
    success: tuple[bool, int] = cli_scan_wrapped(config_path=config_path)

    if guess_environment() == "production" and not success:
        log_to_remote_blocking(
            execution_seconds=f"{time() - start_time}",
            msg="Failure",
            severity="error",
        )

    if not success[0]:
        log_blocking(
            "info",
            "Summary: An error ocurred while trying to analyze your targets.",
        )
        sys.exit(1)
    elif success[1] > 0:
        log_blocking(
            "info",
            "Summary: %s vulnerabilities were found in your targets.",
            success[1],
        )
        if ctx.SKIMS_CONFIG.strict or STRICT_RUN:
            sys.exit(1)
        else:
            sys.exit(0)
    else:
        log_blocking(
            "info", "Summary: No vulnerabilities were found in your targets."
        )
        sys.exit(0)


@shield_blocking(on_error_return=(False, 0))
def cli_scan_wrapped(
    config_path: str,
) -> tuple[bool, int]:
    from config import (
        load,
    )
    import core.scan

    ctx.SKIMS_CONFIG = load(config_path)

    initialize_bugsnag()
    add_bugsnag_data(config=config_path)

    if ctx.SKIMS_CONFIG.debug:
        set_level(logging.DEBUG)
    success: tuple[bool, int] = run(core.scan.main())

    return success


if __name__ == "__main__":
    cli(  # pylint: disable=no-value-for-parameter
        prog_name="skims",
    )
