from db_model.advisories.constants import (
    SUPPORTED_PLATFORMS,
)
from model import (
    core,
)
from s3.model.get import (
    download_advisories,
    download_patch_advisories,
)
from s3.model.types import (
    Advisory,
)
from s3.resource import (
    s3_shutdown,
    s3_start_resource,
)
from semver_match_tools.semver_match import (
    semver_match,
)
from utils.logs import (
    log_blocking,
)

DATABASE: list[Advisory] | None = None
DATABASE_PATCH: list[Advisory] | None = None


def format_advisories_from_s3(
    ads: list[Advisory],
    patch_ads: list[Advisory],
) -> list[Advisory]:
    ads = [] if not ads else ads
    ads_dict = {advisory.id: advisory for advisory in ads}

    for advisory in patch_ads:
        if advisory.id in ads_dict:
            ads.remove(ads_dict[advisory.id])
            ads.append(
                advisory._replace(severity=ads_dict[advisory.id].severity)
            )
        else:
            ads.append(advisory)

    no_gms_ads = [adv for adv in ads if not adv.id.startswith("GMS")]
    return no_gms_ads


async def get_advisories_from_s3(
    pkg_name: str, platform: str
) -> list[Advisory] | None:
    try:
        # pylint: disable=global-statement
        global DATABASE, DATABASE_PATCH
        if DATABASE is None or DATABASE_PATCH is None:
            await s3_start_resource(is_public=True)
            s3_advisories: list[Advisory] = await download_advisories(
                SUPPORTED_PLATFORMS
            )
            s3_patch_advisories = await download_patch_advisories(
                SUPPORTED_PLATFORMS
            )
            DATABASE = s3_advisories
            DATABASE_PATCH = s3_patch_advisories
            await s3_shutdown()
        ads = [
            adv
            for adv in DATABASE
            if adv.package_manager == platform and adv.package_name == pkg_name
        ]
        patch_ads = [
            adv
            for adv in DATABASE_PATCH
            if adv.package_manager == platform and adv.package_name == pkg_name
        ]
        return format_advisories_from_s3(ads, patch_ads)
    except Exception:  # pylint: disable=broad-except
        log_blocking(
            "error",
            "Couldn't download advisories from s3 bucket",
        )
        return None


async def get_remote_advisories(
    pkg_name: str, platform: str
) -> list[Advisory] | None:
    if (
        s3_advisories := await get_advisories_from_s3(
            pkg_name, platform.lower()
        )
    ) is not None:
        return s3_advisories
    return None


async def get_vulnerabilities(
    platform: core.Platform,
    product: str | None,
    version: str | None,
) -> list[Advisory]:
    vulnerabilities = []
    product = product.lower() if product else None
    version = version.lower() if isinstance(version, str) else ""
    platform_val: str = platform.value

    if product and (
        advisories := await get_remote_advisories(
            product, platform_val.lower()
        )
    ):
        vulnerabilities = [
            advisor
            for advisor in advisories
            if semver_match(version, advisor.vulnerable_version)
        ]

    return vulnerabilities
