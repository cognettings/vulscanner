from billing import (
    dal as billing_dal,
    domain as billing_domain,
)
from billing.subscriptions import (
    utils as subs_utils,
)
from billing.types import (
    Subscription,
)
from custom_exceptions import (
    BillingCustomerHasNoPaymentMethod,
    BillingSubscriptionSameActive,
    CouldNotUpdateSubscription,
    InvalidBillingCustomer,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


async def update_subscription(
    *,
    subscription: str,
    org_billing_customer: str | None,
    org_name: str,
    group_name: str,
) -> bool:
    """Update a subscription for a group"""
    # Raise exception if stripe customer does not exist
    if org_billing_customer is None:
        raise InvalidBillingCustomer()

    # Raise exception if customer does not have a payment method
    if not await billing_domain.customer_has_payment_method(
        org_billing_customer=org_billing_customer,
    ):
        raise BillingCustomerHasNoPaymentMethod()

    subscriptions: list[
        Subscription
    ] = await billing_dal.get_group_subscriptions(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
        status="all",
    )

    # Raise exception if group has incomplete, past_due or unpaid subscriptions
    if subs_utils.has_subscription(
        statuses=["incomplete", "past_due", "unpaid"],
        subscriptions=subscriptions,
    ):
        raise CouldNotUpdateSubscription()

    current: Subscription | None = subs_utils.get_active_subscription(
        subscriptions=subscriptions
    )

    # Raise exception if group already has the same subscription active
    is_free: bool = current is None and subscription == "free"
    is_other: bool = current is not None and current.type == subscription
    if is_free or is_other:
        raise BillingSubscriptionSameActive()

    result: bool = False
    if current is None:
        trial: bool = not subs_utils.has_subscription(
            statuses=["canceled"],
            subscriptions=subscriptions,
        )
        data: dict[
            str, Any
        ] = await subs_utils.format_create_subscription_data(
            subscription=subscription,
            org_billing_customer=org_billing_customer,
            org_name=org_name,
            group_name=group_name,
            trial=trial,
        )
        result = await billing_dal.create_subscription(**data)
    elif subscription != "free":
        result = await billing_dal.update_subscription(
            subscription=current,
            upgrade=current.type == "machine" and subscription == "squad",
        )
    else:
        result = await billing_dal.remove_subscription(
            subscription_id=current.id,
            invoice_now=current.type == "squad",
            prorate=True,
        )

    if not result:
        raise CouldNotUpdateSubscription()
    return result
