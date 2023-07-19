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
    stakeholder: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            removeStakeholderOrganizationAccess(
                organizationId: "{org}",
                userEmail: "{stakeholder}"
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


async def put_access_token(
    *,
    user: str,
    expiration_time: int,
) -> dict[str, Any]:
    query: str = """
        mutation UpdateAccessTokenMutation($expirationTime: Int!) {
            updateAccessToken(expirationTime: $expirationTime) {
                sessionJwt
                success
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "expirationTime": expiration_time,
        },
    }

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_organizations(
    *,
    user: str,
    session_jwt: str,
) -> dict[str, Any]:
    query: str = """
        query GetUserOrganizationsGroups {
            me {
                organizations {
                    groups {
                        name
                        permissions
                        serviceAttributes
                    }
                    name
                }
            }
        }
    """
    data: dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
        session_jwt=session_jwt,
    )
