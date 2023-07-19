from .payloads.types import (
    SimpleFindingPayload,
)
from .schema import (
    MUTATION,
)
from api.types import (
    APP_EXCEPTIONS,
)
from custom_exceptions import (
    InvalidCVSSField,
    InvalidCVSSVersion,
)
from custom_utils import (
    cvss as cvss_utils,
    logs as logs_utils,
    validations,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    CVSS31Severity,
)
from decimal import (
    Decimal,
    InvalidOperation,
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
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)


@MUTATION.field("updateSeverity")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_finding_access,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    cvss_version: str,
    cvss_vector: str | None = None,
    **kwargs: float,
) -> SimpleFindingPayload:
    try:
        loaders: Dataloaders = info.context.loaders
        finding = await findings_domain.get_finding(loaders, finding_id)
        if cvss_version != "3.1":
            raise InvalidCVSSVersion()
        if cvss_vector:
            cvss_utils.validate_cvss_vector(cvss_vector)
            await findings_domain.update_severity_from_cvss_vector(
                loaders, finding_id, cvss_vector
            )
        else:
            try:
                cvss_fields = {
                    key: Decimal(str(value)) for key, value in kwargs.items()
                }
            except InvalidOperation as ex:
                raise InvalidCVSSField() from ex
            validations.validate_missing_severity_field_names(
                set(cvss_fields.keys())
            )
            validations.validate_update_severity_values(cvss_fields)
            severity = CVSS31Severity(
                **{
                    field: cvss_fields[field]
                    for field in CVSS31Severity._fields
                }
            )
            await findings_domain.update_severity(
                loaders, finding_id, severity
            )
        await update_unreliable_indicators_by_deps(
            EntityDependency.update_severity,
            finding_ids=[finding_id],
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Updated severity in finding {finding_id} successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to update severity in finding {finding_id}",
        )
        raise

    loaders.finding.clear(finding_id)
    finding = await findings_domain.get_finding(loaders, finding_id)

    return SimpleFindingPayload(finding=finding, success=True)
