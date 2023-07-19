# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)


async def get_result(
    *,
    user: str,
    expiration_time: int,
    name: str,
) -> dict:
    query = """
        mutation AddAccessToken($expirationTime: Int!, $name: String!) {
            addAccessToken(expirationTime: $expirationTime, name: $name) {
                sessionJwt
                success
                __typename
            }
        }
    """
    data = {
        "query": query,
        "variables": {"expirationTime": expiration_time, "name": name},
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_me_data(
    *,
    user: str,
    session_jwt: str,
) -> dict:
    query = """
        query GetMeData {
            me {
                permissions
                role
            }
        }
    """
    data = {"query": query}

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
        session_jwt=session_jwt,
    )


async def get_me_access_token(
    *,
    user: str,
) -> dict:
    query = """
        query GetMeData {
            me {
                accessToken
                accessTokens {
                    __typename
                    id
                    name
                    issuedAt
                    lastUse
                }
            }
        }
    """
    data = {"query": query}

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
