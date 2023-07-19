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
    org_id: str,
) -> dict[str, Any]:
    query: str = f"""{{
        me(callerOrigin: "API") {{
            accessToken
            callerOrigin
            credentials {{
                azureOrganization
                isPat
                key
                isToken
                name
                oauthType
                password
                owner
                organization {{id}}
                user
                token
                type
            }}
            enrolled
            isConcurrentSession
            notificationsPreferences{{
                email
            }}
            organizations {{
                name
                groups {{
                    hasForces
                    hasSquad
                    name
                }}
            }}
            phone{{
                callingCountryCode
                countryCode
                nationalNumber
            }}
            pendingEvents{{
                eventDate
                detail
                id
                groupName
                eventStatus
                eventType
            }}
            permissions
            remember
            role
            sessionExpiration
            tags(organizationId: "{org_id}") {{
                name
                groups {{
                    name
                }}
            }}
            tours{{
                newGroup
                newRoot
            }}
            trial {{
                completed
                extensionDate
                extensionDays
                startDate
                state
            }}
            userEmail
            userName
            vulnerabilitiesAssigned{{
                id
            }}
            __typename
        }}
    }}"""
    data: dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_vulnerabilities(
    *,
    user: str,
) -> dict[str, Any]:
    query: str = """
        query GetMeAssignedVulnerabilities {
            me {
                findingReattacksConnection {
                    edges {
                        node {
                            groupName
                            id
                            status
                            verificationSummary {
                                requested
                            }
                            vulnerabilitiesToReattackConnection {
                                edges {
                                    node {
                                        lastRequestedReattackDate
                                    }
                                }
                            }
                        }
                    }
                }
                reattacks {
                    edges {
                        node {
                            lastRequestedReattackDate
                        }
                    }
                }
                vulnerabilitiesAssigned {
                    id
                    historicTreatmentConnection {
                        edges {
                            node{
                                assigned
                            }
                        }
                    }
                }
                userEmail
                __typename
            }
        }
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_tag(
    *,
    user: str,
    tag_name: str,
    organization_id: str,
) -> dict[str, Any]:
    query: str = """
        query GetPortfoliosGroups($tag: String!, $organizationId: String) {
            tag(tag: $tag, organizationId: $organizationId) {
                name
                groups {
                    description
                    name
                }
            }
        }
    """
    data: dict = {
        "query": query,
        "variables": {"tag": tag_name, "organizationId": organization_id},
    }

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_me_vulnerabilities_assigned_ids(*, user: str) -> dict:
    """
    Query for GetMeVulnerabilitiesAssignedIds
    in /front/.../navbar/to-do/queries.ts
    """
    query: str = """
      query GetMeVulnerabilitiesAssignedIds {
        me(callerOrigin: "FRONT") {
          vulnerabilitiesAssigned {
            id
          }
          userEmail
          __typename
        }
      }
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
