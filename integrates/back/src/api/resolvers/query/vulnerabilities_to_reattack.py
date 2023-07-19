from .schema import (
    QUERY,
)
from aioextensions import (
    collect,
)
from dataloaders import (
    Dataloaders,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from findings.domain import (
    get_vulnerabilities_to_reattack,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from itertools import (
    chain,
)
from organizations import (
    domain as orgs_domain,
)


@QUERY.field("vulnerabilitiesToReattack")
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> list[Vulnerability]:
    loaders: Dataloaders = info.context.loaders
    group_name = kwargs.get("group", "all")
    if group_name == "all":
        group_names = list(
            await orgs_domain.get_all_active_group_names(loaders)
        )
    else:
        group_names = [group_name]

    findings = await loaders.group_findings.load_many_chained(group_names)
    finding_ids = [finding.id for finding in findings]
    vulns_to_reattack = await collect(
        get_vulnerabilities_to_reattack(loaders, finding_id)
        for finding_id in finding_ids
    )

    return list(chain.from_iterable(vulns_to_reattack))
