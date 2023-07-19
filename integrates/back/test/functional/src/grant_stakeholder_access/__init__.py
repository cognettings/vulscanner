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
    stakeholder: str,
    group: str,
    responsibility: str,
    role: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            grantStakeholderAccess (
                email: "{stakeholder}"
                groupName: "{group}"
                responsibility: "{responsibility}"
                role: {role}
            ) {{
            success
                grantedStakeholder {{
                    email
                }}
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


async def get_stakeholders(
    *,
    user: str,
    group: str,
) -> dict[str, Any]:
    query: str = """
        query GetStakeholders($groupName: String!) {
            group (groupName: $groupName) {
                stakeholders {
                    email
                    invitationState
                }
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "groupName": group,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_group_data(
    *,
    user: str,
    group: str,
) -> dict[str, Any]:
    query: str = """
        query GetGroupVulns($after: String, $first: Int, $group: String!) {
            group(groupName: $group) {
                name
                vulnerabilities(
                    after: $after,
                    first: $first,
                    stateStatus: "SAFE"
                ) {
                    edges {
                        node {
                            state
                            zeroRisk
                        }
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                    total
                }
            }
        }
    """

    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "group": group,
            "first": 150,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
