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
    group: str,
    credentials: dict,
    url: str,
) -> dict:
    query: str = """
      mutation AddGitRoot (
        $groupName: String!, $credentials: RootCredentialsInput, $url: String!
      ) {
        addGitRoot(
          branch: "trunk"
          credentials: $credentials
          environment: "production"
          gitignore: []
          groupName: $groupName
          includesHealthCheck: true
          url: $url
        ) {
          rootId
          success
        }
      }
    """
    data: dict = {
        "query": query,
        "variables": {
            "groupName": group,
            "credentials": credentials,
            "url": url,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
