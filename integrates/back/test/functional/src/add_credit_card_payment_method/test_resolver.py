from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.skip(reason="Testing Zoho subscriptions")
@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_credit_card_payment_method")
@pytest.mark.parametrize(
    [
        "make_default",
        "payment_method_id",
    ],
    [
        [False, "pm_card_visa"],
        [False, "pm_card_mastercard"],
    ],
)
async def test_add_credit_card_payment_method(
    populate: bool,
    make_default: bool,
    payment_method_id: str,
) -> None:
    assert populate
    user_email = "admin@fluidattacks.com"
    organization_id = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result: dict[str, Any] = await get_result(
        make_default=make_default,
        organization_id=organization_id,
        payment_method_id=payment_method_id,
        user=user_email,
    )
    assert "errors" not in result
    assert result["data"]["addCreditCardPaymentMethod"]["success"]
