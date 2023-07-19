from .schema import (
    QUERY,
)
from custom_exceptions import (
    ExecutionNotFound,
)
from custom_utils.forces import (
    format_forces_to_resolve,
)
from dataloaders import (
    Dataloaders,
)
from db_model.forces.types import (
    ForcesExecution,
    ForcesExecutionRequest,
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
from typing import (
    Any,
)


@QUERY.field("forcesExecution")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    _: None, info: GraphQLResolveInfo, **kwargs: str
) -> dict[str, Any]:
    execution_id: str = kwargs["execution_id"]
    group_name: str = kwargs["group_name"]
    loaders: Dataloaders = info.context.loaders
    execution: ForcesExecution | None = await loaders.forces_execution.load(
        ForcesExecutionRequest(
            group_name=group_name, execution_id=execution_id
        )
    )

    if execution:
        return format_forces_to_resolve(execution=execution)

    raise ExecutionNotFound()
