from .schema import (
    ORGANIZATION_INTEGRATION_REPOSITORIES,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@ORGANIZATION_INTEGRATION_REPOSITORIES.field("name")
def resolve(
    parent: OrganizationIntegrationRepository,
    _info: GraphQLResolveInfo,
) -> str:
    return parent.name if parent.name is not None else ""
