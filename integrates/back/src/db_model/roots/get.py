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
from context import (
    FI_AWS_S3_CONTINUOUS_REPOSITORIES,
    FI_AWS_S3_PATH_PREFIX,
)
from datetime import (
    datetime,
)
from db_model import (
    TABLE,
)
from db_model.roots.constants import (
    ORG_INDEX_METADATA,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRootCloning,
    Root,
    RootEnvironmentCloud,
    RootEnvironmentSecretsRequest,
    RootEnvironmentUrl,
    RootEnvironmentUrlType,
    RootRequest,
    RootState,
    Secret,
)
from db_model.roots.utils import (
    format_cloning,
    format_root,
)
from dynamodb import (
    keys,
    operations,
)
from itertools import (
    chain,
)
from s3.operations import (
    file_exists,
)
from s3.resource import (
    get_s3_resource,
)


async def _get_roots(*, requests: Iterable[RootRequest]) -> list[Root]:
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["git_root_metadata"],
            values={"name": request.group_name, "uuid": request.root_id},
        )
        for request in requests
    )
    items = await operations.batch_get_item(keys=primary_keys, table=TABLE)

    return [format_root(item) for item in items]


class RootLoader(DataLoader[RootRequest, Root | None]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[RootRequest]
    ) -> list[Root | None]:
        roots = {root.id: root for root in await _get_roots(requests=requests)}

        return [roots.get(request.root_id) for request in requests]


async def _get_group_roots(
    *,
    group_name: str,
    root_dataloader: RootLoader,
) -> list[Root]:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={"name": group_name},
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
        facets=(
            TABLE.facets["git_root_metadata"],
            TABLE.facets["ip_root_metadata"],
            TABLE.facets["url_root_metadata"],
        ),
        index=index,
        table=TABLE,
    )

    roots: list[Root] = []
    for item in response.items:
        root = format_root(item)
        roots.append(root)
        root_dataloader.prime(
            RootRequest(group_name=root.group_name, root_id=root.id), root
        )

    return roots


class GroupRootsLoader(DataLoader[str, list[Root]]):
    def __init__(self, dataloader: RootLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    async def load_many_chained(
        self, group_names: Iterable[str]
    ) -> list[Root]:
        unchained_data = await self.load_many(group_names)
        return list(chain.from_iterable(unchained_data))

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> list[list[Root]]:
        return list(
            await collect(
                _get_group_roots(
                    group_name=group_name, root_dataloader=self.dataloader
                )
                for group_name in group_names
            )
        )


async def _get_organization_roots(
    *,
    organization_name: str,
    root_dataloader: RootLoader,
) -> list[Root]:
    primary_key = keys.build_key(
        facet=ORG_INDEX_METADATA,
        values={"name": organization_name},
    )

    index = TABLE.indexes["gsi_2"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(
            TABLE.facets["git_root_metadata"],
            TABLE.facets["ip_root_metadata"],
            TABLE.facets["url_root_metadata"],
        ),
        index=index,
        table=TABLE,
    )

    roots: list[Root] = []
    for item in response.items:
        root = format_root(item)
        roots.append(root)
        root_dataloader.prime(
            RootRequest(group_name=root.group_name, root_id=root.id), root
        )

    return roots


class OrganizationRootsLoader(DataLoader[str, list[Root]]):
    def __init__(self, dataloader: RootLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, organization_names: Iterable[str]
    ) -> list[list[Root]]:
        return list(
            await collect(
                _get_organization_roots(
                    organization_name=organization_name,
                    root_dataloader=self.dataloader,
                )
                for organization_name in organization_names
            )
        )


async def _get_historic_state(*, root_id: str) -> list[RootState]:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_historic_state"],
        values={"uuid": root_id},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(
            TABLE.facets["git_root_historic_state"],
            TABLE.facets["ip_root_historic_state"],
            TABLE.facets["url_root_historic_state"],
        ),
        table=TABLE,
    )

    return [
        RootState(
            modified_by=state["modified_by"],
            modified_date=datetime.fromisoformat(state["modified_date"]),
            nickname=state.get("nickname"),
            other=state.get("other"),
            reason=state.get("reason"),
            status=RootStatus[state["status"]],
        )
        for state in response.items
    ]


class RootHistoricStatesLoader(DataLoader[str, list[RootState]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, root_ids: Iterable[str]
    ) -> list[list[RootState]]:
        return list(
            await collect(
                _get_historic_state(root_id=root_id) for root_id in root_ids
            )
        )


async def _get_historic_cloning(*, root_id: str) -> list[GitRootCloning]:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_historic_cloning"],
        values={"uuid": root_id},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["git_root_historic_cloning"],),
        table=TABLE,
    )

    return [format_cloning(state) for state in response.items]


class RootHistoricCloningLoader(DataLoader[str, list[GitRootCloning]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, root_ids: Iterable[str]
    ) -> list[list[GitRootCloning]]:
        return list(
            await collect(
                _get_historic_cloning(root_id=root_id) for root_id in root_ids
            )
        )


async def get_download_url(group_name: str, root_nickname: str) -> str | None:
    object_name = f"{group_name}/{root_nickname}.tar.gz"
    object_key = f"{FI_AWS_S3_PATH_PREFIX}{object_name}"
    client = await get_s3_resource()
    if not await file_exists(
        object_key, bucket=FI_AWS_S3_CONTINUOUS_REPOSITORIES
    ):
        return None

    return await client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": FI_AWS_S3_CONTINUOUS_REPOSITORIES,
            "Key": object_key,
        },
        ExpiresIn=1800,
    )


