from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from custom_utils.datetime import (
    get_now,
)
from dataloaders import (
    Dataloaders,
)
from db_model.events.enums import (
    EventEvidenceId,
)
from db_model.events.types import (
    EventRequest,
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
from groups import (
    domain as groups_domain,
)
from organizations.utils import (
    get_organization,
)
from starlette.datastructures import (
    UploadFile,
)


@MUTATION.field("updateEventEvidence")
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
    file: UploadFile,
    group_name: str,
    **_kwargs: None,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    evidence_id = EventEvidenceId[evidence_type]
    event = await events_domain.get_event(
        loaders, EventRequest(event_id=event_id, group_name=group_name)
    )
    group = await groups_domain.get_group(loaders, event.group_name)
    organization = await get_organization(loaders, group.organization_id)
    await events_domain.validate_evidence(
        group_name=group.name.lower(),
        organization_name=organization.name.lower(),
        evidence_id=evidence_id,
        file=file,
    )

    await events_domain.update_evidence(
        loaders=loaders,
        event_id=event_id,
        evidence_id=evidence_id,
        file=file,
        group_name=group_name,
        update_date=get_now(),
    )
    loaders.event.clear(EventRequest(event_id=event_id, group_name=group_name))

    return SimplePayload(success=True)
