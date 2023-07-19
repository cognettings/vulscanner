from .schema import (
    GROUP,
)
from custom_utils.forces import (
    format_forces_to_resolve,
)
from db_model.forces.types import (
    ExecutionEdge,
    ExecutionsConnection,
)
from db_model.forces.utils import (
    format_forces_execution,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
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


@GROUP.field("executionsConnections")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **kwargs: Any,
) -> ExecutionsConnection:
    group_name: str = parent.name
    executions_filters: dict[str, Any] = executions_filter(**kwargs)

    after = kwargs.get("after")
    first = kwargs.get("first", 10)
    query = kwargs.get("search")

    results = await search(
        after=after,
        limit=first,
        query=query,
        must_filters=executions_filters["must_filters"],
        must_match_prefix_filters=executions_filters[
            "must_match_prefix_filters"
        ],
        range_filters=executions_filters["must_range_filters"],
        exact_filters={"group_name": group_name},
        index="forces_executions",
    )

    forces_executions = tuple(
        format_forces_execution(item) for item in results.items
    )
    executions_formatted = [
        format_forces_to_resolve(execution) for execution in forces_executions
    ]
    return ExecutionsConnection(
        edges=tuple(
            ExecutionEdge(
                cursor=results.page_info.end_cursor,
                node=execution,
            )
            for execution in executions_formatted
        ),
        page_info=results.page_info,
        total=results.total,
    )


def executions_filter(**kwargs: Any) -> dict[str, Any]:
    exec_must_filters: list[dict[str, Any]] = must_filter(**kwargs)
    exec_must_match_prefix_filters: list[
        dict[str, Any]
    ] = must_match_prefix_filter(**kwargs)
    exec_must_range_filters: list[dict[str, Any]] = must_range_filter(**kwargs)

    filters: dict[str, Any] = {
        "must_filters": exec_must_filters,
        "must_match_prefix_filters": exec_must_match_prefix_filters,
        "must_range_filters": exec_must_range_filters,
    }

    return filters


def must_filter(**kwargs: Any) -> list[dict[str, Any]]:
    must_filters = []

    if execution_type := kwargs.get("type"):
        must_filters.append({"kind": str(execution_type).upper()})

    if strictness := kwargs.get("strictness"):
        must_filters.append({"strictness": str(strictness).upper()})

    return must_filters


def must_match_prefix_filter(**kwargs: Any) -> list[dict[str, Any]]:
    must_match_filters = []

    if repo := kwargs.get("git_repo"):
        must_match_filters.append({"repo": str(repo)})

    return must_match_filters


def must_range_filter(**kwargs: Any) -> list[dict[str, Any]]:
    must_range_filters: list[dict[str, Any]] = []

    if from_date := kwargs.get("from_date"):
        must_range_filters.append(
            {"execution_date": {"gte": str(from_date.date())}}
        )

    if to_date := kwargs.get("to_date"):
        must_range_filters.append(
            {"execution_date": {"lte": str(to_date.date())}}
        )

    if status := kwargs.get("status"):
        must_range_filters.append(
            {
                "vulnerabilities.num_of_open_vulnerabilities": {"gt": 0}
                if str(status).lower() == "vulnerable"
                else {"lte": 0}
            }
        )

    return must_range_filters
