from .schema import (
    GROUP,
)
from authz import (
    FLUID_IDENTIFIER,
)
from custom_utils import (
    utils,
)
from custom_utils.findings import (
    get_group_released_findings,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityZeroRiskStatus,
)
from decorators import (
    require_asm,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import logging
import logging.config
from search.operations import (
    search,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)
from vulnerabilities.domain.core import (
    get_vulns_filters_by_root_nickname,
)

LOGGER = logging.getLogger(__name__)


@GROUP.field("findings")
@require_asm
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> list[Finding]:
    user_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    user_email: str = user_info["user_email"]
    has_internal_role: bool = user_email.endswith(FLUID_IDENTIFIER)
    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name
    filters: dict[str, Any] | None = kwargs.get("filters")
    findings = await get_findings(
        filters=filters,
        group_name=group_name,
        loaders=loaders,
        has_internal_role=has_internal_role,
    )

    if not has_internal_role:
        findings = get_group_released_findings(findings=findings)
    if filters:
        return utils.filter_findings(findings, filters)

    return findings


async def get_findings(
    *,
    filters: dict[str, Any] | None,
    group_name: str,
    loaders: Dataloaders,
    has_internal_role: bool,
) -> list[Finding]:
    if (
        filters
        and (root := filters.pop("root", None))
        and isinstance(root, str)
    ):
        return await _filter_findings_by_vulns(
            group_name=group_name,
            loaders=loaders,
            root=root,
            has_internal_role=has_internal_role,
        )

    return await loaders.group_findings.load(group_name)


async def _filter_findings_by_vulns(
    *,
    group_name: str,
    loaders: Dataloaders,
    root: str,
    has_internal_role: bool,
) -> list[Finding]:
    has_next_page: bool = True
    after: str | list[str] | None = None
    findings_id: set[str] = set()
    should_and_filters = await get_vulns_filters_by_root_nickname(
        loaders, group_name, root
    )
    released_vulns = (
        [{"sk_6.keyword": "*RELEASED#true*"}]
        if not has_internal_role
        else None
    )

    while has_next_page:
        results = await search(
            after=after,
            exact_filters={"group_name": group_name},
            index="vulnerabilities",
            limit=100,
            must_not_filters=must_not_filter(has_internal_role),
            should_and_filters=should_and_filters,
            should_match_prefix_filters=[{"state.where": root}],
            wildcard_queries=released_vulns,
        )
        has_next_page = results.page_info.has_next_page
        after = results.page_info.end_cursor
        findings_id.update(item["sk"].split("#")[1] for item in results.items)

    findings = await loaders.finding.load_many(findings_id)
    filtered_findings: list[Finding] = list(filter(None, findings))
    return filtered_findings


def must_not_filter(has_internal_role: bool) -> list[dict[str, Any]]:
    must_not_filters: list[dict[str, Any]] = [
        {"state.status": VulnerabilityStateStatus.DELETED.value},
        {"state.status": VulnerabilityStateStatus.MASKED.value},
        {"zero_risk.status": VulnerabilityZeroRiskStatus.CONFIRMED.value},
        {"zero_risk.status": VulnerabilityZeroRiskStatus.REQUESTED.value},
    ]

    if not has_internal_role:
        must_not_filters.append(
            {"state.status": VulnerabilityStateStatus.REJECTED.value}
        )
        must_not_filters.append(
            {"state.status": VulnerabilityStateStatus.SUBMITTED.value}
        )

    return must_not_filters
