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
    finding: str,
    accepted_vulnerability_id: str,
    rejected_vulnerability_id: str,
) -> dict[str, Any]:
    query = f"""
        mutation {{
            handleVulnerabilitiesAcceptance(
                acceptedVulnerabilities:
                    ["{accepted_vulnerability_id}"]
                findingId: "{finding}",
                justification: "test of handle vulns justification",
                rejectedVulnerabilities: ["{rejected_vulnerability_id}"]
            ) {{
            success
            }}
        }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
