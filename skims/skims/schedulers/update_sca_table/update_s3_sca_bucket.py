from .repositories.advisories_community import (
    get_advisories_community,
    URL_ADVISORIES_COMMUNITY,
)
from .repositories.advisory_database import (
    get_advisory_database,
    URL_ADVISORY_DATABASE,
)
from collections.abc import (
    Callable,
)
from git.exc import (
    GitError,
)
from git.repo import (
    Repo,
)
from s3.model import (
    add,
)
from s3.model.types import (
    Advisory,
)
from s3.resource import (
    s3_shutdown,
    s3_start_resource,
)
from tempfile import (
    TemporaryDirectory,
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


def fix_advisories(advisories: list[Advisory]) -> list[Advisory]:
    fixed_advisories = []
    for advisory in advisories:
        versions = advisory.vulnerable_version.split(" || ")
        if ">=0" in versions and len(versions) > 1:
            fixed_vers = [ver for ver in versions if ver != ">=0"]
            fixed_advisories.append(
                advisory._replace(vulnerable_version=" || ".join(fixed_vers))
            )
        else:
            fixed_advisories.append(advisory)
    return fixed_advisories


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


async def update_sca() -> None:
    log_blocking("info", "Cloning necessary repositories")
    tmp_repositories = [
        (fun, repo) for fun, url in REPOSITORIES if (repo := clone_repo(url))
    ]

    advisories: Advisories = []
    log_blocking("info", "Processing advisories")
    for get_ad, repo in tmp_repositories:
        get_ad(advisories, repo)

    fixed_advisories = fix_advisories(advisories)
    log_blocking("info", "Adding advisories to skims.sca bucket")
    await s3_start_resource()
    await add(fixed_advisories)
    await s3_shutdown()


async def main() -> None:
    await update_sca()
