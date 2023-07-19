from billing.types import (
    Subscription,
)
import pytest


@pytest.fixture
def subscription() -> Subscription:
    return Subscription(
        id="si_NzQUjEvnUMty",
        group="testing",
        org_billing_customer="testing@fluidattacks.com",
        organization="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6bd",
        status="active",
        type="MACHINE",
        items={},
    )
