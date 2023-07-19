from .constants import (
    GSI_2_FACET,
)
from .types import (
    OrganizationIntegrationRepository,
)
from db_model import (
    TABLE,
)
from db_model.organizations.utils import (
    remove_org_id_prefix,
)
from db_model.utils import (
    get_as_utc_iso_format,
)
from dynamodb import (
    keys,
    operations,
)


async def update_unreliable_repositories(
    *,
    repository: OrganizationIntegrationRepository,
) -> None:
    if repository.credential_id:
        organization_id = remove_org_id_prefix(repository.organization_id)
        key_structure = TABLE.primary_key
        primary_key = keys.build_key(
            facet=TABLE.facets[
                "organization_unreliable_integration_repository"
            ],
            values={
                "id": organization_id,
                "hash": repository.id,
                "branch": repository.branch.lower(),
            },
        )
        gsi_2_index = TABLE.indexes["gsi_2"]
        gsi_2_key = keys.build_key(
            facet=GSI_2_FACET,
            values={
                "credential_id": repository.credential_id,
                "hash": repository.id,
            },
        )

        item = {
            key_structure.partition_key: primary_key.partition_key,
            key_structure.sort_key: primary_key.sort_key,
            "branch": repository.branch,
            "branches": repository.branches,
            "last_commit_date": get_as_utc_iso_format(
                repository.last_commit_date
            )
            if repository.last_commit_date
            else None,
            "url": repository.url,
            "credential_id": repository.credential_id,
            "name": repository.name,
            gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
            gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        }

        await operations.put_item(
            facet=TABLE.facets[
                "organization_unreliable_integration_repository"
            ],
            item=item,
            table=TABLE,
        )
