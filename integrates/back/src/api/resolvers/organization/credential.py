from .schema import (
    ORGANIZATION,
)
from dataloaders import (
    Dataloaders,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsRequest,
)
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


@ORGANIZATION.field("credential")
async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> Credentials | None:
    credential_id = kwargs.get("id")
    loaders: Dataloaders = info.context.loaders

    if credential_id:
        credential_stats = CredentialsRequest(
            id=credential_id, organization_id=parent.id
        )
        return await loaders.credentials.load(credential_stats)

    return None
