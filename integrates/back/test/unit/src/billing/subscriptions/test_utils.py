from back.test.unit.src.utils import (
    get_module_at_test,
)
from billing.subscriptions.utils import (
    report_subscription_usage,
)
from billing.types import (
    Subscription,
)
from custom_exceptions import (
    NoActiveBillingSubscription,
)
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@patch(
    MODULE_AT_TEST + "billing_dal.report_subscription_usage",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "billing_dal.get_group_subscriptions",
    new_callable=AsyncMock,
)
async def test_report_subscription_usage(
    mock_dal_get_group_subscriptions: AsyncMock,
    mock_dal_report_subscription_usage: AsyncMock,
) -> None:
    subscription_test = Subscription(
        id="test_id",
        group="fluid_group",
        org_billing_customer="billing_custumer",
        organization="org_test",
        status="active",
        type="type_test",
        items={"clave": "valor"},
    )

    group_name = "fluid"
    org_billing_customer = "costumer_test"

    mock_dal_get_group_subscriptions.return_value = [subscription_test]
    mock_dal_report_subscription_usage.return_value = True

    result = await report_subscription_usage(
        group_name=group_name, org_billing_customer=org_billing_customer
    )

    assert result == mock_dal_report_subscription_usage.return_value


@patch(
    MODULE_AT_TEST + "billing_dal.get_group_subscriptions",
    new_callable=AsyncMock,
)
async def test_report_subscription_usage_raises_exception(
    mock_dal_get_group_subscriptions: AsyncMock,
) -> None:
    mock_dal_get_group_subscriptions.return_value = []
    group_name = "fluid"
    org_billing_customer = "costumer_test"
    with pytest.raises(NoActiveBillingSubscription):
        await report_subscription_usage(
            group_name=group_name, org_billing_customer=org_billing_customer
        )
