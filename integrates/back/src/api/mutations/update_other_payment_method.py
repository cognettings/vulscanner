from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from billing import (
    utils as billing_utils,
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
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
)


@MUTATION.field("updateOtherPaymentMethod")
@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    rut: UploadFile | None = None,
    tax_id: UploadFile | None = None,
    **kwargs: Any,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    organization = await orgs_utils.get_organization(
        loaders, kwargs["organization_id"]
    )

    return SimplePayload(
        success=await billing_utils.update_documents(
            org=organization,
            payment_method_id=kwargs["payment_method_id"],
            business_name=kwargs["business_name"],
            city=kwargs["city"],
            country=kwargs["country"],
            email=kwargs["email"],
            state=kwargs["state"],
            rut=rut,
            tax_id=tax_id,
        )
    )
