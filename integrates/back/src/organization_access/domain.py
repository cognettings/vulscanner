import authz
from dataloaders import (
    Dataloaders,
)
from db_model import (
    organization_access as org_access_model,
)
from db_model.organization_access.types import (
    OrganizationAccessMetadataToUpdate,
    OrganizationAccessRequest,
)


async def add_access(
    loaders: Dataloaders, organization_id: str, email: str, role: str
) -> None:
    await org_access_model.update_metadata(
        organization_id=organization_id,
        email=email,
        metadata=OrganizationAccessMetadataToUpdate(
            has_access=True,
        ),
    )
    await authz.grant_organization_level_role(
        loaders, email, organization_id, role
    )


async def has_access(
    loaders: Dataloaders, organization_id: str, email: str
) -> bool:
    if (
        await authz.get_organization_level_role(
            loaders, email, organization_id
        )
        == "admin"
    ):
        return True

    if await loaders.organization_access.load(
        OrganizationAccessRequest(organization_id=organization_id, email=email)
    ):
        return True
    return False
