# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)


def get_query() -> str:
    return """
        query {
            me {
                draftsConnection {
                    edges {
                        node {
                            currentState
                            groupName
                            hacker
                            id
                            lastStateDate
                            openVulnerabilities
                            reportDate
                            severityScore
                            title
                        }
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
    """


async def get_result(
    *,
    user: str,
) -> dict:
    query: str = get_query()
    data: dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
