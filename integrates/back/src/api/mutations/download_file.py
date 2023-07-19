from .payloads.types import (
    DownloadFilePayload,
)
from .schema import (
    MUTATION,
)
from custom_exceptions import (
    ErrorDownloadingFile,
)
from custom_utils import (
    analytics,
    logs as logs_utils,
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
import logging
import logging.config
from resources import (
    domain as resources_domain,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)

LOGGER = logging.getLogger(__name__)


@MUTATION.field("downloadFile")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None, info: GraphQLResolveInfo, group_name: str, **parameters: Any
) -> DownloadFilePayload:
    file_info = parameters["files_data_input"]
    group_name = group_name.lower()
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    signed_url = await resources_domain.download_file(file_info, group_name)
    if signed_url:
        msg = (
            f'Security: Downloaded file {parameters["files_data_input"]} '
            f"in group {group_name} successfully"
        )
        logs_utils.cloudwatch_log(info.context, msg)
        await analytics.mixpanel_track(
            user_email,
            "DownloadGroupFile",
            Group=group_name.upper(),
            FileName=parameters["files_data_input"],
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to download file "
            f'{parameters["files_data_input"]} in group {group_name}',
        )
        LOGGER.error(
            "Couldn't generate signed URL", extra={"extra": parameters}
        )
        raise ErrorDownloadingFile()

    return DownloadFilePayload(success=True, url=str(signed_url))
