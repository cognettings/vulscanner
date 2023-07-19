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


def get_query() -> str:
    return """
        query(
            $attackedBy: String
            $bePresent: Boolean
            $comments: String
            $fromAttackedAt: DateTime
            $fromBePresentUntil: DateTime
            $fromFirstAttackAt: DateTime
            $fromModifiedDate: DateTime
            $fromSeenAt: DateTime
            $groupName: String!
            $hasVulnerabilities: Boolean
            $lastAuthor: String
            $lastCommit: String
            $maxAttackedLines: Int
            $maxCoverage: Int
            $maxLoc: Int
            $maxSortsRiskLevel: Int
            $minAttackedLines: Int
            $minCoverage: Int
            $minLoc: Int
            $minSortsRiskLevel: Int
            $rootId: ID
            $sort: LinesSortInput
            $toAttackedAt: DateTime
            $toBePresentUntil: DateTime
            $toFirstAttackAt: DateTime
            $toModifiedDate: DateTime
            $toSeenAt: DateTime
        ) {
            group(groupName: $groupName) {
                name
                toeLinesConnection(
                    attackedBy: $attackedBy
                    bePresent: $bePresent
                    comments: $comments
                    fromAttackedAt: $fromAttackedAt
                    fromBePresentUntil: $fromBePresentUntil
                    fromFirstAttackAt: $fromFirstAttackAt
                    fromModifiedDate: $fromModifiedDate
                    fromSeenAt: $fromSeenAt
                    hasVulnerabilities: $hasVulnerabilities
                    lastAuthor: $lastAuthor
                    lastCommit: $lastCommit
                    maxAttackedLines: $maxAttackedLines
                    maxCoverage: $maxCoverage
                    maxLoc: $maxLoc
                    maxSortsRiskLevel: $maxSortsRiskLevel
                    minAttackedLines: $minAttackedLines
                    minCoverage: $minCoverage
                    minLoc: $minLoc
                    minSortsRiskLevel: $minSortsRiskLevel
                    rootId: $rootId
                    sort: $sort
                    toAttackedAt: $toAttackedAt
                    toBePresentUntil: $toBePresentUntil
                    toFirstAttackAt: $toFirstAttackAt
                    toModifiedDate: $toModifiedDate
                    toSeenAt: $toSeenAt
                ) {
                    edges {
                        node {
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
                            root {
                                id
                                nickname
                            }
                            seenAt
                            sortsRiskLevel
                            sortsRiskLevelDate
                            sortsSuggestions {
                                findingTitle
                                probability
                            }
                        }
                        cursor
                    }
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                }
            }
        }
    """


async def get_result(
    *,
    user: str,
    group_name: str,
    variables: dict[str, Any] | None = None,
) -> dict[str, Any]:
    query: str = get_query()
    data: dict[str, Any] = {
        "query": query,
        "variables": {},
    }
    if variables is not None:
        data["variables"] = variables
    data["variables"]["groupName"] = group_name
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
