# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)


async def put_mutation(
    *,
    user: str,
    access_key_id: str,
    secret_access_key: str,
) -> dict:
    query: str = """
        query VerifyAwsCredentials(
            $accessKeyId: String!,
            $secretAccessKey: String!
        ) {
            verifyAwsCredentials(
                accessKeyId: $accessKeyId
                secretAccessKey: $secretAccessKey
            )
        }
    """
    data: dict = {
        "query": query,
        "variables": {
            "accessKeyId": access_key_id,
            "secretAccessKey": secret_access_key,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
