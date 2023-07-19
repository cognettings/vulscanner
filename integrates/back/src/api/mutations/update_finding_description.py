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
    validations,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.enums import (
    FindingSorts,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_finding_access,
    require_login,
    require_report_vulnerabilities,
)
from findings import (
    domain as findings_domain,
)
from findings.types import (
    FindingDescriptionToUpdate,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


@MUTATION.field("updateDescription")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_report_vulnerabilities,
    require_finding_access,
)
async def mutate(
    _: None, info: GraphQLResolveInfo, finding_id: str, **kwargs: Any
) -> SimpleFindingPayload:
    loaders: Dataloaders = info.context.loaders
    try:
        old_finding = await findings_domain.get_finding(loaders, finding_id)
        validations.validate_finding_title_change_policy(
            old_title=old_finding.title,
            new_title=kwargs["title"],
            status=old_finding.unreliable_indicators.unreliable_status,
        )

        description = FindingDescriptionToUpdate(
            attack_vector_description=kwargs["attack_vector_description"],
            description=kwargs["description"],
            recommendation=kwargs["recommendation"],
            sorts=FindingSorts[kwargs["sorts"]]
            if kwargs.get("sorts")
            else None,
            threat=kwargs["threat"],
            title=kwargs["title"],
            unfulfilled_requirements=kwargs.get("unfulfilled_requirements"),
        )
        await findings_domain.update_description(
            loaders=loaders,
            finding_id=finding_id,
            description=description,
        )
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Updated description in finding "
            f"{finding_id} with success",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to update description in finding "
            f"{finding_id}",
        )
        raise

    loaders.finding.clear(finding_id)
    finding = await findings_domain.get_finding(loaders, finding_id)

    return SimpleFindingPayload(finding=finding, success=True)
