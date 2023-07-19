from .schema import (
    GROUP,
)
from custom_utils.vulnerabilities import (
    get_inverted_state_converted,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.vulnerabilities.constants import (
    RELEASED_FILTER_STATUSES,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    GroupVulnerabilitiesRequest,
    VulnerabilitiesConnection,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP.field("forcesVulnerabilities")
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    after: str | None = None,
    first: int | None = None,
    state: str | None = None,
    **_kwargs: None,
) -> VulnerabilitiesConnection:
    loaders: Dataloaders = info.context.loaders
    state_status = (
        None
        if state is None
        else VulnerabilityStateStatus[get_inverted_state_converted(state)]
    )
    connection = await loaders.group_vulnerabilities.load(
        GroupVulnerabilitiesRequest(
            is_accepted=None if state_status is None else False,
            group_name=parent.name,
            state_status=state_status,
            after=after,
            first=first,
            paginate=True,
        )
    )
    if state_status in RELEASED_FILTER_STATUSES:
        # Wait to process the indicators
        return VulnerabilitiesConnection(
            edges=tuple(
                edge
                for edge in connection.edges
                if edge.node.unreliable_indicators.unreliable_report_date
            ),
            page_info=connection.page_info,
        )
    return connection
