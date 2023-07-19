from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from aioextensions import (
    collect,
)
from api.types import (
    APP_EXCEPTIONS,
)
from custom_utils import (
    logs as logs_utils,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from server_async.enqueue import (
    queue_refresh_toe_lines_async,
)
from typing import (
    Any,
)


@MUTATION.field("refreshToeLines")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(
    _: None, info: GraphQLResolveInfo, **parameters: Any
) -> SimplePayload:
    try:
        group_name = parameters["group_name"]
        loaders: Dataloaders = info.context.loaders
        roots = tuple(
            root
            for root in (await loaders.group_roots.load(group_name))
            if root.state.status == RootStatus.ACTIVE
            and isinstance(root, GitRoot)
        )
        await collect(
            [
                queue_refresh_toe_lines_async(group_name, root.id)
                for root in roots
            ]
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Schedule the toe lines refreshing in {group_name} "
            "group successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to schedule the toe lines refreshing in "
            f"{group_name} group",
        )
        raise

    return SimplePayload(success=True)
