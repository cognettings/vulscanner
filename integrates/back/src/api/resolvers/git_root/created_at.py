from .schema import (
    GIT_ROOT,
)
from datetime import (
    datetime,
)
from db_model.roots.types import (
    GitRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GIT_ROOT.field("createdAt")
def resolve(parent: GitRoot, _info: GraphQLResolveInfo) -> datetime:
    return parent.created_date
