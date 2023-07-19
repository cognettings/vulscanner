from custom_exceptions import (
    PortfolioNotFound,
)
from dataloaders import (
    get_new_context,
)
import pytest
from tags.domain import (
    has_access,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.resolver_test_group("has_access_portfolio")
async def test_has_access_portfolio(*, populate: bool) -> None:
    assert populate
    subject = (
        "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6dbPORTFOLIO#f66-4a2d9748ad6-543"
    )
    assert await has_access(
        loaders=get_new_context(),
        email="admin@gmail.com",
        subject=subject,
    )


@pytest.mark.resolver_test_group("has_access_portfolio")
async def test_has_access_portfolio_not_found(*, populate: bool) -> None:
    assert populate
    subject = (
        "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6dbPORTFOLIO#f66-4a2d9748ad6"
    )
    with pytest.raises(PortfolioNotFound):
        await has_access(
            loaders=get_new_context(),
            email="admin@gmail.com",
            subject=subject,
        )


@pytest.mark.resolver_test_group("has_access_portfolio")
async def test_has_access_portfolio_no_access(*, populate: bool) -> None:
    assert populate
    subject = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6dbf66-4a2d9748ad6"
    assert not await has_access(
        loaders=get_new_context(),
        email="admin@gmail.com",
        subject=subject,
    )
