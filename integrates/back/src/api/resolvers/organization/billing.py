from .schema import (
    ORGANIZATION,
)
from billing import (
    authors as billing_authors,
)
from billing.types import (
    OrganizationBilling,
)
from custom_utils import (
    datetime as datetime_utils,
)
from datetime import (
    datetime,
)
from db_model.organizations.types import (
    Organization,
)
from decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@ORGANIZATION.field("billing")
@concurrent_decorators(
    enforce_organization_level_auth_async,
    require_login,
)
async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **kwargs: datetime,
) -> OrganizationBilling:
    return await billing_authors.get_organization_billing(
        date=kwargs.get("date", datetime_utils.get_now()),
        org=parent,
        loaders=info.context.loaders,
    )
