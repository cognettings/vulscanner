# type: ignore
# pylint: disable=invalid-name
"""
Set new keys for the root environment facet.

Start Time:        2023-06-22 at 15:39:29 UTC
Finalization Time: 2023-06-22 at 15:43:50 UTC
"""

from aioextensions import (
    collect,
    run,
)
from collections import (
    defaultdict,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model import (
    TABLE,
)
from db_model.roots.constants import (
    NEW_ROOT_ENVIRONMENT_SECRET,
)
from db_model.roots.types import (
    Root,
    RootEnvironmentSecretsRequest,
    RootEnvironmentUrl,
    Secret,
)
from db_model.utils import (
    get_as_utc_iso_format,
)
from dynamodb import (
    keys,
    operations,
)
import json
from organizations import (
    domain as orgs_domain,
)
import time
from typing import (
    TypedDict,
)


class EnvInfo(TypedDict):
    group_name: str
    roots: list[Root]
    url: str


class EnvKeyData(TypedDict):
    group_name: str
    datetime: datetime


EnvConsistencyData = defaultdict[str, dict[str, EnvKeyData]]


async def _get_root_environment_urls(
    loaders: Dataloaders, root: Root
) -> list[RootEnvironmentUrl]:
    return await loaders.root_environment_urls.load(root.id)


async def _get_environment_secrets(
    loaders: Dataloaders, environment: RootEnvironmentUrl, group_name: str
) -> list[Secret]:
    return await loaders.environment_secrets.load(
        RootEnvironmentSecretsRequest(
            url_id=environment.id, group_name=group_name
        )
    )


async def _get_environment_secrets_by_environments(
    loaders: Dataloaders,
    environments: list[RootEnvironmentUrl],
    group_name: str,
) -> tuple[list[Secret], ...]:
    return await collect(
        tuple(
            _get_environment_secrets(loaders, environment, group_name)
            for environment in environments
        ),
        workers=3,
    )


async def process_environment_secret(
    environment: RootEnvironmentUrl, secret: Secret, group_name: str
) -> None:
    old_primary_key = keys.build_key(
        facet=TABLE.facets["root_environment_secret"],
        values={"hash": environment.id, "key": secret.key},
    )
    await operations.delete_item(key=old_primary_key, table=TABLE)
    key_structure = TABLE.primary_key
    new_primary_key = keys.build_key(
        facet=NEW_ROOT_ENVIRONMENT_SECRET,
        values={
            "group_name": group_name,
            "hash": environment.id,
            "key": secret.key,
        },
    )
    secret_item = {
        key_structure.partition_key: new_primary_key.partition_key,
        key_structure.sort_key: new_primary_key.sort_key,
        "key": secret.key,
        "value": secret.value,
        "description": secret.description,
        "created_at": get_as_utc_iso_format(secret.created_at)
        if secret.created_at
        else None,
    }
    await operations.put_item(
        condition_expression=None,
        facet=NEW_ROOT_ENVIRONMENT_SECRET,
        item=secret_item,
        table=TABLE,
    )


async def process_environment(
    loaders: Dataloaders,
    environment: RootEnvironmentUrl,
    group_name: str,
    environment_consistency_data: EnvConsistencyData,
) -> None:
    environment_secrets = await loaders.environment_secrets.load(
        RootEnvironmentSecretsRequest(
            url_id=environment.id, group_name=group_name
        )
    )
    if env_info := environment_consistency_data[environment.id]:
        environment_secrets = [
            secret
            for secret in environment_secrets
            if secret.key not in env_info
            or (
                secret.key in env_info
                and env_info[secret.key]["group_name"] == group_name
            )
        ]

    await collect(
        tuple(
            process_environment_secret(
                environment, environment_secret, group_name=group_name
            )
            for environment_secret in environment_secrets
        ),
        workers=3,
    )


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    environment_consistency_data: EnvConsistencyData,
) -> None:
    group_roots = await loaders.group_roots.load(group_name)
    root_and_environments = await collect(
        tuple(
            _get_root_environment_urls(loaders, root) for root in group_roots
        ),
        workers=3,
    )

    await collect(
        tuple(
            process_environment(
                loaders, environment, group_name, environment_consistency_data
            )
            for environments in root_and_environments
            for environment in environments
        ),
        workers=3,
    )
    print(f"Group processed {group_name}")


