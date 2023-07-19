from .constants import (
    GSI_2_FACET,
)
from .types import (
    OrganizationIntegrationRepository,
    OrganizationIntegrationRepositoryConnection,
    OrganizationIntegrationRepositoryEdge,
    OrganizationIntegrationRepositoryRequest,
)
from .utils import (
    format_organization_integration_repository,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from collections.abc import (
    Iterable,
)
from db_model import (
    TABLE,
)
from db_model.organizations.utils import (
    remove_org_id_prefix,
)
from dynamodb import (
    keys,
    operations,
)


async def _get_unreliable_integration_repositories(
    organization_id: str,
    url_id: str | None = None,
    branch: str | None = None,
) -> list[OrganizationIntegrationRepository]:
    organization_id = remove_org_id_prefix(organization_id)
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_unreliable_integration_repository"],
        values={
            "id": organization_id,
            **(
                {"hash": url_id, "branch": branch} if url_id and branch else {}
            ),
        },
    )

    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & (
                Key(key_structure.sort_key).eq(primary_key.sort_key)
                if url_id and branch
                else Key(key_structure.sort_key).begins_with("URL#")
            )
        ),
        facets=(
            TABLE.facets["organization_unreliable_integration_repository"],
        ),
        table=TABLE,
    )

    if not response.items:
        return []

    return [
        format_organization_integration_repository(item)
        for item in response.items
    ]


async def _get_organization_unreliable_integration_repositories(
    request: OrganizationIntegrationRepositoryRequest,
) -> OrganizationIntegrationRepositoryConnection:
    organization_id = remove_org_id_prefix(request.organization_id)
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_unreliable_integration_repository"],
        values={
            "id": organization_id,
        },
    )

    response = await operations.query(
        after=request.after,
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with("URL#")
        ),
        facets=(
            TABLE.facets["organization_unreliable_integration_repository"],
        ),
        limit=request.first,
        paginate=request.paginate,
        table=TABLE,
    )

    return OrganizationIntegrationRepositoryConnection(
        edges=tuple(
            OrganizationIntegrationRepositoryEdge(
                cursor=response.page_info.end_cursor,
                node=format_organization_integration_repository(item),
            )
            for item in response.items
        ),
        page_info=response.page_info,
    )


async def _get_credential_unreliable_integration_repositories(
    credential_id: str,
) -> list[OrganizationIntegrationRepository]:
    facet = GSI_2_FACET
    primary_key = keys.build_key(
        facet=facet,
        values={
            "credential_id": credential_id,
        },
    )
    index = TABLE.indexes["gsi_2"]
    key_structure = index.primary_key

    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(
            TABLE.facets["organization_unreliable_integration_repository"],
        ),
        index=index,
        table=TABLE,
    )

    return [
        format_organization_integration_repository(item)
        for item in response.items
    ]


class OrganizationUnreliableRepositoriesLoader(
    DataLoader[
        tuple[str, str | None, str | None],
        list[OrganizationIntegrationRepository],
    ]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, ids: Iterable[tuple[str, str | None, str | None]]
    ) -> list[list[OrganizationIntegrationRepository]]:
        return list(
            await collect(
                tuple(
                    _get_unreliable_integration_repositories(
                        organization_id=organization_id,
                        url_id=url_id,
                        branch=branch,
                    )
                    for organization_id, url_id, branch in ids
                )
            )
        )


class CredentialUnreliableRepositoriesLoader(
    DataLoader[
        str,
        list[OrganizationIntegrationRepository],
    ]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, ids: Iterable[str]
    ) -> list[list[OrganizationIntegrationRepository]]:
        return list(
            await collect(
                tuple(
                    _get_credential_unreliable_integration_repositories(
                        credential_id=credential_id,
                    )
                    for credential_id in ids
                )
            )
        )


class OrganizationUnreliableRepositoriesConnectionLoader(
    DataLoader[
        OrganizationIntegrationRepositoryRequest,
        OrganizationIntegrationRepositoryConnection,
    ]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[OrganizationIntegrationRepositoryRequest]
    ) -> list[OrganizationIntegrationRepositoryConnection]:
        return list(
            await collect(
                tuple(
                    _get_organization_unreliable_integration_repositories(
                        request
                    )
                    for request in requests
                )
            )
        )
