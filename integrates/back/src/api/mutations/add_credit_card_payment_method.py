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
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)


@MUTATION.field("addCreditCardPaymentMethod")
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
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]

    return SimplePayload(
        success=await billing_domain.create_credit_card_payment_method(
            org=organization,
            user_email=user_email,
            make_default=kwargs["make_default"],
            payment_method_id=kwargs["payment_method_id"],
        )
    )
