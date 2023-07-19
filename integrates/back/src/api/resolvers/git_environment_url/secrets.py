from .schema import (
    GIT_ENVIRONMENT_URL,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    RootEnvironmentSecretsRequest,
    RootEnvironmentUrl,
    Secret,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GIT_ENVIRONMENT_URL.field("secrets")
@enforce_group_level_auth_async
async def resolve(
    parent: RootEnvironmentUrl, info: GraphQLResolveInfo, **__: None
) -> list[Secret]:
    loaders: Dataloaders = info.context.loaders
    if parent.group_name:
        return await loaders.environment_secrets.load(
            RootEnvironmentSecretsRequest(
                url_id=parent.id, group_name=parent.group_name
            )
        )
    return []
