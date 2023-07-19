from custom_utils.findings import (
    get_requirements_file,
    get_vulns_file,
)
from custom_utils.vulnerabilities import (
    is_machine_vuln,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from dynamodb.types import (
    Item,
)
from findings.domain.core import (
    add_reattack_justification,
    remove_finding,
)
from server_async.report_machine.finding import (
    create_finding,
    split_target_findings,
    update_finding_metadata,
)
from server_async.report_machine.vulnerability import (
    get_vulns_to_confirm,
    get_vulns_to_open_or_submit,
    get_vulns_with_reattack,
    persist_vulnerabilities,
    update_vulns_already_reported,
)


async def _report(
    *,
    loaders: Dataloaders,
    group: Group,
    git_root: GitRoot,
    target_finding: Finding,
    vulnerability_file: dict[str, list[dict[str, Item]]],
    auto_approve: bool = False,
) -> None:
    organization = await loaders.organization.load(group.organization_id)
    if not organization:
        return

    existing_machine_vulns: tuple[Vulnerability, ...] = tuple(
        vuln
        for vuln in await loaders.finding_vulnerabilities.load(
            target_finding.id
        )
        if is_machine_vuln(vuln) and vuln.root_id == git_root.id
    )
    existing_open_machine_vulns: tuple[Vulnerability, ...] = tuple(
        vuln
        for vuln in existing_machine_vulns
        if vuln.state.status == VulnerabilityStateStatus.VULNERABLE
    )
    existing_unreleased_machine_vulns: tuple[Vulnerability, ...] = tuple(
        vuln
        for vuln in existing_machine_vulns
        if vuln.state.status
        in {
            VulnerabilityStateStatus.SUBMITTED,
            VulnerabilityStateStatus.REJECTED,
        }
    )
    vulns_to_confirm = get_vulns_to_confirm(
        vulnerability_file,
        existing_open_machine_vulns,
    )

    reattack_future = add_reattack_justification(
        loaders=loaders,
        finding_id=target_finding.id,
        open_vulnerabilities=get_vulns_with_reattack(
            vulns_to_confirm, existing_open_machine_vulns, "open"
        ),
        closed_vulnerabilities=[],
        commit_hash=(
            vulnerability_file["lines"][0]["commit_hash"]  # type: ignore
            if vulnerability_file.get("lines", [])
            else None
        ),
        comment_type=CommentType.VERIFICATION,
    )

    await update_vulns_already_reported(
        vulnerability_file,
        existing_open_machine_vulns + existing_unreleased_machine_vulns,
    )

    vulns_to_open_or_submit = get_vulns_to_open_or_submit(
        vulnerability_file,
        existing_open_machine_vulns + existing_unreleased_machine_vulns,
    )
    if (
        vulns_to_open_or_submit["lines"] or vulns_to_open_or_submit["inputs"]
    ) and await persist_vulnerabilities(
        loaders=loaders,
        group_name=group.name,
        git_root=git_root,
        finding=target_finding,
        stream={
            "inputs": [
                *vulns_to_open_or_submit["inputs"],
            ],
            "lines": [
                *vulns_to_open_or_submit["lines"],
            ],
        },
        organization_name=(organization).name,
        auto_approve=auto_approve,
    ):
        await reattack_future


async def process_vulnerabilities(
    group_name: str,
    git_root_nickname: str,
    finding_code: str,
    auto_approve: bool,
    vulnerability_file: dict[str, list[dict[str, Item]]],
) -> None:
    loaders: Dataloaders = get_new_context()
    if (
        not vulnerability_file.get("lines")
        and not vulnerability_file.get("inputs")
    ) or (
        vulnerability_file["lines"]
        and (
            await loaders.vulnerability_by_hash.load(
                str(vulnerability_file["lines"][0]["hash"])
            )
        )
        is not None
    ):
        return

    criteria_vulns = await get_vulns_file()
    criteria_reqs = await get_requirements_file()
    group: Group | None = await loaders.group.load(group_name)
    if not group:
        return

    git_root = next(
        (
            root
            for root in (await loaders.group_roots.load(group_name))
            if isinstance(root, GitRoot)
            and root.state.status == RootStatus.ACTIVE
            and root.state.nickname == git_root_nickname
        ),
        None,
    )
    if not git_root:
        return

    group_findings: list[Finding] = await loaders.group_findings.load(
        group_name
    )
    same_type_of_findings = tuple(
        finding
        for finding in group_findings
        if finding.title.startswith(f"{finding_code}.")
    )
    target_finding, _ = split_target_findings(
        same_type_of_findings,
    )

    new_finding = False
    if not target_finding:
        target_finding = await create_finding(
            loaders,
            group.name,
            finding_code,
            group.language.value,
            criteria_vulns[finding_code],
        )
        new_finding = True
    else:
        await update_finding_metadata(
            (group.name, finding_code, group.language.value),
            target_finding,
            criteria_vulns[finding_code],
            criteria_reqs,
        )
        loaders.group_findings.clear(group.name)
        loaders.finding.clear(target_finding.id)

    await _report(
        loaders=loaders,
        group=group,
        git_root=git_root,
        target_finding=target_finding,
        vulnerability_file=vulnerability_file,
        auto_approve=auto_approve,
    )

    loaders.finding_vulnerabilities.clear(target_finding.id)
    if new_finding and not await loaders.finding_vulnerabilities.load(
        target_finding.id
    ):
        await remove_finding(
            loaders,
            email="machine@fluidattacks.com",
            finding_id=target_finding.id,
            justification=StateRemovalJustification.REPORTING_ERROR,
            source=Source.MACHINE,
        )
