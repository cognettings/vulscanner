from .schema import (
    TOE_LINES,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    Root,
)
from db_model.toe_lines.types import (
    ToeLines,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots import (
    utils as roots_utils,
)


@TOE_LINES.field("root")
async def resolve(
    parent: ToeLines,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Root:
    loaders: Dataloaders = info.context.loaders
    root = await roots_utils.get_root(
        loaders, parent.root_id, parent.group_name
    )

    return root
