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
@pytest.mark.resolver_test_group("streams_process_findings")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "organizations": generic_data["db_data"]["organizations"],
        "organization_access": generic_data["db_data"]["organization_access"],
        "groups": generic_data["db_data"]["groups"],
        "policies": generic_data["db_data"]["policies"],
        "stakeholders": generic_data["db_data"]["stakeholders"],
    }

    return await db.populate(data)
