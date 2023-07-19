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
) -> dict[str, Any]:
    query: str = f"""{{
        events(groupName: "{group}"){{
            id
            eventStatus
            groupName
            detail
        }}
    }}"""
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_events_query(*, user: str, group: str) -> dict:
    """
    Query for QueryName
    in /front/.../Dashboard/group/queries.ts
    """
    query: str = """
        query GetEventsQuery($groupName: String!) {
          group(groupName: $groupName) {
            events {
              eventStatus
            }
            name
          }
        }
    """
    variables: dict[str, Any] = {
        "groupName": group,
    }
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_events_query_2(*, user: str, group: str) -> dict:
    """
    Query for GetEventsQuery
    in /front/.../GroupEventsView/queries.ts
    """
    query: str = """
        query GetEventsQuery($groupName: String!) {
            group(groupName: $groupName) {
              events {
                eventDate
                detail
                id
                groupName
                eventStatus
                eventType
                closingDate
                root {
                  ... on GitRoot {
                    id
                    nickname
                  }
                  ... on URLRoot {
                    id
                    nickname
                  }
                  ... on IPRoot {
                    id
                    nickname
                  }
                }
              }
              name
            }
        }
    """
    variables: dict[str, Any] = {
        "groupName": group,
    }
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
