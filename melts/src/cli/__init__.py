import asyncclick as click
import asyncio
from contextlib import (
    suppress,
)
import os
from pathlib import (
    Path,
)
from src.cli.commands.clone import (
    clone,
)
from src.cli.commands.fingerprint import (
    get_fingerprint,
)
from src.cli.commands.pull_repos import (
    pull_repos,
)
from src.cli.commands.push_repos import (
    push_repos,
)
from src.logger import (
    LOGGER,
)
import sys


@click.group()
@click.option("--init", default=False, is_flag=True)
async def main(init: bool = False) -> None:
    """Main function for the cli"""
    if init:
        with suppress(FileExistsError):
            os.mkdir("groups")

    current_path = Path(os.getcwd())
    if "groups" not in os.listdir(current_path):
        for parent in current_path.parents:
            if parent.name == "groups":
                os.chdir(parent.parent)
                break
        else:
            LOGGER.error("Could not find groups directory")
            sys.exit("Could not find groups directory")


main.add_command(pull_repos)
main.add_command(clone)
main.add_command(get_fingerprint)
main.add_command(push_repos)


if __name__ == "__main__":
    asyncio.run(main.main())
