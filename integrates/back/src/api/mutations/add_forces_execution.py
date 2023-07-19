from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from custom_utils import (
    logs as logs_utils,
)
from decorators import (
    enforce_group_level_auth_async,
)
from forces import (
    domain as forces_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
)


@MUTATION.field("addForcesExecution")
@enforce_group_level_auth_async
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    log: UploadFile | None = None,
    **parameters: Any,
) -> SimplePayload:
    await forces_domain.add_forces_execution(
        group_name=group_name, log=log, **parameters
    )
    logs_utils.cloudwatch_log(
        info.context,
        (
            f"Security: Created forces execution in {group_name} "
            "group successfully"
        ),
    )
    return SimplePayload(success=True)
