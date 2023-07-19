# pylint: disable=invalid-name
"""
Refresh code snippet in all LINES vulns that apply.

Start Time:    2023-07-18 at 04:42:32 UTC
Finalization Time: 2023-07-18 at 09:47:09 UTC

Start Time:    2023-07-18 at 22:18:27 UTC
Finalization Time: 2023-07-19 at 00:35:31 UTC
"""

from aioextensions import (
    collect,
    run,
)
from batch_dispatch.utils.s3 import (
    download_repo,
)
from custom_exceptions import (
    GroupNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    Source,
)
from db_model.groups.enums import (
    GroupService,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from git.repo import (
    Repo,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
import os
from settings import (
    LOGGING,
)
import tempfile
import time
from vulnerabilities.domain.snippet import (
    generate_snippet,
    set_snippet,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_vulnerability(
    vulnerability: Vulnerability, repo: Repo
) -> None:
    snippet = generate_snippet(vulnerability.state, repo)
    if snippet and snippet.content:
        await set_snippet(vulnerability, snippet)


async def process_root(
    loaders: Dataloaders,
    root: GitRoot,
    finding_ids: list[str],
) -> None:
    print(f"{root.id=} {root.state.nickname=}")
    try:
        vulns = await loaders.root_vulnerabilities.load(root.id)
        vulns_to_update = [
            vuln
            for vuln in vulns
            if vuln.finding_id in finding_ids
            and vuln.state.status == VulnerabilityStateStatus.VULNERABLE
            and vuln.state.source == Source.MACHINE
            and vuln.type == VulnerabilityType.LINES
        ]
        vulns_snippet_to_update = [
            vuln
            for vuln in vulns_to_update
            if not vuln.state.snippet or not vuln.state.snippet.content
        ]
        if not vulns_snippet_to_update:
            return

        with tempfile.TemporaryDirectory(
            prefix="integrates_rebase_root_", ignore_cleanup_errors=True
        ) as tmpdir:
            os.chdir(tmpdir)
            repo_path = os.path.join(tmpdir, root.state.nickname)
            if not (
                repo := await download_repo(
                    root.group_name,
                    root.state.nickname,
                    tmpdir,
                    root.state.gitignore,
                )
            ):
                print(
                    f"REPO not found {root.group_name=} {root.id=} "
                    f"{repo_path=}"
                )
                return

            os.chdir(repo_path)
            await collect(
                tuple(
                    process_vulnerability(vuln, repo)
                    for vuln in vulns_snippet_to_update
                ),
                workers=64,
            )
    except KeyError as ex:
        print(f"[ERROR] Format exception: {ex}")


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    group = await loaders.group.load(group_name)
    if not group:
        raise GroupNotFound()
    group_findings = await loaders.group_findings.load(group_name)
    findings_filtered = [
        finding.id
        for finding in group_findings
        if finding.state.status
        and any(finding.title.startswith(code) for code in ["011", "393"])
    ]
    if not findings_filtered:
        return

    roots = tuple(
        root
        for root in await loaders.group_roots.load(group_name)
        if isinstance(root, GitRoot) and root.state.status == RootStatus.ACTIVE
    )
    if not roots:
        return

    await collect(
        tuple(
            process_root(loaders, root, findings_filtered) for root in roots
        ),
        workers=1,
    )
    print(f"Group processed {group_name} {str(round(progress, 2))}")


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = await orgs_domain.get_all_active_groups(loaders)
    machine_group_names = sorted(
        group.name
        for group in groups
        if group.state.has_machine is True
        and group.state.service == GroupService.WHITE
    )
    print(f"{machine_group_names=}")
    print(f"{len(machine_group_names)=}")
    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group,
                progress=count / len(machine_group_names),
            )
            for count, group in enumerate(machine_group_names)
        ),
        workers=1,
    )


if __name__ == "__main__":
    execution_time = time.strftime("Start Time:    %Y-%m-%d at %H:%M:%S UTC")
    print(execution_time)
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
