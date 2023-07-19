# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
import simplejson as json
from typing import (
    Any,
)


async def get_result(
    *,
    user: str,
    finding: str,
    vulnerabilities_id: list[str],
    status_after_verification: VulnerabilityStateStatus,
) -> dict[str, Any]:
    open_vuln_ids = (
        json.dumps(vulnerabilities_id)
        if status_after_verification == VulnerabilityStateStatus.VULNERABLE
        else "[]"
    )
    closed_vuln_ids = (
        json.dumps(vulnerabilities_id)
        if status_after_verification == VulnerabilityStateStatus.SAFE
        else "[]"
    )
    query: str = f"""
        mutation {{
            verifyVulnerabilitiesRequest(
                findingId: "{finding}",
                justification: "Vuln verified",
                openVulnerabilities: {open_vuln_ids},
                closedVulnerabilities: {closed_vuln_ids}
            ) {{
                success
            }}
        }}
    """
    data: dict = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
