from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
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
from vulnerabilities import (
    domain as vulns_domain,
)


@MUTATION.field("confirmVulnerabilitiesZeroRisk")
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
    """Resolve confirm_vulnerabilities_zero_risk mutation."""
    user_info = await sessions_domain.get_jwt_content(info.context)
    await vulns_domain.confirm_vulnerabilities_zero_risk(
        loaders=info.context.loaders,
        vuln_ids=set(vulnerabilities),
        finding_id=finding_id,
        user_info=user_info,
        justification=justification,
    )
    logs_utils.cloudwatch_log(
        info.context,
        (
            "Security: Confirmed zero risk vulnerabilities "
            f"in finding_id: {finding_id}"
        ),
    )

    return SimplePayload(success=True)
