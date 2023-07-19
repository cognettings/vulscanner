from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from custom_exceptions import (
    PermissionDenied,
)
from custom_utils import (
    logs as logs_utils,
    validations as validations_utils,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    GroupMetadataToUpdate,
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
from typing import (
    Any,
)


@MUTATION.field("updateGroupAccessInfo")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    group_name: str,
    **kwargs: Any,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    group_name = group_name.lower()
    group = await groups_domain.get_group(loaders, group_name)
    try:
        group_context = validations_utils.validate_markdown(
            kwargs.get("group_context", "")
        )

        await groups_domain.update_metadata(
            group_name=group_name,
            metadata=GroupMetadataToUpdate(
                context=group_context,
            ),
            organization_id=group.organization_id,
        )
    except PermissionDenied:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Unauthorized role attempted to update group "
            f"{group_name}",
        )
        raise

    return SimplePayload(success=True)
