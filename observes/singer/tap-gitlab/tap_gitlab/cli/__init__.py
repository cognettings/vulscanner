from ._emitter_router import (
    cli_handler,
)
import click
from datetime import (
    timedelta,
)
from fa_purity import (
    Cmd,
    FrozenList,
    Maybe,
)
from tap_gitlab import (
    cleaner,
)
from tap_gitlab.api import (
    Credentials,
)
from tap_gitlab.api.http_json_client import (
    HttpJsonClient,
)
from tap_gitlab.api.project import (
    ProjectId,
)
from tap_gitlab.emitter import (
    SupportedStreams,
)
from typing import (
    NoReturn,
)


@click.command()
@click.option("--api-key", type=str, required=True)
@click.option("--project", type=str, required=True)
@click.option("--threshold", type=int, default=1, help="in hours")
@click.option("--start-page", type=int, default=1)
@click.option("--dry-run", is_flag=True)
def clean_stuck_jobs(
    api_key: str, project: str, threshold: int, start_page: int, dry_run: bool
) -> NoReturn:
    # utility to find and cancel stuck jobs
    creds = Credentials(api_key)
    client = HttpJsonClient.new(creds)
    cmd: Cmd[None] = cleaner.clean_stuck_jobs(
        client,
        ProjectId.from_raw_str(project),
        start_page,
        timedelta(hours=threshold),
        dry_run,
    )
    cmd.compute()


@click.command("stream")
@click.option("--api-key", type=str, required=True)
@click.option("--project", type=str, required=True)
@click.option(
    "--state",
    type=str,
    required=False,
    default=None,
    help="json file S3 URI; e.g. s3://mybucket/folder/state.json",
)
@click.option("--max-pages", type=int, default=1000)
@click.argument(
    "streams",
    type=click.Choice(
        [x.value for x in iter(SupportedStreams)], case_sensitive=False
    ),
    nargs=-1,
)
def stream(
    api_key: str,
    project: str,
    streams: FrozenList[str],
    state: str | None,
    max_pages: int,
) -> NoReturn:
    cli_handler(
        api_key, project, tuple(streams), Maybe.from_optional(state), max_pages
    ).compute()


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(stream)
main.add_command(clean_stuck_jobs)
