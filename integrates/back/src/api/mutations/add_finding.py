from .payloads.types import (
    SimplePayload,
)
from api.mutations.schema import (
    MUTATION,
)
from api.types import (
    APP_EXCEPTIONS,
)
from custom_utils import (
    cvss as cvss_utils,
    logs as logs_utils,
    requests as requests_utils,
    validations,
)
from custom_utils.validations import (
    check_and_set_min_time_to_remediate,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    CVSS31Severity,
)
from decimal import (
    Decimal,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
    require_report_vulnerabilities,
)
from findings import (
    domain as findings_domain,
)
from findings.types import (
    FindingAttributesToAdd,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from sessions import (
    domain as sessions_domain,
)


@MUTATION.field("addFinding")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_report_vulnerabilities,
)
async def mutate(  # pylint: disable=too-many-arguments,too-many-locals
    _parent: None,
    info: GraphQLResolveInfo,
    attack_vector_description: str,
    group_name: str,
    description: str,
    recommendation: str,
    title: str,
    threat: str,
    unfulfilled_requirements: list[str],
    cvss_vector: str | None = None,
    min_time_to_remediate: int | None = None,
    **kwargs: float,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    stakeholder_info = await sessions_domain.get_jwt_content(info.context)
    stakeholder_email = stakeholder_info["user_email"]
    try:
        if cvss_vector:
            cvss_utils.validate_cvss_vector(cvss_vector)
            severity_legacy = cvss_utils.parse_cvss_vector_string(cvss_vector)
        else:
            cvss_fields = {
                key: Decimal(str(value)) for key, value in kwargs.items()
            }
            validations.validate_missing_severity_field_names(
                set(cvss_fields.keys())
            )
            validations.validate_update_severity_values(cvss_fields)
            severity_legacy = cvss_utils.adjust_privileges_required(
                CVSS31Severity(
                    **{
                        field: cvss_fields[field]
                        for field in CVSS31Severity._fields
                    }
                )
            )
            cvss_vector = cvss_utils.parse_cvss31_severity_legacy(
                severity_legacy
            )

        severity_score = cvss_utils.get_severity_score_from_cvss_vector(
            cvss_vector
        )
        await findings_domain.add_finding(
            loaders=loaders,
            group_name=group_name,
            stakeholder_email=stakeholder_email,
            attributes=FindingAttributesToAdd(
                attack_vector_description=attack_vector_description,
                description=description,
                min_time_to_remediate=check_and_set_min_time_to_remediate(
                    min_time_to_remediate
                ),
                recommendation=recommendation,
                severity=severity_legacy,
                severity_score=severity_score,
                source=requests_utils.get_source_new(info.context),
                threat=threat,
                title=title,
                unfulfilled_requirements=unfulfilled_requirements,
            ),
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Added finding in {group_name} group successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to add finding in {group_name} group",
        )
        raise

    return SimplePayload(success=True)
