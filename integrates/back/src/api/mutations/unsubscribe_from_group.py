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
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from sessions import (
    domain as sessions_domain,
)


@MUTATION.field("unsubscribeFromGroup")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None, info: GraphQLResolveInfo, group_name: str
) -> SimplePayload:
    stakeholder_info = await sessions_domain.get_jwt_content(info.context)
    stakeholder_email = stakeholder_info["user_email"]
    loaders: Dataloaders = info.context.loaders
    await groups_domain.unsubscribe_from_group(
        loaders=loaders,
        group_name=group_name,
        email=stakeholder_email,
    )
    msg = (
        f"Security: Unsubscribed stakeholder: {stakeholder_email} "
        f"from {group_name} group successfully"
    )
    logs_utils.cloudwatch_log(info.context, msg)

    return SimplePayload(success=True)
