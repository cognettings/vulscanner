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
    vulnerability: str,
) -> dict[str, Any]:
    query: str = f"""
            mutation {{
                rejectVulnerabilitiesZeroRisk(
                    findingId: "{finding}",
                    justification: "reject zero risk vuln",
                    vulnerabilities:
                        ["{vulnerability}"]
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
