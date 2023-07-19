from aioextensions import (
    collect,
)
from batch.dal import (
    delete_action,
)
from batch.types import (
    BatchProcessing,
)
from batch_dispatch.utils.s3 import (
    download_repo,
)
from botocore.exceptions import (
    ClientError,
)
from concurrent.futures import (
    ThreadPoolExecutor,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    InvalidVulnerabilityAlreadyExists,
    LineDoesNotExistInTheLinesOfCodeRange,
    VulnerabilityPathDoesNotExistInToeLines,
    VulnerabilityUrlFieldDoNotExistInToeInputs,
    VulnNotFound,
)
from custom_utils.utils import (
    get_advisories,
    ignore_advisories,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
    RootRequest,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
)
from git.exc import (
    GitError,
)
from git.repo.base import (
    Repo,
)
import git_self as git_utils
import json
import logging
import logging.config
import os
from roots import (
    domain as roots_domain,
)
from settings import (
    LOGGING,
)
from sqs.resources import (
    get_sqs_resource,
)
import tempfile
from vulnerabilities.domain import (
    get_vulnerabilities,
)
from vulnerabilities.domain.rebase import (
    close_vulnerability,
    rebase as rebase_vulnerability,
)
from vulnerabilities.domain.snippet import (
    generate_snippet,
    set_snippet,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def _get_vulnerabilities_to_rebase(
    loaders: Dataloaders,
    group_name: str,
    git_root: GitRoot,
) -> tuple[Vulnerability, ...]:
    findings = await loaders.group_findings.load(group_name)
    findings_vulns = await loaders.finding_vulnerabilities.load_many(
        [find.id for find in findings if "117." not in find.title]
    )
    vulnerabilities: tuple[Vulnerability, ...] = tuple(
        vuln
        for vulns in findings_vulns
        for vuln in vulns
        if vuln.root_id == git_root.id
        and vuln.state.commit is not None
        and vuln.type == VulnerabilityType.LINES
        and vuln.state.status
        in (
            VulnerabilityStateStatus.REJECTED,
            VulnerabilityStateStatus.SUBMITTED,
            VulnerabilityStateStatus.VULNERABLE,
        )
    )
    return vulnerabilities


def _rebase_vulnerability(
    repo: Repo,
    vulnerability: Vulnerability,
    states: tuple[VulnerabilityState, ...],
) -> git_utils.RebaseResult | None:
    try:
        if (
            states[0].commit
            and states[0].commit != "0000000000000000000000000000000000000000"
            and (
                result := git_utils.rebase(
                    repo,
                    path=ignore_advisories(states[0].where),
                    line=int(states[0].specific),
                    rev_a=states[0].commit,
                    rev_b="HEAD",
                )
            )
        ):
            if (
                ignore_advisories(
                    vulnerability.state.where,
                )
                != vulnerability.state.where
            ):
                advisories = get_advisories(vulnerability.state.where)
                if advisories and advisories not in result.path:
                    result = result._replace(
                        path=f"{result.path} {advisories}"
                    )
            return result
    except GitError as exc:
        LOGGER.error(
            "Failed to rebase vulnerability",
            extra=dict(extra={"vuln_id": vulnerability.id, "exception": exc}),
        )
    return None


async def _rebase_vulnerability_integrates(
    *,
    loaders: Dataloaders,
    finding_id: str,
    finding_vulns_data: tuple[Vulnerability, ...],
    vulnerability_commit: str,
    vulnerability_id: str,
    vulnerability_where: str,
    vulnerability_specific: str,
    vulnerability_type: VulnerabilityType,
) -> None:
    local_vars = locals()
    with suppress(InvalidVulnerabilityAlreadyExists, VulnNotFound):
        try:
            await rebase_vulnerability(
                loaders=loaders,
                finding_id=finding_id,
                finding_vulns_data=finding_vulns_data,
                vulnerability_commit=vulnerability_commit,
                vulnerability_id=vulnerability_id,
                vulnerability_where=vulnerability_where,
                vulnerability_specific=vulnerability_specific,
                vulnerability_type=vulnerability_type,
            )
        except (
            VulnerabilityPathDoesNotExistInToeLines,
            LineDoesNotExistInTheLinesOfCodeRange,
            VulnerabilityUrlFieldDoNotExistInToeInputs,
        ) as exception:
            local_vars.pop("loaders", None)
            local_vars.pop("finding_vulns_data", None)
            LOGGER.error(
                "Failed to rebase vulnerability in integrates",
                extra=dict(extra={"exception": exception, **local_vars}),
            )


async def _vulnerability_historic_state(
    loaders: Dataloaders, vuln_id: str
) -> tuple[str, tuple[VulnerabilityState, ...]]:
    return (
        vuln_id,
        tuple(await loaders.vulnerability_historic_state.load(vuln_id)),
    )


async def rebase_root(
    loaders: Dataloaders, group_name: str, repo: Repo, git_root: GitRoot
) -> None:
    root_head_commit = repo.head.commit.hexsha
    vulnerabilities: tuple[
        Vulnerability, ...
    ] = await _get_vulnerabilities_to_rebase(loaders, group_name, git_root)
    vuln_states_dict: dict[str, tuple[VulnerabilityState, ...]] = dict(
        await collect(
            [
                _vulnerability_historic_state(loaders, vuln.id)
                for vuln in vulnerabilities
            ],
            workers=100,
        )
    )
    with ThreadPoolExecutor(max_workers=8) as executor:
        all_rebase: tuple[
            tuple[git_utils.RebaseResult | None, Vulnerability], ...
        ] = tuple(
            executor.map(
                lambda vuln: (
                    _rebase_vulnerability(
                        repo, vuln, vuln_states_dict[vuln.id]
                    ),
                    vuln,
                ),
                vulnerabilities,
            )
        )
    await collect(
        [
            _rebase_vulnerability_integrates(
                loaders=loaders,
                finding_id=vuln.finding_id,
                finding_vulns_data=tuple(
                    item
                    for item in vulnerabilities
                    if item.finding_id == vuln.finding_id
                ),
                vulnerability_commit=rebase_result.rev,
                vulnerability_id=vuln.id,
                vulnerability_where=rebase_result.path,
                vulnerability_specific=str(rebase_result.line),
                vulnerability_type=vuln.type,
            )
            for rebase_result, vuln in all_rebase
            if rebase_result
            and (
                rebase_result.path != vuln.state.where
                or str(rebase_result.line) != vuln.state.specific
            )
            and rebase_result.rev == root_head_commit
        ]
    )
    await collect(
        [
            close_vulnerability(
                loaders,
                vuln.id,
                rebase_result.rev,
                rebase_result.path,
                str(rebase_result.line),
            )
            for rebase_result, vuln in all_rebase
            if rebase_result
            and rebase_result.rev != root_head_commit
            and vuln.created_by == "machine@fluidattacks.com"
        ]
    )
    vulnerabilities_snippet = await get_vulnerabilities(
        loaders=loaders,
        vulnerability_ids=[vuln.id for vuln in vulnerabilities],
        clear_loader=True,
    )
    futures = []
    for vuln in vulnerabilities_snippet:
        if (not vuln.state.snippet or not vuln.state.snippet.content) and (
            snippet := generate_snippet(vuln.state, repo)
        ):
            futures.append(set_snippet(vuln, snippet))
    await collect(futures, workers=50)


async def rebase_root_simple_args(group_name: str, git_root_id: str) -> None:
    loaders = get_new_context()
    git_root = await loaders.root.load(RootRequest(group_name, git_root_id))
    if not git_root or not isinstance(git_root, GitRoot):
        return
    with tempfile.TemporaryDirectory(
        prefix="integrates_rebase_root_", ignore_cleanup_errors=True
    ) as tmpdir:
        os.chdir(tmpdir)
        repo_path = os.path.join(tmpdir, git_root.state.nickname)
        repo = await download_repo(
            git_root.group_name,
            git_root.state.nickname,
            tmpdir,
            git_root.state.gitignore,
        )
        if not repo:
            return None

        os.chdir(repo_path)
        await rebase_root(loaders, group_name, repo, git_root)


async def rebase(*, item: BatchProcessing) -> None:
    group_name: str = item.entity
    try:
        root_nicknames = json.loads(item.additional_info)["roots"]
    except json.JSONDecodeError:
        root_nicknames = item.additional_info.split(",")

    loaders = get_new_context()
    group_roots = [
        root
        for root in await loaders.group_roots.load(group_name)
        if root.state.status == RootStatus.ACTIVE and isinstance(root, GitRoot)
    ]
    # In the off case there are multiple roots with the same nickname
    if item.additional_info == "*":
        root_ids = [root.id for root in group_roots]
    else:
        root_ids = [
            roots_domain.get_root_id_by_nickname(
                nickname=nickname,
                group_roots=group_roots,
                only_git_roots=True,
            )
            for nickname in root_nicknames
        ]

    roots = [root for root in group_roots if root.id in root_ids]
    for git_root in roots:
        with tempfile.TemporaryDirectory(
            prefix=f"integrates_rebase_{group_name}_",
            ignore_cleanup_errors=True,
        ) as tmpdir:
            os.chdir(tmpdir)
            repo_path = os.path.join(tmpdir, git_root.state.nickname)
            repo = await download_repo(
                git_root.group_name,
                git_root.state.nickname,
                tmpdir,
                git_root.state.gitignore,
            )
            if not repo:
                return None
            os.chdir(repo_path)
            await rebase_root(loaders, group_name, repo, git_root)
            await delete_action(
                action_name=item.action_name,
                additional_info=item.additional_info,
                entity=item.entity,
                subject=item.subject,
                time=item.time,
            )


async def queue_rebase_async(group_name: str, git_root_id: str) -> None:
    with suppress(ClientError):
        await (await get_sqs_resource()).send_message(
            QueueUrl=(
                "https://sqs.us-east-1.amazonaws.com/205810638802/"
                "integrates_rebase"
            ),
            MessageBody=json.dumps(
                {
                    "id": f"{group_name}_{git_root_id}",
                    "task": "rebase",
                    "args": [
                        group_name,
                        git_root_id,
                    ],
                }
            ),
        )
