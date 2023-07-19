from .schema import (
    ORGANIZATION_INTEGRATION_REPOSITORIES,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@ORGANIZATION_INTEGRATION_REPOSITORIES.field("branches")
def resolve(
    parent: OrganizationIntegrationRepository,
    _info: GraphQLResolveInfo,
) -> tuple[str, ...]:
    return parent.branches if parent.branches is not None else tuple()
