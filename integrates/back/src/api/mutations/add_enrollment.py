from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from custom_utils import (
    logs as logs_utils,
    stakeholders as stakeholders_utils,
)
from dataloaders import (
    Dataloaders,
)
from decorators import (
    concurrent_decorators,
    require_corporate_email,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from sessions import (
    domain as sessions_domain,
)
from stakeholders import (
    domain as stakeholders_domain,
)


@MUTATION.field("addEnrollment")
@concurrent_decorators(
    require_corporate_email,
    require_login,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    user_data = await sessions_domain.get_jwt_content(info.context)
    user_email = user_data["user_email"]

    await stakeholders_domain.add_enrollment(
        loaders=loaders,
        user_email=user_email,
        full_name=stakeholders_utils.get_full_name(user_data),
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Enrolled user {user_email} successfully",
    )

    return SimplePayload(success=True)
