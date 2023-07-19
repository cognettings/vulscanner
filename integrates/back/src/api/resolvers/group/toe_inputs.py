from .schema import (
    GROUP,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
    RootToeInputsRequest,
    ToeInputsConnection,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    validate_connection,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP.field("toeInputs")
@concurrent_decorators(
    enforce_group_level_auth_async,
    validate_connection,
)
async def resolve(  # pylint: disable=too-many-arguments
    parent: Group,
    info: GraphQLResolveInfo,
    root_id: str | None = None,
    after: str | None = None,
    be_present: bool | None = None,
    first: int | None = None,
) -> ToeInputsConnection:
    loaders: Dataloaders = info.context.loaders
    if root_id:
        return await loaders.root_toe_inputs.load(
            RootToeInputsRequest(
                group_name=parent.name,
                root_id=root_id,
                after=after,
                be_present=be_present,
                first=first,
                paginate=True,
            )
        )

    return await loaders.group_toe_inputs.load(
        GroupToeInputsRequest(
            group_name=parent.name,
            after=after,
            be_present=be_present,
            first=first,
            paginate=True,
        )
    )
