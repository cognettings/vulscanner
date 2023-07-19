from ..utils import (
    format_advisory,
    print_exc,
)
from collections.abc import (
    Iterable,
)
from custom_exceptions import (
    AdvisoryAlreadyCreated,
    InvalidSeverity,
    InvalidVulnerableVersion,
    UnavailabilityError,
)
from s3.model.types import (
    Advisory,
)
from s3.operations import (
    upload_object,
)
from typing import (
    Any,
)
from utils.logs import (
    log_blocking,
)

ACTION = "added"


async def _update(
    adv: Advisory,
    s3_advisories: dict[str, Any],
) -> None:
    adv = format_advisory(adv)
    if adv.package_manager not in s3_advisories:
        s3_advisories.update({adv.package_manager: {}})
    if adv.package_name not in s3_advisories[adv.package_manager]:
        s3_advisories[adv.package_manager].update({adv.package_name: {}})
    s3_advisories[adv.package_manager][adv.package_name].update(
        {
            adv.id: {
                "source": adv.source,
                "created": adv.created_at,
                "modified": adv.modified_at,
                "vulnerable_version": adv.vulnerable_version,
                "cvss": adv.severity,
                "cwe_ids": adv.cwe_ids,
            }
        }
    )


async def update(
    to_storage: Iterable[Advisory],
    s3_advisories: dict[str, Any],
    is_patch: bool = False,
) -> None:
    for adv in to_storage:
        try:
            await _update(adv, s3_advisories)
            for key, value in s3_advisories.items():
                await upload_object(
                    bucket="skims.sca",
                    dict_object=value,
                    file_name=f"{key}{'_patch' if is_patch else ''}.json",
                )
        except UnavailabilityError as ex:
            log_blocking("error", "%s", ex.new())
        except (InvalidVulnerableVersion,) as exc:
            print_exc(exc, ACTION, adv, f" ({adv.vulnerable_version})")
        except (InvalidSeverity,) as exc:
            print_exc(exc, ACTION, adv, f" ({adv.severity})")
        except (AdvisoryAlreadyCreated,) as exc:
            print_exc(exc, ACTION, adv)
