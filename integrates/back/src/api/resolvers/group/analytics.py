from .schema import (
    GROUP,
)
from analytics import (
    domain as analytics_domain,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP.field("analytics")
@concurrent_decorators(
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **kwargs: str,
) -> object:
    document_name: str = kwargs["document_name"]
    document_type: str = kwargs["document_type"]

    return await analytics_domain.get_document(
        document_name=document_name,
        document_type=document_type,
        entity="group",
        subject=parent.name,
    )
