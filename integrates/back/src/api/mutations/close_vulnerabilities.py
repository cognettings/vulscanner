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
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)
from vulnerability_files.close import (
    close_vulnerabilities,
)


@MUTATION.field("closeVulnerabilities")
@concurrent_decorators(
    require_login,
    require_report_vulnerabilities,
    enforce_group_level_auth_async,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    vulnerabilities: list[str],
    **_kwargs: Any,
) -> SimplePayload:
    try:
        processed_vulnerabilities = await close_vulnerabilities(
            loaders=info.context.loaders,
            vulnerabilities_ids=set(vulnerabilities),
            finding_id=finding_id,
            info=info,
        )
        await update_unreliable_indicators_by_deps(
            EntityDependency.upload_file,
            finding_ids=[finding_id],
            vulnerability_ids=list(processed_vulnerabilities),
        )
        await sleep(0.5)  # wait for streams to update

        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Closed vulnerabilities in finding {finding_id}",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to close vulnerabilities in finding "
            f"{finding_id}",
        )
        raise

    return SimplePayload(success=True)
