from .schema import (
    QUERY,
)
from dataloaders import (
    Dataloaders,
)
from db_model.events.types import (
    Event,
    EventRequest,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    rename_kwargs,
    require_asm,
    require_login,
)
from events import (
    domain as events_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@QUERY.field("event")
@rename_kwargs({"identifier": "event_id"})
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
@rename_kwargs({"event_id": "identifier"})
async def resolve(
    _parent: None, info: GraphQLResolveInfo, group_name: str, **kwargs: str
) -> Event:
    event_id: str = kwargs["identifier"]
    loaders: Dataloaders = info.context.loaders

    return await events_domain.get_event(
        loaders, EventRequest(event_id=event_id, group_name=group_name)
    )
