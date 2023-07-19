# pylint: disable=import-error
from back.test.functional.src.utils import (
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
    user: str,
    org: str,
    email: str,
    role: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            updateOrganizationStakeholder(
                organizationId: "{org}"
                userEmail: "{email}"
                role: {role}
            ) {{
                success
                modifiedStakeholder {{
                    email
                }}
            }}
        }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
