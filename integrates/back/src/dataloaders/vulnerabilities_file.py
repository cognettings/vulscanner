from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
import aiofiles
from collections.abc import (
    Iterable,
)
from context import (
    FI_INTEGRATES_CRITERIA_VULNERABILITIES,
)
from dynamodb.types import (
    Item,
)
import yaml


async def _get_vulnerabilities_file() -> Item:
    """Parses the vulns info yaml from the repo into a dictionary."""
    async with aiofiles.open(
        FI_INTEGRATES_CRITERIA_VULNERABILITIES, encoding="utf-8"
    ) as handler:
        return yaml.safe_load(await handler.read())


class VulnerabilitiesFileLoader(DataLoader[str, Item]):
    # pylint: disable=method-hidden
    async def batch_load_fn(self, ids: Iterable[str]) -> list[Item]:
        return list(
            await collect(tuple(_get_vulnerabilities_file() for _ in ids))
        )
