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


async def get_group_findings(
    *,
    user: str,
    group: str,
    can_get_rejected_vulns: bool,
    can_get_submitted_vulns: bool,
) -> dict:
    query: str = """
        query GetFindingsQuery(
            $groupName: String!,
            $canGetRejectedVulnerabilities: Boolean!,
            $canGetSubmittedVulnerabilities: Boolean!) {
            group(groupName: $groupName) {
                findings {
                    id
                    rejectedVulnerabilities @include(
                        if: $canGetRejectedVulnerabilities
                    )
                    submittedVulnerabilities @include(
                        if: $canGetSubmittedVulnerabilities
                    )
                }
                name
            }
        }
    """

    data: dict = {
        "query": query,
        "variables": {
            "groupName": group,
            "canGetRejectedVulnerabilities": can_get_rejected_vulns,
            "canGetSubmittedVulnerabilities": can_get_submitted_vulns,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_group_forces(
    *,
    user: str,
    group: str,
    first: int,
    after: list[str] | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
    git_repo: str | None = None,
    strictness: str | None = None,
    status: str | None = None,
    execution_type: str | None = None,
) -> dict:
    query: str = """
        query GetForcesExecutions(
            $after: [String]
            $first: Int
            $fromDate: DateTime
            $gitRepo: String
            $groupName: String!
            $search: String
            $status: String
            $strictness: String
            $toDate: DateTime
            $type: String
        ) {
            group(groupName: $groupName) {
                forcesExecutionsConnection(
                    after: $after
                    first: $first
                    fromDate: $fromDate
                    gitRepo: $gitRepo
                    search: $search
                    status: $status
                    strictness: $strictness
                    toDate: $toDate
                    type: $type
                ) {
                    edges {
                        node {
                            groupName
                            gracePeriod
                            date
                            exitCode
                            gitRepo
                            executionId
                            kind
                            severityThreshold
                            strictness
                            vulnerabilities {
                                numOfAcceptedVulnerabilities
                                numOfOpenVulnerabilities
                                numOfClosedVulnerabilities
                            }
                        }
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                    total
                }
                name
            }
        }
    """

    data: dict = {
        "query": query,
        "variables": {
            "groupName": group,
            "after": after,
            "first": first,
            "fromDate": from_date,
            "toDate": to_date,
            "gitRepo": git_repo,
            "strictness": strictness,
            "status": status,
            "type": execution_type,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_result(
    *,
    user: str,
    group: str,
) -> dict[str, Any]:
    query: str = f"""
        query {{
            group(groupName: "{group}"){{
                analytics(documentName: "", documentType: "")
                forcesToken
                name
                hasSquad
                hasForces
                hasAsm
                hasMachine
                openVulnerabilities
                closedVulnerabilities
                lastClosedVulnerability
                managed
                maxAcceptanceDays
                maxAcceptanceSeverity
                maxNumberAcceptances
                meanRemediate
                meanRemediateCriticalSeverity
                meanRemediateHighSeverity
                meanRemediateLowSeverity
                meanRemediateMediumSeverity
                minAcceptanceSeverity
                minBreakingSeverity
                openFindings
                subscription
                userDeletion
                tags
                description
                serviceAttributes
                organization
                userRole
                maxOpenSeverity
                maxOpenSeverityFinding {{
                    id
                }}
                stakeholders{{
                    email
                }}
                consulting {{
                    content
                }}
                findings(
                    filters: {{
                        verified: false
                    }}
                ) {{
                    id
                }}
                events {{
                    id
                }}
                roots {{
                    ...on GitRoot {{
                        createdAt
                        createdBy
                        id
                        lastEditedAt
                        lastEditedBy
                        vulnerabilities {{
                            id
                        }}
                    }}
                }}
                lastClosedVulnerabilityFinding {{
                    id
                }}
                language
                groupContext
                service
                tier
                businessId
                businessName
                sprintDuration
                sprintStartDate
                vulnerabilityGracePeriod
                vulnerabilities(stateStatus: "open") {{
                    edges {{
                        node {{
                            id
                            state
                            treatmentStatus
                            zeroRisk
                        }}
                    }}
                }}
                forcesVulnerabilities(state: VULNERABLE) {{
                    edges {{
                        node {{
                            id
                            state
                            treatmentStatus
                            zeroRisk
                        }}
                    }}
                }}
                __typename
            }}
        }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_group_vulnerability_drafts(
    *,
    user: str,
    group_name: str,
    state_status: str | None = None,
) -> dict:
    query: str = """
        query GetGroupVulnerabilityDrafts(
            $after: String
            $first: Int
            $groupName: String!
            $stateStatus: String
        ) {
            group(groupName: $groupName) {
                name
                vulnerabilityDrafts(
                    stateStatus: $stateStatus,
                    after: $after,
                    first: $first
                ) {
                    edges {
                        node {
                            where
                            specific
                            state
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

    data: dict = {
        "query": query,
        "variables": {
            "first": 100,
            "groupName": group_name,
            "stateStatus": state_status,
        },
    }

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_forces_vulnerabilities(
    *,
    user: str,
    group_name: str,
    state_status: str | None = None,
) -> dict:
    query: str = """
        query GetForcesVulnerabilities(
            $after: String
            $first: Int
            $groupName: String!
            $stateStatus: VulnerabilityState
        ) {
            group(groupName: $groupName) {
                name
                forcesVulnerabilities(
                    state: $stateStatus,
                    after: $after,
                    first: $first
                ) {
                    edges {
                        node {
                            state
                            treatmentStatus
                            where
                            specific
                            rootNickname
                            zeroRisk
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

    data: dict = {
        "query": query,
        "variables": {
            "first": 100,
            "groupName": group_name,
            "stateStatus": state_status,
        },
    }

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_language_query(
    *,
    user: str,
    group_name: str,
) -> dict:
    query: str = """
        query GetLanguageQuery($groupName: String!) {
            group(groupName: $groupName) {
                name
                language
                __typename
        }}
    """

    data: dict = {
        "query": query,
        "variables": {
            "groupName": group_name,
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
    group_name: str,
) -> dict:
    """
    Query for GetGroupData
    in /front/.../GroupSettingsView/queries.ts
    """
    query: str = """
        query GetGroupData($groupName: String!) {
            group(groupName: $groupName) {
              businessId
              businessName
              description
              hasSquad
              hasMachine
              language
              managed
              name
              service
              sprintDuration
              sprintStartDate
              subscription
              __typename
            }
        }
    """
    variables: dict[str, Any] = {
        "groupName": group_name,
    }
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
