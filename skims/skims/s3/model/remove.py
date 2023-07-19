from s3.model.types import (
    Advisory,
)
from typing import (
    Any,
)


def remove(adv: Advisory, s3_advisories: dict[str, Any]) -> None:
    if (
        adv.package_manager in s3_advisories
        and adv.package_name in s3_advisories[adv.package_manager]
        and adv.id in s3_advisories[adv.package_manager][adv.package_name]
    ):
        del s3_advisories[adv.package_manager][adv.package_name][adv.id]
        if s3_advisories[adv.package_manager][adv.package_name] == {}:
            del s3_advisories[adv.package_manager][adv.package_name]
