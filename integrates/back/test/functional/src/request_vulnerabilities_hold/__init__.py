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
    event: str,
    user: str,
    finding: str,
    vulnerability: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            requestVulnerabilitiesHold(
                eventId: "{event}",
                findingId: "{finding}",
                groupName: "group1",
                vulnerabilities:
                    ["{vulnerability}"]
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
