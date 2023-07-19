from .schema import (
    ORGANIZATION,
)
from dataloaders import (
    Dataloaders,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepositoryConnection,
    OrganizationIntegrationRepositoryRequest,
)
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@ORGANIZATION.field("integrationRepositoriesConnection")
async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    after: str | None = None,
    first: int | None = None,
    **_kwargs: None,
) -> OrganizationIntegrationRepositoryConnection:
    loaders: Dataloaders = info.context.loaders
    current_repositories = (
        await loaders.organization_unreliable_integration_repositories_c.load(
            OrganizationIntegrationRepositoryRequest(
                organization_id=parent.id,
                after=after,
                first=first,
                paginate=True,
            )
        )
    )

    return current_repositories
