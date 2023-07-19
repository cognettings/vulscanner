from aioextensions import (
    run,
)
from collections.abc import (
    Iterable,
)
from custom_exceptions import (
    InvalidActionParameter,
    InvalidPatchItem,
    InvalidPathParameter,
    InvalidScaPatchFormat,
    UnavailabilityError,
)
from db_model.advisories.constants import (
    PATCH_SRC,
)
from dynamodb.resource import (
    dynamo_shutdown,
    dynamo_startup,
)
import json
import os
from s3.model import (
    remove,
)
from s3.model.get import (
    get_platforms,
)
from s3.model.types import (
    Advisory,
)
from s3.model.update import (
    update,
)
from s3.operations import (
    download_advisories_dict,
)
from s3.resource import (
    s3_shutdown,
    s3_start_resource,
)
import sys
from typing import (
    Any,
)
from utils.logs import (
    log_blocking,
)

Advisories = Iterable[Advisory]
ADD = "add"
REMOVE = "remove"
UPDATE = "update"


def check_item(item: dict, action: str) -> Advisory:
    if not all(
        key in item
        for key in (
            "package_name",
            "package_manager",
            "associated_advisory",
        )
    ) or (action == REMOVE and "source" not in item):
        raise InvalidPatchItem()
    if action != REMOVE and not all(
        key in item for key in ("vulnerable_version", "severity")
    ):
        raise InvalidPatchItem()
    return Advisory(
        id=item["associated_advisory"],
        package_manager=item["package_manager"],
        package_name=item["package_name"],
        source=item["source"] if action == REMOVE else PATCH_SRC,
        vulnerable_version=item.get("vulnerable_version", ""),
        severity=item.get("severity"),
        cwe_ids=item.get("cwe_ids"),
    )


def remove_from_s3(adv: Advisory, s3_advisories: dict[str, Any]) -> None:
    if (
        adv.package_manager in s3_advisories
        and adv.package_name in s3_advisories[adv.package_manager]
        and adv.id in s3_advisories[adv.package_manager][adv.package_name]
    ):
        del s3_advisories[adv.package_manager][adv.package_name][adv.id]
        if s3_advisories[adv.package_manager][adv.package_name] == {}:
            del s3_advisories[adv.package_manager][adv.package_name]


async def update_s3(
    to_storage: Iterable[Advisory],
    action: str,
    needed_platforms: Iterable[str],
) -> None:
    try:
        await s3_start_resource()
        s3_advisories, s3_patch_advisories = await download_advisories_dict(
            dl_only_patches=action != REMOVE,
            needed_platforms=needed_platforms,
        )
        if action != REMOVE:
            await update(
                to_storage,
                s3_patch_advisories,
                is_patch=True,
            )
        else:
            for adv in to_storage:
                if adv.source == PATCH_SRC:
                    remove(adv, s3_patch_advisories)
                else:
                    remove(adv, s3_advisories)
            await update(to_storage=[], s3_advisories=s3_advisories)
            await update(
                to_storage=[],
                s3_advisories=s3_patch_advisories,
                is_patch=True,
            )
    except UnavailabilityError as ex:
        log_blocking("error", "%s", ex.new())
    finally:
        await s3_shutdown()


async def patch_sca(filename: str, action: str) -> None:
    with open(filename, "r", encoding="utf-8") as stream:
        try:
            from_json: list = json.load(stream)
            if not isinstance(from_json, list):
                raise InvalidScaPatchFormat()
            items: Advisories = [
                check_item(item, action) for item in from_json
            ]

            needed_platforms = get_platforms(items)
            await update_s3(items, action, needed_platforms)
        except (
            json.JSONDecodeError,
            InvalidPatchItem,
            InvalidScaPatchFormat,
        ) as exc:
            log_blocking("error", "%s", exc.msg)


async def main() -> None:
    try:
        action = sys.argv[1]
        if action not in (ADD, UPDATE, REMOVE):
            raise InvalidActionParameter()
        path = sys.argv[2]
        if not os.path.exists(path):
            raise InvalidPathParameter()

        await dynamo_startup()
        await patch_sca(path, action)
    except (InvalidActionParameter, InvalidPathParameter) as exc:
        log_blocking("error", "%s", exc.msg)
    finally:
        await dynamo_shutdown()


if __name__ == "__main__":
    run(main())
