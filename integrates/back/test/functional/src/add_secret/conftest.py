# pylint: disable=import-error
from back.test import (
    db,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_secret")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    return await db.populate(generic_data["db_data"])
