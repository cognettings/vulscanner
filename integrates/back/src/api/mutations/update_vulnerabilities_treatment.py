from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from api.types import (
    APP_EXCEPTIONS,
)
from custom_utils import (
    cvss as cvss_utils,
    datetime as datetime_utils,
    logs as logs_utils,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
    timezone,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.utils import (
    get_inverted_treatment_converted,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from findings import (
    domain as findings_domain,
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
from vulnerabilities.types import (
    VulnerabilityTreatmentToUpdate,
)


def _get_accepted_until(
    acceptance_date: str | None,
    treatment_status: VulnerabilityTreatmentStatus,
) -> datetime | None:
    if (
        treatment_status != VulnerabilityTreatmentStatus.ACCEPTED
        or not acceptance_date
    ):
        return None

    if len(acceptance_date.split(" ")) == 1:
        today = datetime_utils.get_now_as_str()
        acceptance_date = f"{acceptance_date.split()[0]} {today.split()[1]}"

    return datetime_utils.get_from_str(acceptance_date).astimezone(
        tz=timezone.utc
    )


@MUTATION.field("updateVulnerabilitiesTreatment")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    vulnerability_id: str,
    **kwargs: str,
) -> SimplePayload:
    try:
        user_info = await sessions_domain.get_jwt_content(info.context)
        user_email: str = user_info["user_email"]
        loaders: Dataloaders = info.context.loaders
        finding = await findings_domain.get_finding(loaders, finding_id)
        severity_score = cvss_utils.get_severity_score(finding.severity)
        justification: str = kwargs["justification"]
        treatment_status = VulnerabilityTreatmentStatus[
            get_inverted_treatment_converted(
                kwargs["treatment"].replace(" ", "_").upper()
            )
        ]
        accepted_until = _get_accepted_until(
            kwargs.get("acceptance_date"), treatment_status
        )
        assigned = kwargs.get("assigned", "")
        await vulns_domain.update_vulnerabilities_treatment(
            loaders=loaders,
            finding=finding,
            finding_severity=severity_score,
            modified_by=user_email,
            vulnerability_id=vulnerability_id,
            treatment=VulnerabilityTreatmentToUpdate(
                accepted_until=accepted_until,
                assigned=assigned,
                justification=justification,
                status=treatment_status,
            ),
        )
        await update_unreliable_indicators_by_deps(
            EntityDependency.update_vulnerabilities_treatment,
            finding_ids=[finding_id],
            vulnerability_ids=[vulnerability_id],
        )
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Vulnerabilities treatment successfully updated in "
            f"finding {finding_id}",
        )

    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to update vulnerabilities treatment in "
            f"finding {finding_id}",
        )
        raise

    return SimplePayload(success=True)
