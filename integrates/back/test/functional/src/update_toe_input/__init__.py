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
    be_present: bool,
    component: str,
    entry_point: str,
    group_name: str,
    root_id: str,
    user: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            updateToeInput(
                bePresent: {str(be_present).lower()},
                component: "{component}",
                groupName: "{group_name}",
                rootId: "{root_id}",
                entryPoint: "{entry_point}",
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
