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


async def get_result_mutation(
    *,
    user: str,
) -> dict[str, Any]:
    query: str = """
        mutation RemoveStakeholder {
            removeStakeholder {
                success
            }
        }
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_result_me_query(
    *,
    user: str,
    organization_id: str,
) -> dict[str, Any]:
    query: str = """
        query GetUser ($organizationId: String!, $callerOrigin: String!) {
            me(callerOrigin: $callerOrigin) {
                remember
                role
                tags(organizationId: $organizationId) {
                    organization
                }
                __typename
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "callerOrigin": "API",
            "organizationId": organization_id,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_result_stakeholder_query(
    *,
    user: str,
    stakeholder: str,
    group_name: str = "",
    organization_id: str = "",
    entity: str = "GROUP",
) -> dict[str, Any]:
    query: str = """
        query getGroupStakeholder (
            $entity: StakeholderEntity!
            $groupName: String
            $organizationId: String
            $userEmail: String!
        ) {
            stakeholder(
                entity: $entity,
                groupName: $groupName,
                userEmail: $userEmail,
                organizationId: $organizationId
            ) {
                email
                role
                responsibility
                firstLogin
                lastLogin
                groups {
                    name
                }
                __typename
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "entity": entity,
            "groupName": group_name,
            "organizationId": organization_id,
            "userEmail": stakeholder,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
