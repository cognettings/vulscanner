from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from custom_exceptions import (
    ErrorUpdatingGroup,
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
import logging
import logging.config
import re
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)

LOGGER = logging.getLogger(__name__)


@MUTATION.field("removeFiles")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    files_data_input: dict[str, Any],
    group_name: str,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    files_data_input = {
        re.sub(r"_([a-z])", lambda x: x.group(1).upper(), k): v
        for k, v in files_data_input.items()
    }
    file_name = str(files_data_input.get("fileName"))
    group_name = group_name.lower()
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]

    try:
        await groups_domain.remove_file(
            loaders=loaders,
            group_name=group_name,
            file_name=file_name,
            email=user_email,
        )
    except ErrorUpdatingGroup:
        LOGGER.error(
            "Couldn't remove file",
            extra={
                "extra": {
                    "file_name": file_name,
                    "group_name": group_name,
                }
            },
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to remove files from {group_name} group",
        )
        raise

    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Removed files from {group_name} group successfully",
    )
    return SimplePayload(success=True)
