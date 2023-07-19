# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)


async def run_mutation(
    *,
    user: str,
    finding: str,
    vulnerability: str,
) -> dict:
    query: str = """
        mutation CloseVulnerabilities(
            $findingId: String!,
            $vulnerabilities: [String!]!
        ) {
            closeVulnerabilities (
                findingId: $findingId,
                vulnerabilities: $vulnerabilities,
            ) {
                success
            }
        }
    """
    variables = {
        "findingId": finding,
        "vulnerabilities": [vulnerability],
    }
    data = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
