from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from custom_utils import (
    logs as logs_utils,
)
from dataloaders import (
    Dataloaders,
)
from db_model.events.enums import (
    EventEvidenceId,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from events import (
    domain as events_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@MUTATION.field("removeEventEvidence")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    event_id: str,
    evidence_type: str,
    group_name: str,
    **_kwargs: str,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    evidence_id = EventEvidenceId[evidence_type]
    await events_domain.remove_evidence(
        loaders, evidence_id, event_id, group_name
    )
    logs_utils.cloudwatch_log(
        info.context, f"Security: Removed evidence in event {event_id}"
    )

    return SimplePayload(success=True)
