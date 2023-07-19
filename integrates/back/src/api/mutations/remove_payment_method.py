from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from billing import (
    domain as billing_domain,
)
from dataloaders import (
    Dataloaders,
)
from decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from organizations import (
    utils as orgs_utils,
)
from typing import (
    Any,
)


@MUTATION.field("removePaymentMethod")
@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    organization = await orgs_utils.get_organization(
        loaders, kwargs["organization_id"]
    )

    return SimplePayload(
        success=await billing_domain.remove_payment_method(
            org=organization,
            payment_method_id=kwargs["payment_method_id"],
        )
    )
