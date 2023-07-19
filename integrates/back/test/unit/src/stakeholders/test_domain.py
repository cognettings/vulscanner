from dataloaders import (
    Dataloaders,
    get_new_context,
)
import pytest
from stakeholders import (
    domain as stakeholders_domain,
)

pytestmark = [
    pytest.mark.asyncio,
]


async def test_exists() -> None:
    loaders: Dataloaders = get_new_context()
    assert await stakeholders_domain.exists(
        loaders=loaders, email="integratesuser@gmail.com"
    )
    assert not await stakeholders_domain.exists(
        loaders=loaders, email="madeup_stakeholder@void.com"
    )
