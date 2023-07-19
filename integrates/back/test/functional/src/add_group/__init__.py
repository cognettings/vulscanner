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
    group: str,
    has_machine: bool = True,
    has_squad: bool = True,
    service: str = "null",
    subscription: str = "CONTINUOUS",
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            addGroup(
                organizationName: "{org}",
                description: "This is a new group from pytest",
                groupName: "{group}",
                service: {service},
                subscription: {subscription},
                hasMachine: {str(has_machine).lower()},
                hasSquad: {str(has_squad).lower()}
            ) {{
            success
            }}
        }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
