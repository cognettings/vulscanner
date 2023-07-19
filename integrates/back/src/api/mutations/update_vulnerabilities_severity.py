from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from aioextensions import (
    collect,
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
from dataloaders import (
    Dataloaders,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
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


@MUTATION.field("updateVulnerabilitiesSeverity")
@concurrent_decorators(require_login, enforce_group_level_auth_async)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    cvss_vector: str,
    finding_id: str,
    vulnerability_ids: list[str],
) -> SimplePayload:
    try:
        loaders: Dataloaders = info.context.loaders
        vulnerability_ids_set = set(vulnerability_ids)
        vulnerabilities = await vulns_domain.get_by_finding_and_vuln_ids(
            loaders, finding_id, vulnerability_ids_set
        )
        await collect(
            [
                vulns_domain.update_severity_score(
                    loaders=loaders,
                    vulnerability_id=vulnerability.id,
                    cvss_vector=cvss_vector,
                )
                for vulnerability in vulnerabilities
            ],
            workers=32,
        )
        finding_ids_set = set(
            vulnerability.finding_id for vulnerability in vulnerabilities
        )
        await update_unreliable_indicators_by_deps(
            EntityDependency.update_severity,
            finding_ids=list(finding_ids_set),
            vulnerability_ids=list(vulnerability_ids_set),
        )
        await sleep(1)  # wait for streams to update
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Updated severity for vulnerabilities successfully: "
            f"{vulnerability_ids_set} ",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to update severity for vulnerabilities: "
            f"{set(vulnerability_ids)}",
        )
        raise

    return SimplePayload(success=True)
