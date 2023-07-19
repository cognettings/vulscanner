from .payloads.types import (
    AddEnvironmentUrlPayload,
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
    require_login,
    require_service_white,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots import (
    domain as roots_domain,
)
from sessions.domain import (
    get_jwt_content,
)


@MUTATION.field("addGitEnvironmentUrl")
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_service_white
)
async def mutate(  # pylint: disable = too-many-arguments
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    url: str,
    url_type: str,
    root_id: str,
    cloud_name: str | None = None,
    **_kwargs: None,
) -> AddEnvironmentUrlPayload:
    loaders: Dataloaders = info.context.loaders
    user_info = await get_jwt_content(info.context)
    user_email = user_info["user_email"]
    await roots_domain.add_root_environment_url(
        loaders=loaders,
        group_name=group_name,
        root_id=root_id,
        url=url,
        url_type=url_type,
        user_email=user_email,
        should_notified=True,
        cloud_type=cloud_name,
    )
    logs_utils.cloudwatch_log(
        info.context, f"Security: Updated git envs for root {root_id}"
    )

    urls = await loaders.root_environment_urls.load(root_id)
    for _url in urls:
        if _url.url == url:
            new_url_id = _url.id

    return AddEnvironmentUrlPayload(success=True, url_id=new_url_id)
