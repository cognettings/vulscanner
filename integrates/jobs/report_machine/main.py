from asyncio import (
    run,
)
from server_async.report_machine import (
    process_execution,
)
import sys


async def main_wrapped() -> None:
    await process_execution(sys.argv[1])


async def main() -> None:
    await main_wrapped()


if __name__ == "__main__":
    run(main())
