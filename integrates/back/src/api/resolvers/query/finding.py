from .schema import (
    QUERY,
)
from custom_utils.findings import (
    is_finding_released,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    rename_kwargs,
    require_asm,
    require_login,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@enforce_group_level_auth_async
async def _get_draft(
    loaders: Dataloaders, _info: GraphQLResolveInfo, **kwargs: str
) -> Finding:
    finding_id: str = kwargs["finding_id"]
    return await findings_domain.get_finding(loaders, finding_id)


@QUERY.field("finding")
@rename_kwargs({"identifier": "finding_id"})
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_asm
)
@require_login
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Finding:
    finding_id: str = kwargs["finding_id"]
    loaders: Dataloaders = info.context.loaders
    finding = await findings_domain.get_finding(loaders, finding_id)
    if not is_finding_released(finding):
        return await _get_draft(loaders, info, **kwargs)

    return finding
