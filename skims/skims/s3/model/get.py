from ..operations import (
    download_json_fileobj,
)
from collections.abc import (
    Iterable,
)
from s3.model.types import (
    Advisory,
)
from s3.utils import (
    format_advisory_from_s3,
)
from typing import (
    Any,
)


def get_platforms(to_storage: Iterable[Advisory]) -> Iterable[str]:
    platforms = []
    for adv in to_storage:
        if adv.package_manager not in platforms:
            platforms.append(adv.package_manager)
    return platforms


async def download_advisories(
    needed_platforms: Iterable[str],
) -> list[Advisory]:
    advisories: list[Advisory] = []
    bucket_name = "skims.sca"
    for platform in needed_platforms:
        dict_obj: dict[
            str, dict[str, dict[str, Any]]
        ] = await download_json_fileobj(bucket_name, f"{platform}.json")
        for package, item in dict_obj.items():
            for cve, values in item.items():
                advisories.append(
                    await format_advisory_from_s3(
                        package, cve, values, platform
                    )
                )
    return advisories


async def download_patch_advisories(
    needed_platforms: Iterable[str],
) -> list[Advisory]:
    patch_advisories: list[Advisory] = []
    bucket_name = "skims.sca"
    for platform in needed_platforms:
        dict_patch_obj: dict[str, Any] = await download_json_fileobj(
            bucket_name, f"{platform}_patch.json"
        )
        for package, item in dict_patch_obj.items():
            for cve, values in item.items():
                patch_advisories.append(
                    await format_advisory_from_s3(
                        package, cve, values, platform
                    )
                )
    return patch_advisories
