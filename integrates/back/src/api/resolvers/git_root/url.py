from .schema import (
    GIT_ROOT,
)
from db_model.roots.types import (
    GitRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GIT_ROOT.field("url")
def resolve(parent: GitRoot, _info: GraphQLResolveInfo) -> str:
    return parent.state.url
