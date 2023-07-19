from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from api.types import (
    APP_EXCEPTIONS,
)
from custom_exceptions import (
    EventAlreadyClosed,
    EventNotFound,
)
from custom_utils import (
    logs as logs_utils,
)
from dataloaders import (
    Dataloaders,
)
from db_model.events.enums import (
    EventStateStatus,
)
from db_model.events.types import (
    EventRequest,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_continuous,
    require_finding_access,
    require_login,
    require_report_vulnerabilities,
)
from events import (
    domain as events_domain,
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


@MUTATION.field("requestVulnerabilitiesHold")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_continuous,
    require_asm,
    require_report_vulnerabilities,
    require_finding_access,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    event_id: str,
    group_name: str,
    finding_id: str,
    vulnerabilities: list[str],
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    try:
        user_info = await sessions_domain.get_jwt_content(info.context)
        event = await events_domain.get_event(
            loaders, EventRequest(event_id=event_id, group_name=group_name)
        )
        if group_name != event.group_name:
            raise EventNotFound()
        if event.state.status == EventStateStatus.SOLVED:
            raise EventAlreadyClosed()

        await events_domain.request_vulnerabilities_hold(
            loaders=loaders,
            event_id=event_id,
            finding_id=finding_id,
            user_info=user_info,
            vulnerability_ids=set(vulnerabilities),
        )
        await update_unreliable_indicators_by_deps(
            EntityDependency.request_vulnerabilities_hold,
            finding_ids=[finding_id],
            vulnerability_ids=vulnerabilities,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Requested vuln reattack hold in finding {finding_id}",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to request reattack hold in finding "
            f"{finding_id}",
        )
        raise

    return SimplePayload(success=True)
