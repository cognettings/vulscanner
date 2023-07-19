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
    attacked_lines: int | None,
    group_name: str,
    comments: str,
    filename: str,
    root_id: str,
) -> dict[str, Any]:
    variables: dict[str, Any] = {
        "comments": comments,
        "filename": filename,
        "groupName": group_name,
        "rootId": root_id,
    }
    if attacked_lines:
        variables["attackedLines"] = attacked_lines
    query: str = """
        mutation UpdateToeLinesAttackedLinesMutation(
            $attackedLines: Int,
            $comments: String!,
            $filename: String!,
            $groupName: String!,
            $rootId: String!
        ) {
            updateToeLinesAttackedLines(
                attackedLines:  $attackedLines,
                groupName: $groupName,
                rootId:  $rootId,
                filename: $filename,
                comments: $comments
            ) {
                success
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": variables,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def query_get(
    *,
    user: str,
    group_name: str,
) -> dict[str, Any]:
    query: str = f"""{{
        group(groupName: "{group_name}"){{
            name
            toeLines {{
                edges {{
                    node {{
                        attackedAt
                        attackedBy
                        attackedLines
                        bePresent
                        bePresentUntil
                        comments
                        lastAuthor
                        filename
                        firstAttackAt
                        loc
                        lastCommit
                        modifiedDate
                        root {{
                            id
                            nickname
                        }}
                        seenAt
                        sortsRiskLevel
                    }}
                    cursor
                }}
                pageInfo {{
                    hasNextPage
                    endCursor
                }}
            }}
        }}
    }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
