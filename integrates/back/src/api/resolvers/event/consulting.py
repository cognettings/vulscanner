from .schema import (
    EVENT,
)
from custom_utils.event_comments import (
    format_event_consulting_resolve,
)
from dataloaders import (
    Dataloaders,
)
from db_model.events.types import (
    Event,
)
from decorators import (
    require_squad,
)
from dynamodb.types import (
    Item,
)
from event_comments import (
    domain as event_comments_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from sessions import (
    domain as sessions_domain,
)


@EVENT.field("consulting")
@require_squad
async def resolve(
    parent: Event,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Item]:
    loaders: Dataloaders = info.context.loaders
    user_data: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    event_coments = await event_comments_domain.get_comments(
        loaders,
        parent.group_name,
        parent.id,
        user_data["user_email"],
    )

    return [
        format_event_consulting_resolve(comment) for comment in event_coments
    ]
