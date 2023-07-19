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
    cvss_vector: str,
    finding_id: str,
    vulnerability_ids: list[str],
) -> dict[str, Any]:
    query: str = """
            mutation UpdateVulnerabilitiesSeverity(
                $cvssVector: String!,
                $findingId: ID!,
                $vulnerabilityIds: [ID!]!
            ) {
                updateVulnerabilitiesSeverity (
                    cvssVector: $cvssVector,
                    findingId: $findingId,
                    vulnerabilityIds: $vulnerabilityIds,
                ) {
                    success
                }
            }
        """
    variables: dict[str, Any] = {
        "cvssVector": cvss_vector,
        "findingId": finding_id,
        "vulnerabilityIds": vulnerability_ids,
    }
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=email,
        context=get_new_context(),
    )