async def get_upload_url(group_name: str, root_nickname: str) -> str | None:
    object_name = f"{group_name}/{root_nickname}.tar.gz"
    client = await get_s3_resource()
    return await client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": FI_AWS_S3_CONTINUOUS_REPOSITORIES,
            "Key": f"{FI_AWS_S3_PATH_PREFIX}{object_name}",
        },
        ExpiresIn=1800,
    )


async def get_upload_url_post(
    group_name: str, root_nickname: str
) -> tuple[str, dict[str, str]]:
    object_name = f"{group_name}/{root_nickname}.tar.gz"
    client = await get_s3_resource()
    response = await client.generate_presigned_post(
        FI_AWS_S3_CONTINUOUS_REPOSITORIES,
        f"{FI_AWS_S3_PATH_PREFIX}{object_name}",
        ExpiresIn=1800,
    )

    return response["url"], response["fields"]


async def _get_secrets(
    *, root_id: str, secret_key: str | None = None
) -> list[Secret]:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_secret"],
        values={
            "uuid": root_id,
            **({"key": secret_key} if secret_key else {}),
        },
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & (
                Key(key_structure.sort_key).eq(primary_key.sort_key)
                if secret_key
                else Key(key_structure.sort_key).begins_with(
                    primary_key.sort_key
                )
            )
        ),
        facets=(TABLE.facets["root_secret"],),
        table=TABLE,
    )

    return [
        Secret(
            key=item["key"],
            value=item["value"],
            description=item.get("description"),
        )
        for item in response.items
    ]


class RootSecretsLoader(DataLoader[str, list[Secret]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        root_ids: Iterable[str],
    ) -> list[list[Secret]]:
        return list(
            await collect(
                _get_secrets(root_id=root_id) for root_id in root_ids
            )
        )


async def _get_environment_secrets(
    *, request: RootEnvironmentSecretsRequest
) -> list[Secret]:
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["root_environment_secret"],
        values={
            "group_name": request.group_name,
            "hash": request.url_id,
        },
    )
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["root_environment_secret"],),
        table=TABLE,
    )
    return [
        Secret(
            key=item["key"],
            value=item["value"],
            description=item.get("description"),
            created_at=datetime.fromisoformat(item["created_at"])
            if "created_at" in item
            else None,
        )
        for item in response.items
    ]


class GitEnvironmentSecretsLoader(
    DataLoader[RootEnvironmentSecretsRequest, list[Secret]]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[RootEnvironmentSecretsRequest]
    ) -> list[list[Secret]]:
        return list(
            await collect(
                _get_environment_secrets(request=request)
                for request in requests
            )
        )

    async def load_many_chained(
        self, requests: Iterable[RootEnvironmentSecretsRequest]
    ) -> list[Secret]:
        unchained_data = await self.load_many(requests)
        return list(chain.from_iterable(unchained_data))


async def _get_git_environment_urls(
    *, root_id: str, url_id: str | None = None
) -> list[RootEnvironmentUrl]:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_environment_url"],
        values={
            "uuid": root_id,
            **({"hash": url_id} if url_id else {}),
        },
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & (
                Key(key_structure.sort_key).eq(primary_key.sort_key)
                if url_id
                else Key(key_structure.sort_key).begins_with(
                    primary_key.sort_key
                )
            )
        ),
        facets=(TABLE.facets["root_environment_url"],),
        table=TABLE,
    )
    return [
        RootEnvironmentUrl(
            url=item["url"],
            id=item["sk"].split("URL#")[-1],
            created_at=datetime.fromisoformat(item["created_at"])
            if "created_at" in item
            else None,
            created_by=item.get("created_by", None),
            url_type=RootEnvironmentUrlType[item["type"]]
            if "type" in item
            else RootEnvironmentUrlType.URL,
            cloud_name=RootEnvironmentCloud[item["cloud_name"]]
            if "cloud_name" in item
            else None,
        )
        for item in response.items
    ]


class RootEnvironmentUrlsLoader(DataLoader[str, list[RootEnvironmentUrl]]):
    async def load_many_chained(
        self, root_ids: Iterable[str]
    ) -> list[RootEnvironmentUrl]:
        unchained_data = await self.load_many(root_ids)
        return list(chain.from_iterable(unchained_data))

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, root_ids: Iterable[str]
    ) -> list[list[RootEnvironmentUrl]]:
        return list(
            await collect(
                _get_git_environment_urls(root_id=root_id)
                for root_id in root_ids
            )
        )


async def get_git_environment_url_by_id(
    *, url_id: str, root_id: str | None = None
) -> RootEnvironmentUrl | None:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_environment_url"],
        values={
            "hash": url_id,
            **({"uuid": root_id} if root_id else {}),
        },
    )
    index = TABLE.indexes["inverted_index"]
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.sort_key).eq(primary_key.sort_key)
            & (
                Key(key_structure.partition_key).eq(primary_key.partition_key)
                if root_id
                else Key(key_structure.partition_key).begins_with(
                    primary_key.partition_key
                )
            )
        ),
        facets=(TABLE.facets["root_environment_url"],),
        table=TABLE,
        index=index,
    )
    if not response.items:
        return None
    item = response.items[0]
    return RootEnvironmentUrl(
        url=item["url"],
        id=item["sk"].split("URL#")[-1],
        created_at=datetime.fromisoformat(item["created_at"])
        if "created_at" in item
        else None,
        created_by=item.get("created_by", None),
        url_type=RootEnvironmentUrlType[item["type"]],
        cloud_name=RootEnvironmentCloud[item["cloud_name"]]
        if "cloud_name" in item
        else None,
    )
