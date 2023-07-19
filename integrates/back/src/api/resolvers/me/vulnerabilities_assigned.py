from .schema import (
    ME,
)
from custom_utils.filter_vulnerabilities import (
    filter_non_zero_risk,
    filter_open_vulns,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from db_model.vulnerabilities.utils import (
    format_vulnerability,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from search.operations import (
    search,
)
from typing import (
    Any,
)


@ME.field("vulnerabilitiesAssigned")
async def resolve(
    parent: dict[str, Any], _info: GraphQLResolveInfo
) -> list[Vulnerability]:
    email: str = str(parent["user_email"])

    results = await search(
        must_filters=[{"treatment.assigned": email}],
        index="vulnerabilities",
        limit=1000,
    )

    vulnerabilities = filter_non_zero_risk(
        [format_vulnerability(result) for result in results.items]
    )

    return filter_non_zero_risk(filter_open_vulns(vulnerabilities))
