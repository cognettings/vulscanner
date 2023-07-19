from .payloads.types import (
    AddOrganizationPayload,
)
from .schema import (
    MUTATION,
)
from custom_utils.organizations import (
    get_organization_country,
)
from decorators import (
    require_corporate_email,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)

# Constants
TRANSACTIONS_LOGGER: logging.Logger = logging.getLogger("transactional")


@MUTATION.field("addOrganization")
@require_login
@require_corporate_email
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> AddOrganizationPayload:
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    country = (
        get_organization_country(info.context)
        if kwargs["country"] == "TRIAL"
        else kwargs["country"]
    )
    name = kwargs["name"]

    TRANSACTIONS_LOGGER.info(
        "User %s attempted to add a new organization with name %s",
        user_email,
        name,
    )
    organization = await orgs_domain.add_organization(
        loaders=info.context.loaders,
        organization_name=name,
        email=user_email,
        country=country,
    )
    TRANSACTIONS_LOGGER.info(
        "Organization %s with ID %s was successfully added by %s from %s",
        organization.name,
        organization.id,
        user_email,
        country,
    )

    return AddOrganizationPayload(success=True, organization=organization)
