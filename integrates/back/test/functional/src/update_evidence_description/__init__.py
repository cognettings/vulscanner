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
    description: str,
    finding_id: str,
    evidence: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
                updateEvidenceDescription(
                description: "{description}",
                findingId: "{finding_id}",
                evidenceId: {evidence}
            ) {{
                success
            }}
        }}
    """
    data: dict[str, str] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
