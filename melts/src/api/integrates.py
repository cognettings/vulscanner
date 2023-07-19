import aiohttp
import asyncio
from src.constants import (
    API_TOKEN,
)
from src.logger import (
    LOGGER,
)
from typing import (
    Any,
)

INTEGRATES_API_URL = "https://app.fluidattacks.com/api"


async def make_graphql_request(
    url: str, query: str, variables: dict, max_retries: int = 3
) -> dict[str, Any]:
    retry_count = 0
    while retry_count < max_retries:
        try:
            async with aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {API_TOKEN}"}
            ) as session:
                payload = {"query": query, "variables": variables}

                async with session.post(url, json=payload) as response:
                    if response.status == 429:
                        retry_after = int(response.headers["Retry-After"])
                        LOGGER.debug(
                            "Rate limit exceeded. Retrying after %s seconds.",
                            retry_after,
                        )
                        await asyncio.sleep(retry_after)
                        continue
                    data = await response.json()

                    return data
        except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
            retry_count += 1
            print(f"Retry #{retry_count} due to network error.")
            print(exc)

    raise Exception(
        f"Failed to make GraphQL request after {max_retries} retries."
    )


async def get_group_git_roots(group_names: str) -> list[dict[str, Any]]:
    query = """
            query MeltsGetGitRoots($groupName: String!) {
              group(groupName: $groupName){
                roots {
                  ...on GitRoot{
                    id
                    branch
                    lastCloningStatusUpdate
                    nickname
                    gitignore
                    url
                    state
                    cloningStatus {
                        commit
                    }
                    __typename
                  }
                }
              }
            }
        """

    variables = {"groupName": group_names}
    data = await make_graphql_request(INTEGRATES_API_URL, query, variables)
    if not data["data"]["group"]:
        LOGGER.warning("The group %s does not exist", group_names)
        return []

    return data["data"]["group"]["roots"]


async def get_git_root_download_url(
    group_name: str, git_root_id: str
) -> str | None:
    query = """
            query MeltsGetGitRootDownloadUrl($groupName: String!, $rootId: ID!)
            {
              root(groupName: $groupName, rootId: $rootId) {
                ... on GitRoot {
                  id
                  nickname
                  downloadUrl
                }
              }
            }
        """
    params: dict = {"groupName": group_name, "rootId": git_root_id}

    data = await make_graphql_request(INTEGRATES_API_URL, query, params)
    if not data["data"]["root"]:
        LOGGER.warning("The root %s does not exist", git_root_id)
        return None

    return data["data"]["root"]["downloadUrl"]


async def get_git_root_credentials(
    group_name: str, git_root_id: str
) -> dict[str, Any] | None:
    query = """
            query MeltsGetGitRootCredentials($groupName: String!, $rootId: ID!)
            {
              root(groupName: $groupName, rootId: $rootId) {
                ... on GitRoot {
                  id
                  nickname
                  credentials {
                    oauthType
                    user
                    password
                    key
                    token
                    type
                  }
                }
              }
            }
        """
    params: dict = {"groupName": group_name, "rootId": git_root_id}

    data = await make_graphql_request(INTEGRATES_API_URL, query, params)
    if not data["data"]["root"]:
        LOGGER.warning("The root %s does not exist", git_root_id)
        return None

    return data["data"]["root"]["credentials"]


async def get_git_root_upload_url(
    group_name: str, git_root_id: str
) -> str | None:
    query = """
            query MeltsGetGitRootUploadUrl($groupName: String!, $rootId: ID!) {
              root(groupName: $groupName, rootId: $rootId) {
                ... on GitRoot {
                  id
                  nickname
                  uploadUrl
                }
              }
            }
        """
    params: dict = {"groupName": group_name, "rootId": git_root_id}

    data = await make_graphql_request(INTEGRATES_API_URL, query, params)
    if not data["data"]["root"]:
        LOGGER.warning("The root %s does not exist", git_root_id)
        return None

    return data["data"]["root"]["uploadUrl"]


async def update_git_root_cloning_status(
    group_name: str,
    git_root_id: str,
    status: str,
    commit: str | None = None,
    message: str | None = None,
) -> None:
    query = """
            mutation MeltsUpdateRootCloningStatus(
                $groupName: String!
                $rootId: ID!
                $status: CloningStatus!
                $message: String!
                $commit: String
            ) {
              updateRootCloningStatus(
                groupName: $groupName
                id: $rootId
                status: $status
                message: $message
                commit: $commit
              ) {
                success
              }
            }
        """
    params = {
        "groupName": group_name,
        "rootId": git_root_id,
        "status": status,
        "message": message,
        "commit": commit,
    }
    await make_graphql_request(INTEGRATES_API_URL, query, params)
