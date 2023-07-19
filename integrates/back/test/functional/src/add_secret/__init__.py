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
    key: str,
    value: str,
    group_name: str,
    root_id: str,
    description: str,
) -> dict[str, Any]:
    query: str = """
        mutation AddSecret (
            $rootId: ID!
            $key: String!
            $value: String!
            $groupName: String!
            $description: String
        ) {
        addSecret(
                rootId: $rootId
                key: $key
                value: $value
                groupName: $groupName
                description: $description
                ) {
            success
        }
      }
    """

    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "rootId": root_id,
            "key": key,
            "value": value,
            "groupName": group_name,
            "description": description,
        },
    }

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