async def _get_environment_with_secrets(
    loaders: Dataloaders,
    group_name: str,
) -> defaultdict[str, EnvInfo]:
    environment_with_secrets: defaultdict[str, EnvInfo] = defaultdict(
        lambda: dict(group_name="", roots=[], url="")
    )
    group_roots = await loaders.group_roots.load(group_name)
    root_environment_urls = await collect(
        tuple(
            _get_root_environment_urls(loaders, root) for root in group_roots
        ),
        workers=3,
    )
    environment_secrets_by_environments = await collect(
        tuple(
            _get_environment_secrets_by_environments(
                loaders, environments, group_name
            )
            for environments in root_environment_urls
        ),
        workers=3,
    )
    for environments, env_secrets, root in zip(
        root_environment_urls,
        environment_secrets_by_environments,
        group_roots,
        strict=True,
    ):
        for environment, secrets in zip(
            environments, env_secrets, strict=True
        ):
            if secrets:
                environment_with_secrets[environment.id]["roots"].append(root)
                environment_with_secrets[environment.id][
                    "url"
                ] = environment.url
                environment_with_secrets[environment.id][
                    "group_name"
                ] = group_name
    return environment_with_secrets


async def _validate_environment_with_secrets_exists_in_only_one_group(
    loaders: Dataloaders,
    all_group_names: list[str],
    environment_consistency_data: EnvConsistencyData,
) -> None:
    are_duplicated_environment = False
    environments_by_group = await collect(
        [
            _get_environment_with_secrets(loaders, group_name)
            for group_name in all_group_names
        ],
        workers=10,
    )
    group_by_env_id: dict[str, list[EnvInfo]] = defaultdict(list)
    for environments in environments_by_group:
        for environment_id in environments:
            group_by_env_id[environment_id].append(
                environments[environment_id]
            )
    for environment_id, envs_with_same_id in group_by_env_id.items():
        handled_duplicated = environment_id in environment_consistency_data
        if len(envs_with_same_id) > 1 and not handled_duplicated:
            are_duplicated_environment = True
            print(f"Duplicated {environment_id}")
            for environment_info in envs_with_same_id:
                print(f" Group {environment_info['group_name']}")
                print(f" Url {environment_info['url']}")
                for root in environment_info["roots"]:
                    print("   ROOT")
                    print(f"  Root id {root.id}")
                    print(f"  Root nickname {root.state.nickname}")
            print("============================================")
    if are_duplicated_environment:
        raise Exception("Duplicated environment")


def _get_data(file_data: list[dict]) -> EnvConsistencyData:
    result: EnvConsistencyData = defaultdict(dict)
    for item in file_data:
        item_datetime = datetime.fromisoformat(item["datetime"])
        if (
            item["info"]["key"] in result[item["info"]["urlId"]]
            and item_datetime
            > result[item["info"]["urlId"]][item["info"]["key"]]["datetime"]
        ) or item["info"]["key"] not in result[item["info"]["urlId"]]:
            result[item["info"]["urlId"]][item["info"]["key"]] = {
                "group_name": item["info"]["groupName"],
                "datetime": item_datetime,
            }
    return result


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    with open(
        "path_to_file",
        mode="r",
        encoding="utf8",
    ) as file:
        env_data = _get_data(json.load(file))

    all_group_names = sorted(
        await orgs_domain.get_all_group_names(loaders=loaders)
    )
    await _validate_environment_with_secrets_exists_in_only_one_group(
        loaders, all_group_names, env_data
    )
    count = 0
    print("all_group_names", len(all_group_names))
    for group_name in all_group_names:
        count += 1
        print("group", group_name, count)
        await process_group(loaders, group_name, env_data)


if __name__ == "__main__":
    execution_time = time.strftime("Start Time:    %Y-%m-%d at %H:%M:%S UTC")
    print(execution_time)
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
