# type: ignore
# pylint: disable=invalid-name
"""
Remove whitespaces from existing EnvironmentUrls, or values that do not begin
with http:// or https://

Start Time:         UTC
Finalization Time:  UTC
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
from db_model.roots.types import (
    Root,
    RootEnvironmentUrl,
)
from dynamodb import (
    keys,
    operations,
)
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


def update_url(url: str):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    if " " in url:
        url = (url.split(" "))[0]

    return url


async def update_git_environment_urls(
    root_id: str,
    url: RootEnvironmentUrl,
) -> None:
    url_key = keys.build_key(
        facet=TABLE.facets["root_environment_url"],
        values={"uuid": root_id, "hash": url.id},
    )

    new_url = update_url(url.url)
    url_item = {"url": new_url}

    await operations.update_item(
        item=url_item,
        key=url_key,
        table=TABLE,
    )


async def _get_root_environment_urls(
    loaders: Dataloaders, root: Root
) -> list[RootEnvironmentUrl]:
    return await loaders.root_environment_urls.load(root.id)


async def _get_environment(
    loaders: Dataloaders,
    group_name: str,
) -> defaultdict[str, EnvInfo]:
    group_roots = await loaders.group_roots.load(group_name)

    for root in group_roots:
        urls = await _get_root_environment_urls(loaders, root)
        if urls:
            for url in urls:
                if (
                    url.url_type == "URL"
                    and " " in url.url
                    or not url.url.startswith(("http://", "https://"))
                ):
                    await update_git_environment_urls(root.id, url)


async def _get_environment_by_group(
    loaders: Dataloaders,
    all_group_names: list[str],
) -> None:
    await collect(
        [
            _get_environment(loaders, group_name)
            for group_name in all_group_names
        ],
        workers=10,
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()

    all_group_names = sorted(
        await orgs_domain.get_all_group_names(loaders=loaders)
    )
    await _get_environment_by_group(loaders, all_group_names)


if __name__ == "__main__":
    execution_time = time.strftime("Start Time:    %Y-%m-%d at %H:%M:%S UTC")
    print(execution_time)
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
