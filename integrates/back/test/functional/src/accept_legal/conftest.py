# pylint: disable=import-error
from back.test import (
    db,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("accept_legal")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "stakeholders": [
            Stakeholder(
                email="admin@gmail.com",
                legal_remember=True,
                is_registered=True,
            ),
            Stakeholder(
                email="hacker@gmail.com",
                legal_remember=True,
                is_registered=True,
            ),
            Stakeholder(
                email="reattacker@gmail.com",
                legal_remember=True,
                is_registered=True,
            ),
            Stakeholder(
                email="user@gmail.com",
                legal_remember=True,
                is_registered=True,
            ),
            Stakeholder(
                email="user_manager@gmail.com",
                legal_remember=True,
                is_registered=True,
            ),
            Stakeholder(
                email="vulnerability_manager@gmail.com",
                legal_remember=True,
                is_registered=True,
            ),
            Stakeholder(
                email="resourcer@gmail.com",
                legal_remember=True,
                is_registered=True,
            ),
            Stakeholder(
                email="reviewer@gmail.com",
                legal_remember=True,
                is_registered=True,
            ),
            Stakeholder(
                email="service_forces@gmail.com",
                legal_remember=True,
                is_registered=True,
            ),
            Stakeholder(
                email="customer_manager@gmail.com",
                legal_remember=True,
                is_registered=True,
            ),
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
