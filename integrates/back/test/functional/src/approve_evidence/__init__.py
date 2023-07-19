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
    *, email: str, evidence_id: str, finding_id: str
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            approveEvidence(
                evidenceId: {evidence_id},
                findingId: "{finding_id}",
            ) {{
                success
            }}
        }}
    """
    return await get_graphql_result(
        {"query": query},
        stakeholder=email,
        context=get_new_context(),
    )
