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
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from findings import (
    domain as findings_domain,
)
from graphql import (
    GraphQLResolveInfo,
)


@MUTATION.field("approveEvidence")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    evidence_id: str,
    finding_id: str,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    await findings_domain.approve_evidence(
        loaders=loaders,
        evidence_id=evidence_id,
        finding_id=finding_id,
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Approved evidence {evidence_id} in finding {finding_id}",
    )

    return SimplePayload(success=True)
