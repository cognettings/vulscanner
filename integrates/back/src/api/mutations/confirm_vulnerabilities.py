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
    cvss as cvss_utils,
    logs as logs_utils,
)
from dataloaders import (
    Dataloaders,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_report_vulnerabilities,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from mailer import (
    findings as findings_mail,
)
from sessions import (
    domain as sessions_domain,
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
from vulnerabilities import (
    domain as vulns_domain,
)
from vulnerabilities.domain.core import (
    get_by_finding_and_vuln_ids,
)


@MUTATION.field("confirmVulnerabilities")
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
) -> SimplePayload:
    try:
        loaders: Dataloaders = info.context.loaders
        user_data = await sessions_domain.get_jwt_content(info.context)
        stakeholder_email = user_data["user_email"]
        vulnerabilities_set = set(vulnerabilities)
        await vulns_domain.confirm_vulnerabilities(
            loaders=loaders,
            vuln_ids=vulnerabilities_set,
            finding_id=finding_id,
            modified_by=stakeholder_email,
        )
        await update_unreliable_indicators_by_deps(
            EntityDependency.confirm_vulnerabilities,
            finding_ids=[finding_id],
            vulnerability_ids=list(vulnerabilities_set),
        )
        reported_vulnerabilities = list(
            await get_by_finding_and_vuln_ids(
                loaders, finding_id, vulnerabilities_set
            )
        )
        finding = await findings_domain.get_finding(loaders, finding_id)
        severity_score = cvss_utils.get_vulnerabilities_score(
            finding,
            reported_vulnerabilities,
            VulnerabilityStateStatus.SUBMITTED,
        )
        severity_level = cvss_utils.get_severity_level(severity_score)
        vulnerabilities_properties: dict[
            str, Any
        ] = await findings_domain.vulns_properties(
            loaders,
            finding_id,
            reported_vulnerabilities,
        )
        await findings_mail.send_mail_vulnerability_report(
            loaders=loaders,
            group_name=finding.group_name,
            finding_title=finding.title,
            finding_id=finding_id,
            vulnerabilities_properties=vulnerabilities_properties,
            responsible=reported_vulnerabilities[0].hacker_email
            if reported_vulnerabilities
            else finding.hacker_email,
            severity_score=severity_score,
            severity_level=severity_level,
        )
        await sleep(0.8)  # wait for streams to update
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Approve vulnerabilities in finding {finding_id}",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to approve vulnerabilities in finding "
            f"{finding_id}",
        )
        raise

    return SimplePayload(success=True)
