from .payloads.types import (
    SimpleFindingPayload,
)
from .schema import (
    MUTATION,
)
from api.types import (
    APP_EXCEPTIONS,
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
    require_asm,
    require_finding_access,
    require_login,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@MUTATION.field("removeEvidence")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_finding_access,
)
async def mutate(
    _: None, info: GraphQLResolveInfo, evidence_id: str, finding_id: str
) -> SimpleFindingPayload:
    loaders: Dataloaders = info.context.loaders
    try:
        await findings_domain.remove_evidence(loaders, evidence_id, finding_id)
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Removed evidence in finding {finding_id} successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to remove evidence in finding {finding_id}",
        )
        raise

    loaders.finding.clear(finding_id)
    finding = await findings_domain.get_finding(loaders, finding_id)

    return SimpleFindingPayload(finding=finding, success=True)
