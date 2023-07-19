from .types import (
    OrganizationAccess,
    OrganizationAccessRequest,
)
from .utils import (
    format_organization_access,
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


async def _get_organization_access(
    *, requests: Iterable[OrganizationAccessRequest]
) -> list[OrganizationAccess | None]:
    requests_formatted = [
        request._replace(email=request.email.lower().strip())
        for request in requests
    ]
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["organization_access"],
            values={
                "email": request.email,
                "id": remove_org_id_prefix(request.organization_id),
            },
        )
        for request in requests_formatted
    )
    items = await operations.batch_get_item(keys=primary_keys, table=TABLE)
    response = {
        OrganizationAccessRequest(
            organization_id=access.organization_id, email=access.email
        ): access
        for access in [format_organization_access(item) for item in items]
    }

    return list(response.get(request) for request in requests_formatted)


class OrganizationAccessLoader(
    DataLoader[OrganizationAccessRequest, OrganizationAccess | None]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[OrganizationAccessRequest]
    ) -> list[OrganizationAccess | None]:
        return await _get_organization_access(requests=requests)


async def _get_organization_stakeholders_access(
    *,
    access_dataloader: OrganizationAccessLoader,
    organization_id: str,
) -> list[OrganizationAccess]:
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_access"],
        values={
            "id": remove_org_id_prefix(organization_id),
        },
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["organization_access"],),
        table=TABLE,
        index=index,
    )

    access_list: list[OrganizationAccess] = []
    for item in response.items:
        access = format_organization_access(item)
        access_list.append(access)
        access_dataloader.prime(
            OrganizationAccessRequest(
                organization_id=organization_id, email=access.email
            ),
            access,
        )

    return access_list


class OrganizationStakeholdersAccessLoader(
    DataLoader[str, list[OrganizationAccess]]
):
    def __init__(self, dataloader: OrganizationAccessLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, organization_ids: Iterable[str]
    ) -> list[list[OrganizationAccess]]:
        return list(
            await collect(
                tuple(
                    _get_organization_stakeholders_access(
                        access_dataloader=self.dataloader,
                        organization_id=organization_id,
                    )
                    for organization_id in organization_ids
                )
            )
        )


async def _get_stakeholder_organizations_access(
    *,
    access_dataloader: OrganizationAccessLoader,
    email: str,
) -> list[OrganizationAccess]:
    email = email.lower().strip()
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_access"],
        values={
            "email": email,
        },
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["organization_access"],),
        table=TABLE,
    )

    access_list: list[OrganizationAccess] = []
    for item in response.items:
        access = format_organization_access(item)
        access_list.append(access)
        access_dataloader.prime(
            OrganizationAccessRequest(
                organization_id=access.organization_id, email=email
            ),
            access,
        )

    return access_list


class StakeholderOrganizationsAccessLoader(
    DataLoader[str, list[OrganizationAccess]]
):
    def __init__(self, dataloader: OrganizationAccessLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, emails: Iterable[str]
    ) -> list[list[OrganizationAccess]]:
        return list(
            await collect(
                tuple(
                    _get_stakeholder_organizations_access(
                        access_dataloader=self.dataloader,
                        email=email,
                    )
                    for email in emails
                )
            )
        )
