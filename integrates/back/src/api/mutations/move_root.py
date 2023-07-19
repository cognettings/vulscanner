from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from batch import (
    dal as batch_dal,
)
from batch.enums import (
    Action,
    IntegratesBatchQueue,
    Product,
)
from custom_utils import (
    logs as logs_utils,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    GitRoot,
    IPRoot,
    URLRoot,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    rename_kwargs,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import json
from roots import (
    domain as roots_domain,
    utils as roots_utils,
)
from sessions import (
    domain as sessions_domain,
)


@MUTATION.field("moveRoot")
@concurrent_decorators(require_login, enforce_group_level_auth_async)
@rename_kwargs(
    {"group_name": "source_group_name", "target_group_name": "group_name"}
)
@enforce_group_level_auth_async
@rename_kwargs(
    {"group_name": "target_group_name", "source_group_name": "group_name"}
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    user_info = await sessions_domain.get_jwt_content(info.context)
    email = user_info["user_email"]
    group_name: str = kwargs["group_name"].lower()
    root_id: str = kwargs["id"]
    target_group_name: str = kwargs["target_group_name"].lower()

    new_root_id = await roots_domain.move_root(
        loaders=loaders,
        email=email,
        group_name=group_name,
        root_id=root_id,
        target_group_name=target_group_name,
    )
    await batch_dal.put_action(
        action=Action.MOVE_ROOT,
        entity=group_name,
        subject=email,
        additional_info=json.dumps(
            {
                "target_group_name": target_group_name,
                "target_root_id": new_root_id,
                "source_group_name": group_name,
                "source_root_id": root_id,
            },
        ),
        queue=IntegratesBatchQueue.SMALL,
        product_name=Product.INTEGRATES,
    )
    root = await roots_utils.get_root(loaders, root_id, group_name)
    if isinstance(root, GitRoot):
        await batch_dal.put_action(
            action=Action.REFRESH_TOE_LINES,
            attempt_duration_seconds=7200,
            entity=group_name,
            subject=email,
            additional_info=root.state.nickname,
            product_name=Product.INTEGRATES,
            queue=IntegratesBatchQueue.SMALL,
        )
    if isinstance(root, (GitRoot, URLRoot)):
        await batch_dal.put_action(
            action=Action.REFRESH_TOE_INPUTS,
            entity=group_name,
            subject=email,
            additional_info=root.state.nickname,
            product_name=Product.INTEGRATES,
            queue=IntegratesBatchQueue.SMALL,
        )
    if isinstance(root, IPRoot):
        await batch_dal.put_action(
            action=Action.REFRESH_TOE_PORTS,
            entity=group_name,
            subject=email,
            additional_info=root.state.nickname,
            product_name=Product.INTEGRATES,
            queue=IntegratesBatchQueue.SMALL,
        )

    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Moved a root from {group_name} to {target_group_name}",
    )

    return SimplePayload(success=True)
