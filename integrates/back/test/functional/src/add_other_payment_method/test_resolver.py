from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_other_payment_method")
async def test_add_other_payment_method(
    populate: bool,
) -> None:
    assert populate

    user = "admin@fluidattacks.com"
    organization_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    business_name: str = "test business"
    email: str = "test@test.com"
    country: str = "Colombia"
    state: str = "Antioquia"
    city: str = "Medellin"

    result: dict[str, Any] = await get_result(
        organization_id=organization_id,
        business_name=business_name,
        email=email,
        country=country,
        state=state,
        city=city,
        user=user,
    )
    assert "errors" not in result
    assert result["data"]["addOtherPaymentMethod"]["success"]
