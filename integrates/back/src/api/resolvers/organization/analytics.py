from .schema import (
    ORGANIZATION,
)
from analytics import (
    domain as analytics_domain,
)
from db_model.organizations.types import (
    Organization,
)
from decorators import (
    enforce_organization_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@ORGANIZATION.field("analytics")
@enforce_organization_level_auth_async
async def resolve(
    parent: Organization,
    _info: GraphQLResolveInfo,
    **kwargs: str,
) -> object:
    document_name: str = kwargs["document_name"]
    document_type: str = kwargs["document_type"]
    org_id = parent.id

    return await analytics_domain.get_document(
        document_name=document_name,
        document_type=document_type,
        entity="organization",
        subject=org_id,
    )
