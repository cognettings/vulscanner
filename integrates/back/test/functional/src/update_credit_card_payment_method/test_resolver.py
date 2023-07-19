from . import (
    get_add_result,
    get_payment,
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.skip(reason="Testing Zoho subscriptions")
@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_credit_card_payment_method")
@pytest.mark.parametrize(
    [
        "updated_card_expiration_month",
        "updated_card_expirations_year",
        "make_default",
        "payment_method_id",
    ],
    [
        [1, 2026, False, "pm_card_visa"],
        [
            12,
            2026,
            False,
            "pm_card_mastercard",
        ],
    ],
)
async def test_update_credit_card_payment_method(
    populate: bool,
    updated_card_expiration_month: int,
    updated_card_expirations_year: int,
    make_default: bool,
    payment_method_id: str,
) -> None:
    assert populate
    user_email = "admin@fluidattacks.com"
    organization_id = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result: dict[str, Any] = await get_add_result(
        make_default=make_default,
        organization_id=organization_id,
        payment_method_id=payment_method_id,
        user=user_email,
    )

    assert "errors" not in result
    assert result["data"]["addCreditCardPaymentMethod"]["success"]
    payment: dict[str, Any] = await get_payment(
        organization_id=organization_id,
        user=user_email,
    )
    payment_id = payment["data"]["organization"]["billing"]["paymentMethods"][
        0
    ]["id"]

    result_update: dict[str, Any] = await get_result(
        payment_method_id=payment_id,
        card_expiration_month=updated_card_expiration_month,
        card_expirations_year=updated_card_expirations_year,
        make_default=make_default,
        organization_id=organization_id,
        user=user_email,
    )
    assert "errors" not in result_update
    assert result_update["data"]["updateCreditCardPaymentMethod"]["success"]
