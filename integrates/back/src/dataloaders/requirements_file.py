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
    FI_INTEGRATES_CRITERIA_REQUIREMENTS,
)
from dynamodb.types import (
    Item,
)
import yaml


async def _get_requirements_file() -> Item:
    """Parses the requirements info yaml from the repo into a dictionary."""
    async with aiofiles.open(
        FI_INTEGRATES_CRITERIA_REQUIREMENTS, encoding="utf-8"
    ) as handler:
        return yaml.safe_load(await handler.read())


class RequirementsFileLoader(DataLoader[str, Item]):
    # pylint: disable=method-hidden
    async def batch_load_fn(self, ids: Iterable[str]) -> list[Item]:
        return list(
            await collect(tuple(_get_requirements_file() for _ in ids))
        )
