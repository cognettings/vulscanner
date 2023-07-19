from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from aioextensions import (
    schedule,
)
from api.types import (
    APP_EXCEPTIONS,
)
from custom_utils import (
    cvss as cvss_utils,
    logs as logs_utils,
)
from dataloaders import (
    Dataloaders,
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


@MUTATION.field("resubmitVulnerabilities")
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
        loaders: Dataloaders = info.context.loaders
        user_data = await sessions_domain.get_jwt_content(info.context)
        stakeholder_email = user_data["user_email"]
        await vulns_domain.resubmit_vulnerabilities(
            loaders=loaders,
            vulnerability_ids=set(vulnerabilities),
            finding_id=finding_id,
            modified_by=stakeholder_email,
        )
        await update_unreliable_indicators_by_deps(
            EntityDependency.resubmit_vulnerabilities,
            finding_ids=[finding_id],
        )
        finding = await findings_domain.get_finding(loaders, finding_id)
        severity_score = cvss_utils.get_severity_score(finding.severity)
        severity_level = cvss_utils.get_severity_level(severity_score)
        vulns_properties = await findings_domain.vulns_properties(
            loaders,
            finding_id,
            await get_by_finding_and_vuln_ids(
                loaders, finding_id, set(vulnerabilities)
            ),
        )
        schedule(
            findings_mail.send_mail_submit_vulnerability(
                loaders=loaders,
                finding=finding,
                responsible=stakeholder_email,
                vulnerabilities_properties=vulns_properties,
                severity_score=severity_score,
                severity_level=severity_level,
            )
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Resubmitted vulnerabilities in finding {finding_id}",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to resubmit vulnerabilities in finding "
            f"{finding_id}",
        )
        raise

    return SimplePayload(success=True)
