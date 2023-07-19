from .schema import (
    ME,
)
from dataloaders import (
    Dataloaders,
)
from db_model.stakeholders.types import (
    NotificationsPreferences,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from mailer import (
    utils,
)
from stakeholders.domain import (
    get_stakeholder,
)
from typing import (
    Any,
)


@ME.field("notificationsPreferences")
async def resolve(
    parent: dict[str, Any], info: GraphQLResolveInfo, **_kwargs: None
) -> NotificationsPreferences:
    loaders: Dataloaders = info.context.loaders
    email = str(parent["user_email"])
    stakeholder = await get_stakeholder(loaders, email)

    return stakeholder.state.notifications_preferences._replace(
        available=await utils.get_available_notifications(loaders, email)
    )
