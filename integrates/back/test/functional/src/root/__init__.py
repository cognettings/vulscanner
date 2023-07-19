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


async def get_root_way1(
    *,
    group: str,
    user: str,
) -> dict[str, Any]:
    """Query for GetRoot in /front/.../GroupFindingsView/queries.ts"""
    query: str = """
        query GetRoots($groupName: String!) {
          group(groupName: $groupName) {
            name
            roots {
              ... on GitRoot {
                id
                nickname
                state
                __typename
              }
              ... on IPRoot {
                id
                nickname
                state
                __typename
              }
              ... on URLRoot {
                id
                nickname
                state
                __typename
              }
              __typename
            }
            __typename
          }
        }
    """
    variables: dict[str, Any] = {"groupName": group}
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_root_way2(
    *,
    group: str,
    user: str,
) -> dict[str, Any]:
    """Query for GetRoot in /front/.../GroupScopeView/queries.ts"""
    query: str = """
        query GetRoots($groupName: String!) {
            group(groupName: $groupName) {
              name
              roots {
                ... on GitRoot {
                  branch
                  cloningStatus {
                    message
                    status
                    __typename
                  }
                  credentials {
                    id
                    isToken
                    name
                    type
                    __typename
                  }
                  environment
                  gitEnvironmentUrls {
                    url
                    id
                    createdAt
                    createdBy
                    urlType
                    __typename
                  }
                  gitignore
                  id
                  includesHealthCheck
                  nickname
                  state
                  url
                  useVpn
                  createdAt
                  createdBy
                  lastEditedAt
                  lastEditedBy
                  __typename
                }
                ... on IPRoot {
                  address
                  id
                  nickname
                  state
                  __typename
                }
                ... on URLRoot {
                  host
                  id
                  nickname
                  path
                  port
                  protocol
                  query
                  state
                  __typename
                }
                __typename
              }
              __typename
            }
       }
    """
    variables: dict[str, Any] = {"groupName": group}
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_root_way3(
    *,
    group: str,
    user: str,
) -> dict[str, Any]:
    """Query for GetRoot in front/.../MachineView/queries.ts"""
    query: str = """
        query GetRoots($groupName: String!) {
            group(groupName: $groupName) {
              name
              roots {
                ... on GitRoot {
                  nickname
                  state
                  __typename
                }
                __typename
              }
              __typename
            }
        }
    """
    variables: dict[str, Any] = {"groupName": group}
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
