from .schema import (
    CREDENTIALS,
)
from dataloaders import (
    Dataloaders,
)
from db_model.credentials.types import (
    Credentials,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
from decorators import (
    require_organization_access,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from outside_repositories.utils import (
    get_credentials_repositories,
)


@CREDENTIALS.field("integrationRepositories")
@require_organization_access
async def resolve(
    parent: Credentials,
    info: GraphQLResolveInfo,
) -> tuple[OrganizationIntegrationRepository, ...]:
    loaders: Dataloaders = info.context.loaders
    unreliable_repositories = (
        await loaders.credential_unreliable_repositories.load(parent.id)
    )
    if unreliable_repositories:
        return tuple(unreliable_repositories)

    repositories = await get_credentials_repositories(loaders, parent)

    return repositories
