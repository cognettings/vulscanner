from billing import (
    dal as billing_dal,
)
from billing.types import (
    Price,
    Subscription,
)
from custom_exceptions import (
    NoActiveBillingSubscription,
)
from custom_utils import (
    datetime as datetime_utils,
)
from datetime import (
    datetime,
)
from typing import (
    Any,
)

TRIAL_DAYS: int = 21


async def format_create_subscription_data(
    *,
    subscription: str,
    org_billing_customer: str,
    org_name: str,
    group_name: str,
    trial: bool,
) -> dict[str, Any]:
    """Format create subscription session data according to stripe API"""
    prices: dict[str, Price] = await billing_dal.get_prices()
    now: datetime = datetime_utils.get_utc_now()

    result: dict[str, Any] = {
        "customer": org_billing_customer,
        "items": [
            {
                "price": prices["machine"].id,
                "quantity": 1,
                "metadata": {
                    "group": group_name,
                    "name": "machine",
                    "organization": org_name,
                },
            },
        ],
        "metadata": {
            "group": group_name,
            "organization": org_name,
            "subscription": subscription,
        },
    }

    if trial:
        after_trial: datetime = datetime_utils.get_plus_delta(
            now, days=TRIAL_DAYS
        )
        now = after_trial
        result["trial_end"] = int(after_trial.timestamp())

    result["billing_cycle_anchor"] = int(
        datetime_utils.get_first_day_next_month(now).timestamp()
    )

    if subscription == "squad":
        result["items"].append(
            {
                "price": prices["squad"].id,
                "metadata": {
                    "group": group_name,
                    "name": "squad",
                    "organization": org_name,
                },
            },
        )

    return result


def has_subscription(
    *,
    statuses: list[str],
    subscriptions: list[Subscription],
) -> bool:
    for subscription in subscriptions:
        if subscription.status in statuses:
            return True
    return False


def get_active_subscription(
    *,
    subscriptions: list[Subscription],
) -> Subscription | None:
    result: list[Subscription] = [
        subscription
        for subscription in subscriptions
        if subscription.status in ("active", "trialing")
    ]
    if len(result) > 0:
        return result[0]
    return None


async def report_subscription_usage(
    *,
    group_name: str,
    org_billing_customer: str,
) -> bool:
    """Report group squad usage to Stripe"""
    subscriptions: list[
        Subscription
    ] = await billing_dal.get_group_subscriptions(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
        status="active",
    )

    # Raise exception if group does not have an active subscription
    if len(subscriptions) == 0:
        raise NoActiveBillingSubscription()

    return await billing_dal.report_subscription_usage(
        subscription=subscriptions[0],
    )
