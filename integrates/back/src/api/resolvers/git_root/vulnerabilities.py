from .schema import (
    GIT_ROOT,
)
from custom_utils.filter_vulnerabilities import (
    filter_non_deleted,
    filter_non_zero_risk,
    filter_released_vulns,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    Root,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GIT_ROOT.field("vulnerabilities")
async def resolve(
    parent: Root, info: GraphQLResolveInfo
) -> list[Vulnerability]:
    loaders: Dataloaders = info.context.loaders
    root_vulnerabilities = await loaders.root_vulnerabilities.load(parent.id)
    return filter_released_vulns(
        filter_non_zero_risk(filter_non_deleted(root_vulnerabilities))
    )
