from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_other_payment_method")
async def test_update_other_payment_method(
    populate: bool,
) -> None:
    assert populate

    user = "test@fluidattacks.com"
    organization_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    business_name: str = "test business"
    email: str = "test@fluidattacks.com"
    country: str = "Colombia"
    state: str = "Antioquia"
    city: str = "Medellin"

    result: dict[str, Any] = await get_result(
        organization_id=organization_id,
        payment_method_id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
        business_name=business_name,
        email=email,
        country=country,
        state=state,
        city=city,
        user=user,
    )
    assert "errors" not in result
    assert result["data"]["updateOtherPaymentMethod"]["success"]
