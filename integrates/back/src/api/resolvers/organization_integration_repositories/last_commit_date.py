from .schema import (
    ORGANIZATION_INTEGRATION_REPOSITORIES,
)
from custom_utils import (
    datetime as datetime_utils,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@ORGANIZATION_INTEGRATION_REPOSITORIES.field("lastCommitDate")
def resolve(
    parent: OrganizationIntegrationRepository,
    _info: GraphQLResolveInfo,
) -> str | None:
    return (
        datetime_utils.get_as_str(parent.last_commit_date)
        if parent.last_commit_date
        else None
    )
