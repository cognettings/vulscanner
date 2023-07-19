# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)


async def get_result(
    *,
    user: str,
    token_id: str | None = None,
) -> dict:
    query = """
        mutation InvalidateAccessToken($id: ID) {
            invalidateAccessToken(id: $id) {
                success
            }
        }
    """
    data = {"query": query, "variables": {"id": token_id}}

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
