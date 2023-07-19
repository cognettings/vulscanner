from collections.abc import (
    Callable,
)
from custom_exceptions import (
    UnavailabilityError,
)
from db_model import (
    advisories as advisories_model,
)
from db_model.advisories.constants import (
    PATCH_SRC,
)
from db_model.advisories.get import (
    AllAdvisoriesLoader,
)
from dynamodb.types import (
    Item,
)
from git.exc import (
    GitError,
)
from git.repo import (
    Repo,
)
from operator import (
    attrgetter,
)
from s3.model.get import (
    get_platforms,
)
from s3.model.types import (
    Advisory,
)
from s3.operations import (
    download_advisories_dict,
    upload_advisories,
)
from s3.resource import (
    s3_shutdown,
    s3_start_resource,
)
from schedulers.update_sca_table.repositories.advisories_community import (
    get_advisories_community,
    URL_ADVISORIES_COMMUNITY,
)
from schedulers.update_sca_table.repositories.advisory_database import (
    get_advisory_database,
    URL_ADVISORY_DATABASE,
)
from semantic_version import (
    NpmSpec,
)
from semver_match_tools.semver_match import (
    coerce_range,
)
from tempfile import (
    TemporaryDirectory,
)
from typing import (
    Iterable,
)
from utils.logs import (
    log_blocking,
)

Advisories = list[Advisory]

REPOSITORIES: list[tuple[Callable[[Advisories, str], None], str]] = [
    (
        get_advisories_community,
        URL_ADVISORIES_COMMUNITY,
    ),
    (
        get_advisory_database,
        URL_ADVISORY_DATABASE,
    ),
]


def clone_repo(url: str) -> str | None:
    # pylint: disable=consider-using-with
    tmp_dirname = TemporaryDirectory().name
    try:
        print(f"cloning {url}")
        Repo.clone_from(url, tmp_dirname, depth=1)
    except GitError as error:
        log_blocking("error", f"Error cloning repository: {url}")
        print(error)
        return None
    return tmp_dirname


def remove_from_s3(adv: Advisory, s3_advisories: Item) -> None:
    if (
        adv.package_manager in s3_advisories
        and adv.package_name in s3_advisories[adv.package_manager]
        and adv.id in s3_advisories[adv.package_manager][adv.package_name]
    ):
        del s3_advisories[adv.package_manager][adv.package_name][adv.id]
        if s3_advisories[adv.package_manager][adv.package_name] == {}:
            del s3_advisories[adv.package_manager][adv.package_name]


async def update_s3(
    to_delete: list[Advisory], needed_platforms: Iterable[str]
) -> None:
    try:
        await s3_start_resource()
        s3_advisories, s3_patch_advisories = await download_advisories_dict(
            needed_platforms=needed_platforms,
        )

        for adv in to_delete:
            if adv.source == PATCH_SRC:
                remove_from_s3(adv, s3_patch_advisories)
            else:
                remove_from_s3(adv, s3_advisories)
        await upload_advisories(to_storage=[], s3_advisories=s3_advisories)
        await upload_advisories(
            to_storage=[],
            s3_advisories=s3_patch_advisories,
            is_patch=True,
        )
    except UnavailabilityError as ex:
        log_blocking("error", "%s", ex.new())
    finally:
        await s3_shutdown()


def compare_version(patch_ver: str, ext_ver: str) -> bool:
    try:
        if (
            NpmSpec(coerce_range(patch_ver)).clause
            == NpmSpec(coerce_range(ext_ver)).clause
        ):
            return True
        return False
    except ValueError:
        log_blocking(
            "error",
            "Semver match %s to %s : Invalid semver version",
            patch_ver,
            ext_ver,
        )
        return False


async def clean_manual_sca(
    ext_sources_advisories: Advisories, manual_source_advisories: Advisories
) -> None:
    key_function = attrgetter("id", "package_manager", "package_name")
    to_delete = []
    for patch_adv in manual_source_advisories:
        for ext_adv in ext_sources_advisories:
            if key_function(patch_adv) == key_function(
                ext_adv
            ) and compare_version(
                patch_adv.vulnerable_version, ext_adv.vulnerable_version
            ):
                to_delete.append(patch_adv)
                await advisories_model.batch_remove(
                    advisory_id=patch_adv.id,
                    pkg_name=patch_adv.package_name,
                    platform=patch_adv.package_manager,
                    source=patch_adv.source,
                )
    log_blocking("info", f"{len(to_delete)} Manual items to delete")
    needed_platforms = get_platforms(to_delete)
    await update_s3(to_delete, needed_platforms)


async def clean_dynamo_sca(
    ext_sources_advisories: Advisories, sources_advisories: Advisories
) -> None:
    sources_advisories_cve = [adv.id for adv in sources_advisories]
    to_delete = []
    for advisor in ext_sources_advisories:
        if advisor.id not in sources_advisories_cve or advisor.id.startswith(
            "GMS"
        ):
            to_delete.append(advisor)
            await advisories_model.batch_remove(
                advisory_id=advisor.id,
                pkg_name=advisor.package_name,
                platform=advisor.package_manager,
                source=advisor.source,
            )
    log_blocking("info", f"{len(to_delete)} external source items to delete")
    needed_platforms = get_platforms(to_delete)
    await update_s3(to_delete, needed_platforms)


async def clean_sca() -> None:
    log_blocking("info", "Cloning necessary repositories")
    tmp_repositories = [
        (fun, repo) for fun, url in REPOSITORIES if (repo := clone_repo(url))
    ]

    sources_advisories: Advisories = []
    log_blocking("info", "Processing advisories")
    for get_ad, repo in tmp_repositories:
        get_ad(sources_advisories, repo)
    log_blocking("info", f"{len(sources_advisories)} processed")

    log_blocking("info", "Scanning sca_table items")
    all_db_advisories: Iterable[Advisory] = await AllAdvisoriesLoader().load(
        ""
    )

    ext_sources_advisories = [
        advisory
        for advisory in all_db_advisories
        if advisory.source != PATCH_SRC
    ]
    manual_source_advisories = [
        advisory
        for advisory in all_db_advisories
        if advisory.source == PATCH_SRC
    ]
    await clean_dynamo_sca(ext_sources_advisories, sources_advisories)
    await clean_manual_sca(ext_sources_advisories, manual_source_advisories)


async def main() -> None:
    await clean_sca()
