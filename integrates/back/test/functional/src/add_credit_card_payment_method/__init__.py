from back.test.functional.src.utils import (  # pylint: disable=import-error
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
)


async def get_result(
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
