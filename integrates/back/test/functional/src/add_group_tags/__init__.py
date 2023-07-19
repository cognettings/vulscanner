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
    group: str,
    tags: list[str],
) -> dict[str, Any]:
    query: str = """
        mutation AddGroupTagsMutation(
            $groupName: String!,
            $tagsData: [String!]
        ) {
            addGroupTags(
                tagsData: $tagsData,
                groupName: $groupName) {
                success
            }
        }
    """
    variables: dict[str, Any] = {
        "groupName": group,
        "tagsData": tags,
    }
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
