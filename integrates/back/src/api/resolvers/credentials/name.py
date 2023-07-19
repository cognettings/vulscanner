from .schema import (
    CREDENTIALS,
)
from db_model.credentials.types import (
    Credentials,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@CREDENTIALS.field("name")
def resolve(parent: Credentials, _info: GraphQLResolveInfo) -> str:
    return parent.state.name
