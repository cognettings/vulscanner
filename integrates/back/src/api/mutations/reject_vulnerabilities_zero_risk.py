from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from api.types import (
    APP_EXCEPTIONS,
)
from asyncio import (
    sleep,
)
from custom_utils import (
    logs as logs_utils,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_report_vulnerabilities,
    require_request_zero_risk,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from sessions import (
    domain as sessions_domain,
)
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)
from vulnerabilities import (
    domain as vulns_domain,
)


@MUTATION.field("rejectVulnerabilitiesZeroRisk")
@concurrent_decorators(
    require_request_zero_risk,
    require_login,
    require_report_vulnerabilities,
    enforce_group_level_auth_async,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    justification: str,
    vulnerabilities: list[str],
) -> SimplePayload:
    try:
        user_info = await sessions_domain.get_jwt_content(info.context)
        await vulns_domain.reject_vulnerabilities_zero_risk(
            loaders=info.context.loaders,
            vuln_ids=set(vulnerabilities),
            finding_id=finding_id,
            user_info=user_info,
            justification=justification,
        )
        await update_unreliable_indicators_by_deps(
            EntityDependency.reject_vulnerabilities_zero_risk,
            finding_ids=[finding_id],
        )
        await sleep(1.2)  # wait for streams to update
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Rejected a zero risk vuln in finding {finding_id}",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to reject a zero risk vuln in finding "
            f"{finding_id}",
        )
        raise

    return SimplePayload(success=True)
