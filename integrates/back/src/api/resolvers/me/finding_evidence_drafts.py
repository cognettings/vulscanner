from .schema import (
    ME,
)
import authz
from custom_utils.validations_deco import (
    validate_all_fields_length_deco,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    FindingEdge,
    FindingEvidences,
    FindingsConnection,
)
from db_model.findings.utils import (
    format_finding,
)
from dynamodb.types import (
    PageInfo,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_access.domain import (
    get_stakeholder_groups_names,
)
from search.operations import (
    search,
)
from typing import (
    Any,
)


@ME.field("findingEvidenceDrafts")
@validate_all_fields_length_deco(max_length=300)
async def resolve(
    parent: dict[str, Any], info: GraphQLResolveInfo, **kwargs: Any
) -> FindingsConnection:
    email = str(parent["user_email"])
    loaders: Dataloaders = info.context.loaders

    must_not_filters = [
        {"state.status": FindingStateStatus.DELETED},
        {"state.status": FindingStateStatus.MASKED},
    ]
    should_filters = [
        {f"evidences.{evidence}.is_draft": True}
        for evidence in FindingEvidences._fields
    ]
    group_names = await get_stakeholder_groups_names(loaders, email, True)
    enforcer = await authz.get_group_level_enforcer(loaders, email)
    groups_to_search = [
        group_name
        for group_name in group_names
        if enforcer(group_name, "api_mutations_approve_evidence_mutate")
    ]

    if not groups_to_search:
        return FindingsConnection(
            edges=tuple(),
            page_info=PageInfo(has_next_page=False, end_cursor=""),
            total=0,
        )

    results = await search(
        after=kwargs.get("after"),
        exact_filters={"group_name": groups_to_search},
        must_not_filters=must_not_filters,
        should_filters=should_filters,
        index="findings",
        limit=kwargs.get("first", 100),
    )

    return FindingsConnection(
        edges=tuple(
            FindingEdge(
                cursor=results.page_info.end_cursor,
                node=format_finding(item),
            )
            for item in results.items
        ),
        page_info=results.page_info,
        total=results.total,
    )
