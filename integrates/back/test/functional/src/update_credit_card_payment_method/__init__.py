from back.test.functional.src.utils import (  # pylint: disable=import-error
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
)


async def get_add_result(
    *,
    make_default: bool,
    organization_id: str,
    payment_method_id: str,
    user: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            addCreditCardPaymentMethod(
                organizationId: "{organization_id}",
                makeDefault: {str(make_default).lower()},
                paymentMethodId: "{payment_method_id}"
            ) {{
                success
            }}
        }}
    """
    data: dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_result(
    *,
    payment_method_id: str,
    card_expiration_month: int,
    card_expirations_year: int,
    make_default: bool,
    organization_id: str,
    user: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            updateCreditCardPaymentMethod(
                organizationId: "{organization_id}",
                paymentMethodId: "{payment_method_id}",
                cardExpirationMonth: {card_expiration_month},
                cardExpirationYear: {card_expirations_year},
                makeDefault: {str(make_default).lower()},
            ) {{
                success
            }}
        }}
    """
    data: dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_payment(*, user: str, organization_id: str) -> dict:
    query = """
        query GetOrganizationBilling($organizationId: String!) {
        organization(organizationId: $organizationId) {
            name
            billing {
                paymentMethods {
                    businessName
                    id
                    brand
                    default
                    expirationMonth
                    expirationYear
                    lastFourDigits
                    email
                    country
                    state
                    city
                    rut {
                        fileName
                        modifiedDate
                    }
                    taxId {
                        fileName
                        modifiedDate
                    }
                }
            }
        }
    }
    """

    data = {
        "query": query,
        "variables": {"organizationId": organization_id},
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
