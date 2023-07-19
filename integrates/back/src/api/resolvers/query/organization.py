from .schema import (
    QUERY,
)
from dataloaders import (
    Dataloaders,
)
from db_model.organizations.types import (
    Organization,
)
from decorators import (
    concurrent_decorators,
    require_login,
    require_organization_access,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@QUERY.field("organization")
@concurrent_decorators(
    require_login,
    require_organization_access,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Organization | None:
    loaders: Dataloaders = info.context.loaders
    organization_id: str = kwargs["organization_id"]

    return await loaders.organization.load(organization_id)
