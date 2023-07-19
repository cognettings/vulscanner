from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from custom_utils import (
    logs as logs_utils,
)
from dataloaders import (
    Dataloaders,
)
from decorators import (
    enforce_organization_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from organizations import (
    domain as orgs_domain,
    utils as orgs_utils,
)
from sessions import (
    domain as sessions_domain,
)


@MUTATION.field("removeStakeholderOrganizationAccess")
@enforce_organization_level_auth_async
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    organization_id: str,
    user_email: str,
) -> SimplePayload:
    user_data = await sessions_domain.get_jwt_content(info.context)
    requester_email = user_data["user_email"]
    loaders: Dataloaders = info.context.loaders
    organization = await orgs_utils.get_organization(loaders, organization_id)

    await orgs_domain.remove_access(
        organization_id=organization_id,
        email=user_email.lower(),
        modified_by=requester_email,
        send_reassignment_email=True,
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Stakeholder {requester_email} removed stakeholder"
        f" {user_email} from organization {organization.name}",
    )

    return SimplePayload(success=True)
