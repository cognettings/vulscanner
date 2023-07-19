from back.test.unit.src.utils import (
    get_module_at_test,
)
from billing.dal import (
    _get_subscription_usage,
    _pay_squad_authors_to_date,
    attach_payment_method,
    create_customer,
)
from billing.types import (
    Customer,
    GroupAuthor,
    Price,
    Subscription,
)
from custom_exceptions import (
    CouldNotCreatePaymentMethod,
)
from custom_utils import (
    datetime as datetime_utils,
)
from freezegun import (
    freeze_time,
)
import pytest
from unittest.mock import (
    AsyncMock,
    MagicMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@patch(
    MODULE_AT_TEST + "billing_authors.get_group_authors",
    return_value=(
        GroupAuthor(
            actor="testing",
            commit="04f6b8bcb2d286ee4667f0c90fce479b2545s",
            groups=frozenset(["group1", "group2", "group3"]),
            organization="fluid_org",
            repository="repo_fluid",
        ),
    ),
)
@freeze_time("2020-12-31T18:40:37+00:00")
async def test_get_subscription_usage(
    mock_get_group_authors: AsyncMock,
    subscription: Subscription,
) -> None:
    result: int = await _get_subscription_usage(subscription=subscription)
    assert result == 1
    mock_get_group_authors.assert_awaited_once_with(
        date=datetime_utils.get_utc_now(), group="testing"
    )


@patch(MODULE_AT_TEST + "_get_subscription_usage", return_value=2)
@patch(
    MODULE_AT_TEST + "get_customer",
    return_value=Customer(
        id="b8bcb2d286ee4667f0c90fc",
        name="Jon",
        address=None,
        phone=None,
        email="jon@doe.com",
        default_payment_method="credit card",
    ),
)
@patch(
    MODULE_AT_TEST + "in_thread", return_value=MagicMock(status="succeeded")
)
async def test_pay_squad_authors_to_date(
    mock_in_thread: AsyncMock,
    mock_get_customer: AsyncMock,
    mock_get_subscription_usage: AsyncMock,
    subscription: Subscription,
) -> None:
    _subscription: Subscription = subscription
    assert await _pay_squad_authors_to_date(
        prices={"squad": Price(id="90fce479b25", currency="USD", amount=900)},
        subscription=_subscription,
    )
    mock_in_thread.assert_awaited_once()
    mock_get_customer.assert_awaited_once_with(
        org_billing_customer="testing@fluidattacks.com"
    )
    mock_get_subscription_usage.assert_awaited_once_with(
        subscription=_subscription
    )


@patch(
    MODULE_AT_TEST + "in_thread",
    return_value={"card": {"checks": {"cvc_check": "fail"}}},
)
@patch(
    MODULE_AT_TEST + "remove_payment_method",
    side_effect=None,
)
async def test_attach_payment_method_fails(
    mock_remove_payment_method: AsyncMock,
    mock_in_thread: AsyncMock,
) -> None:
    with pytest.raises(CouldNotCreatePaymentMethod):
        await attach_payment_method(
            payment_method_id="pm_1NDD72eZvKYlo2CkMTDiXDQ",
            org_billing_customer="cus_9s6XBnVi5gbXub",
        )
    mock_in_thread.assert_awaited_once()
    mock_remove_payment_method.assert_called_once_with(
        payment_method_id="pm_1NDD72eZvKYlo2CkMTDiXDQ"
    )


@patch(
    MODULE_AT_TEST + "in_thread",
    return_value=Customer(
        id="b8bcb2d286ee4667f0c90fc",
        name="Jon",
        address=None,
        phone=None,
        email="jon@doe.com",
        default_payment_method="credit card",
    ),
)
@patch(
    MODULE_AT_TEST + "orgs_domain.update_billing_customer",
    side_effect=None,
)
async def test_create_customer(
    mock_update_billing_customer: AsyncMock,
    mock_in_thread: AsyncMock,
) -> None:
    expected_result = Customer(
        id="b8bcb2d286ee4667f0c90fc",
        name="Jon",
        address=None,
        email="jon@doe.com",
        phone=None,
        default_payment_method=None,
    )
    assert (
        await create_customer(
            org_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6bd",
            org_name="testing",
            user_email="jon@doe.com",
        )
        == expected_result
    )
    mock_in_thread.assert_awaited_once()
    mock_update_billing_customer.assert_awaited_once_with(
        organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6bd",
        organization_name="testing",
        billing_customer="b8bcb2d286ee4667f0c90fc",
    )
