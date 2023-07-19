from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from batch.dal import (
    put_action,
)
from batch.enums import (
    Action,
    IntegratesBatchQueue,
    Product,
)
from dataloaders import (
    Dataloaders,
)
from db_model.organization_finding_policies.enums import (
    PolicyStateStatus,
)
from decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from organizations_finding_policies import (
    domain as policies_domain,
)
from sessions import (
    domain as sessions_domain,
)


@MUTATION.field("handleOrganizationFindingPolicyAcceptance")
@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    finding_policy_id: str,
    organization_name: str,
    status: str,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    user_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    user_email: str = user_info["user_email"]
    status_typed = PolicyStateStatus[status]

    await policies_domain.handle_finding_policy_acceptance(
        loaders=loaders,
        email=user_email,
        finding_policy_id=finding_policy_id,
        organization_name=organization_name,
        status=status_typed,
    )

    if status_typed == PolicyStateStatus.APPROVED:
        await put_action(
            action=Action.HANDLE_FINDING_POLICY,
            entity=finding_policy_id,
            subject=user_email,
            additional_info=organization_name,
            product_name=Product.INTEGRATES,
            queue=IntegratesBatchQueue.SMALL,
        )

    return SimplePayload(success=True)
