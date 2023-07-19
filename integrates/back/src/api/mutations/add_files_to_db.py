from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from custom_exceptions import (
    ErrorFileNameAlreadyExists,
    InvalidChar,
)
from custom_utils import (
    logs as logs_utils,
    utils,
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
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)

LOGGER = logging.getLogger(__name__)


@MUTATION.field("addFilesToDb")
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
    group_name = str(group_name).lower()
    files_data = kwargs["files_data_input"]
    new_files_data = utils.camel_case_list_dict(files_data)
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]

    try:
        for file_data in new_files_data:
            await groups_domain.add_file(
                loaders=loaders,
                description=file_data["description"],
                file_name=file_data["fileName"],
                group_name=group_name,
                email=user_email,
            )
    except (InvalidChar, ErrorFileNameAlreadyExists):
        LOGGER.error(
            "Couldn't add the file to the db", extra={"extra": kwargs}
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to add resource files "
            f"from {group_name} group",
        )
        raise

    logs_utils.cloudwatch_log(
        info.context,
        f'Security: Added file {kwargs["files_data_input"]} '
        f"to db in group {group_name} successfully",
    )

    return SimplePayload(success=True)
