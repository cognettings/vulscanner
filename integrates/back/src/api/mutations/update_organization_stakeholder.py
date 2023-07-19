from .payloads.types import (
    UpdateStakeholderPayload,
)
from .schema import (
    MUTATION,
)
from custom_exceptions import (
    StakeholderNotFound,
)
from custom_utils import (
    logs as logs_utils,
)
from custom_utils.utils import (
    map_roles,
)
from dataloaders import (
    Dataloaders,
)
from db_model.organization_access.types import (
    OrganizationAccessRequest,
)
from decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
    require_organization_access,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
    utils as orgs_utils,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)

# Constants
LOGGER = logging.getLogger(__name__)


@MUTATION.field("updateOrganizationStakeholder")
@concurrent_decorators(
    require_login,
    require_organization_access,
    enforce_organization_level_auth_async,
)
async def mutate(
    _: None, info: GraphQLResolveInfo, **parameters: Any
) -> UpdateStakeholderPayload:
    loaders: Dataloaders = info.context.loaders
    organization_id: str = str(parameters.get("organization_id"))
    organization = await orgs_utils.get_organization(loaders, organization_id)
    requester_data = await sessions_domain.get_jwt_content(info.context)
    requester_email = requester_data["user_email"]

    user_email: str = str(parameters.get("user_email"))
    new_role: str = map_roles(str(parameters.get("role")).lower())

    if (
        organization_access := await loaders.organization_access.load(
            OrganizationAccessRequest(
                organization_id=organization_id, email=user_email
            )
        )
    ) is None:
        raise StakeholderNotFound()

    # Validate role requirements before changing anything
    await orgs_domain.update_stakeholder_role(
        loaders=loaders,
        user_email=user_email,
        organization_id=organization_id,
        organization_access=organization_access,
        new_role=new_role,
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Stakeholder {requester_email} modified "
        f"information from the stakeholder {user_email} "
        f"in the organization {organization.name}",
    )

    return UpdateStakeholderPayload(
        success=True, modified_stakeholder=dict(email=user_email)
    )
