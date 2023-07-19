from .schema import (
    GIT_ROOT,
)
from custom_utils import (
    datetime as datetime_utils,
)
from db_model.roots.types import (
    GitRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GIT_ROOT.field("lastCloningStatusUpdate")
def resolve(parent: GitRoot, _info: GraphQLResolveInfo) -> str:
    return datetime_utils.get_as_str(parent.cloning.modified_date)
