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
    finding_id: str,
    should_get_zero_risk: bool = False,
) -> dict:
    query: str = f"""
        query {{
            finding(
                identifier: "{finding_id}"
            ){{
                age
                hacker
                attackVectorDescription
                closedVulnerabilities
                consulting {{
                    content
                    created
                    email
                    fullName
                }}
                currentState
                cvssVersion
                description
                draftsConnection @include(
                    if: {str(should_get_zero_risk).lower()}
                ) {{
                    edges {{
                        node {{
                            id
                            state
                        }}
                    }}
                    pageInfo {{
                        endCursor
                        hasNextPage
                    }}
                }}
                evidence {{
                    animation {{
                        date
                        description
                        url
                    }}
                    evidence1 {{
                        date
                        description
                        url
                    }}
                    evidence2 {{
                        date
                        description
                        url
                    }}
                    evidence3 {{
                        date
                        description
                        url
                    }}
                    evidence4 {{
                        date
                        description
                        url
                    }}
                    evidence5 {{
                        date
                        description
                        url
                    }}
                    exploitation {{
                        date
                        description
                        url
                    }}
                }}
                groupName
                id
                isExploitable
                lastStateDate
                lastVulnerability
                maxOpenSeverityScore
                minTimeToRemediate
                observations{{
                    content
                    email
                    fullName
                }}
                openAge
                openVulnerabilities
                recommendation
                records
                rejectedVulnerabilities
                releaseDate
                remediated
                reportDate
                requirements
                severity {{
                    attackComplexity
                    attackVector
                    availabilityImpact
                    availabilityRequirement
                    confidentialityImpact
                    confidentialityRequirement
                    exploitability
                    integrityImpact
                    integrityRequirement
                    modifiedAttackComplexity
                    modifiedAttackVector
                    modifiedAvailabilityImpact
                    modifiedConfidentialityImpact
                    modifiedIntegrityImpact
                    modifiedPrivilegesRequired
                    modifiedSeverityScope
                    modifiedUserInteraction
                    privilegesRequired
                    remediationLevel
                    reportConfidence
                    severityScope
                    userInteraction
                }}
                severityScore
                severityVector
                sorts @include(if: {str(should_get_zero_risk).lower()})
                status
                submittedVulnerabilities
                threat
                title
                tracking {{
                    accepted
                    acceptedUndefined
                    cycle
                    date
                    justification
                    assigned
                    safe
                    vulnerable
                }}
                totalOpenCVSSF
                treatmentSummary {{
                    accepted
                    acceptedUndefined
                    inProgress
                    untreated
                }}
                verificationSummary {{
                    requested
                    onHold
                    verified
                }}
                verified
                vulnerabilitiesConnection {{
                    edges {{
                        node {{
                            id
                            state
                        }}
                    }}
                    pageInfo {{
                        endCursor
                        hasNextPage
                    }}
                }}
                vulnerabilitiesToReattackConnection {{
                    edges {{
                        node {{
                            id
                        }}
                    }}
                    pageInfo {{
                        endCursor
                        hasNextPage
                    }}
                }}
                zeroRiskConnection(
                    state: VULNERABLE
                ) @include(if: {str(should_get_zero_risk).lower()}) {{
                    edges {{
                        node {{
                            id
                            state
                        }}
                    }}
                    pageInfo {{
                        endCursor
                        hasNextPage
                    }}
                }}
                where
                __typename
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


async def get_finding_nzr_vulns(
    *, user: str, finding_id: str, first: int | None = None
) -> dict:
    query: str = """
        query GetFindingNzrVulns(
            $after: String,
            $findingId: String!,
            $first: Int,
            $state: VulnerabilityState
        ) {
            finding(identifier: $findingId) {
                __typename
                id
                vulnerabilitiesConnection(
                    after: $after,
                    first: $first,
                    state: $state
                ) {
                    edges {
                        node {
                            ...vulnFields
                            __typename
                        }
                        __typename
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                        __typename
                    }
                    __typename
                }
            }
        }

        fragment vulnFields on Vulnerability {
            externalBugTrackingSystem
            findingId
            id
            lastStateDate
            lastTreatmentDate
            lastVerificationDate
            remediated
            reportDate
            rootNickname
            severity
            severityTemporalScore
            snippet {
                content
                offset
                __typename
            }
            source
            specific
            state
            stream
            tag
            technique
            treatmentAcceptanceDate
            treatmentAcceptanceStatus
            treatmentAssigned
            treatmentJustification
            treatmentStatus
            treatmentUser
            verification
            vulnerabilityType
            where
            zeroRisk
            __typename
        }
    """
    variables: dict[str, Any] = {"findingId": finding_id, "first": first}
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_finding_vuln_drafts(
    *, user: str, finding_id: str, can_retrieve_drafts: bool
) -> dict:
    """
    Query for GetFindingVulnDrafts
    in front/.../VulnerabilitiesView/queries.ts
    """
    query: str = """
        query GetFindingVulnDrafts(
            $after: String,
            $canRetrieveDrafts: Boolean!,
            $findingId: String!,
            $first: Int
        ) {
            finding(identifier: $findingId) {
                __typename
                id
                draftsConnection(
                    after: $after,
                first: $first) @include(if: $canRetrieveDrafts) {
                    edges {
                        node {
                            ...vulnFields
                            __typename
                        }
                        __typename
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                        __typename
                    }
                    __typename
                }
            }
        }

        fragment vulnFields on Vulnerability {
            externalBugTrackingSystem
            findingId
            id
            lastStateDate
            lastTreatmentDate
            lastVerificationDate
            remediated
            reportDate
            rootNickname
            severity
            severityTemporalScore
            snippet {
                content
                offset
                __typename
            }
            source
            specific
            state
            stream
            tag
            technique
            treatmentAcceptanceDate
            treatmentAcceptanceStatus
            treatmentAssigned
            treatmentJustification
            treatmentStatus
            treatmentUser
            verification
            vulnerabilityType
            where
            zeroRisk
            __typename
        }
    """
    variables: dict[str, Any] = {
        "findingId": finding_id,
        "canRetrieveDrafts": can_retrieve_drafts,
    }
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_finding_zr_vulns(
    *, user: str, finding_id: str, can_retrieve_zero_risk: bool
) -> dict:
    """
    Query for GetFindingZrVulns
    in /front/.../VulnerabilitiesView/queries.ts
    """
    query: str = """
        query GetFindingZrVulns(
          $after: String,
          $canRetrieveZeroRisk: Boolean!,
          $findingId: String!,
          $first: Int) {
          finding(identifier: $findingId) {
            __typename
            id
            zeroRiskConnection(
                after: $after,
                first: $first
              ) @include(if: $canRetrieveZeroRisk) {
              edges {
                node {
                  ...vulnFields
                  __typename
                }
                __typename
              }
              pageInfo {
                endCursor
                hasNextPage
                __typename
              }
              __typename
            }
          }
        }
        fragment vulnFields on Vulnerability {
          externalBugTrackingSystem
          findingId
          id
          lastStateDate
          lastTreatmentDate
          lastVerificationDate
          remediated
          reportDate
          rootNickname
          severity
          severityTemporalScore
          snippet {
            content
            offset
            __typename
          }
          source
          specific
          state
          stream
          tag
          technique
          treatmentAcceptanceDate
          treatmentAcceptanceStatus
          treatmentAssigned
          treatmentJustification
          treatmentStatus
          treatmentUser
          verification
          vulnerabilityType
          where
          zeroRisk
          __typename
        }
    """
    variables: dict[str, Any] = {
        "findingId": finding_id,
        "canRetrieveZeroRisk": can_retrieve_zero_risk,
    }
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_finding_info(*, user: str, finding_id: str) -> dict:
    """
    Query for GetFindingInfo
    in /front/.../VulnerabilitiesView/queries.ts
    """
    query: str = """
        query GetFindingInfo($findingId: String!) {
          finding(identifier: $findingId) {
            id
            remediated
            releaseDate
            status
            totalOpenCVSSF
            verified
          }
        }
    """
    variables: dict[str, Any] = {
        "findingId": finding_id,
    }
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_finding_header(*, user: str, finding_id: str) -> dict:
    """
    Query for GetFindingHeader
    in /common/utils/retrieves/src/queries.ts
    """
    query: str = """
        query GetFindingHeader($findingId: String!) {
            finding(identifier: $findingId) {
                title
            }
       }
    """
    variables: dict[str, Any] = {
        "findingId": finding_id,
    }
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_finding_header_2(*, user: str, finding_id: str) -> dict:
    """
    Query for GetFindingHeader
    in /front/.../Finding-content/queries.ts
    """
    query: str = """
        query GetFindingHeader(
          $findingId: String!
          $canRetrieveHacker: Boolean! = false
        ) {
          finding(identifier: $findingId) {
            closedVulns: closedVulnerabilities
            currentState
            hacker @include(if: $canRetrieveHacker)
            id
            maxOpenSeverityScore
            minTimeToRemediate
            openVulns: openVulnerabilities
            releaseDate
            status
            title
            totalOpenCVSSF
          }
        }
    """
    variables: dict[str, Any] = {
        "findingId": finding_id,
    }
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_finding_title(*, user: str, finding_id: str) -> dict:
    """
    Query for GetFindingTitle
    in /front/.../navbar/breadcrumb/queries.ts
    """
    query: str = """
        query GetFindingTitle($findingId: String!) {
            finding(identifier: $findingId) {
               id
               title
            }
        }
    """
    variables: dict[str, Any] = {
        "findingId": finding_id,
    }
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
