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
    email: str,
    finding_id: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            updateSeverity (
            findingId: "{finding_id}",
            cvssVersion: "3.1",
            attackComplexity: "0.77",
            attackVector: "0.62",
            availabilityImpact: "0",
            availabilityRequirement: "1",
            confidentialityImpact: "0",
            confidentialityRequirement: "1",
            exploitability: "0.91",
            integrityImpact: "0.22",
            integrityRequirement: "1",
            modifiedAttackComplexity: "0.77",
            modifiedAttackVector: "0.62",
            modifiedAvailabilityImpact: "0",
            modifiedConfidentialityImpact: "0",
            modifiedIntegrityImpact: "0.22",
            modifiedPrivilegesRequired: "0.62",
            modifiedSeverityScope: "0",
            modifiedUserInteraction: "0.85",
            privilegesRequired: "0.62",
            remediationLevel: "0.97",
            reportConfidence: "0.92",
            severityScope: "0",
            userInteraction: "0.85"
            ) {{
                finding {{
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
                }}
                success
            }}
        }}
    """
    data: dict[str, str] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=email,
        context=get_new_context(),
    )


async def get_result2(
    *,
    email: str,
    finding_id: str,
    cvss_vector: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            updateSeverity (
            findingId: "{finding_id}",
            cvssVector: "{cvss_vector}",
            cvssVersion: "3.1",
            attackComplexity: "0.0",
            attackVector: "0.0",
            availabilityImpact: "0.0",
            availabilityRequirement: "0.0",
            confidentialityImpact: "0.0",
            confidentialityRequirement: "0.0",
            exploitability: "0.0",
            integrityImpact: "0.0",
            integrityRequirement: "0.0",
            modifiedAttackComplexity: "0.0",
            modifiedAttackVector: "0.0",
            modifiedAvailabilityImpact: "0.0",
            modifiedConfidentialityImpact: "0.0",
            modifiedIntegrityImpact: "0.0",
            modifiedPrivilegesRequired: "0.0",
            modifiedSeverityScope: "0.0",
            modifiedUserInteraction: "0.0",
            privilegesRequired: "0.0",
            remediationLevel: "0.0",
            reportConfidence: "0.0",
            severityScope: "0.0",
            userInteraction: "0.0"
            ) {{
                finding {{
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
                }}
                success
            }}
        }}
    """
    data: dict[str, str] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=email,
        context=get_new_context(),
    )


async def get_finding_severity(
    *,
    email: str,
    finding_id: str,
) -> dict[str, Any]:
    query: str = f"""
        query {{
            finding(
                identifier: "{finding_id}"
            ){{
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
                __typename
            }}
        }}
    """
    data: dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=email,
        context=get_new_context(),
    )
