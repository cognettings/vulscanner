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
    *, user: str, event_id: str, comments: str
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            requestEventVerification(
                eventId: "{event_id}"
                comments: "{comments}"
                groupName: "group1"
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
