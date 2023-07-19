from .schema import (
    GROUP,
)
from db_model.groups.types import (
    Group,
)
from db_model.toe_lines.types import (
    ToeLinesConnection,
    ToeLinesEdge,
)
from db_model.toe_lines.utils import (
    format_toe_lines,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    rename_kwargs,
    validate_connection,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from search.enums import (
    Sort,
)
from search.operations import (
    search,
)
from search.types import (
    ScriptQuery,
    SearchResponse,
)
from typing import (
    Any,
)

DEFAULT_PAGE_SIZE = 10
INDEX_NAME = "toe_lines"


@GROUP.field("toeLinesConnection")
@rename_kwargs(
    {
        "from_modified_date": "from_last_commit_date",
        "to_modified_date": "to_last_commit_date",
    }
)
@concurrent_decorators(
    enforce_group_level_auth_async,
    validate_connection,
)
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **kwargs: Any,
) -> ToeLinesConnection:
    search_params = create_search_params(parent, kwargs)
    results: SearchResponse = await search(**search_params)
    response = create_toe_lines_connection(results)

    return response


def create_search_params(parent: Group, kwargs: Any) -> dict[str, Any]:
    toe_lines_filters: dict[str, Any] = toe_lines_filter(**kwargs)
    sort_values = kwargs.get("sort", {})
    sort_field = sort_values.get("field", "sorts_priority_factor").lower()
    sort_order = sort_values.get("order", Sort.DESCENDING.value).lower()

    return {
        "after": kwargs.get("after"),
        "exact_filters": {"group_name": parent.name},
        "must_filters": toe_lines_filters["must_filters"],
        "must_match_prefix_filters": toe_lines_filters["must_match_filters"],
        "range_filters": toe_lines_filters["must_range_filters"],
        "index": INDEX_NAME,
        "limit": kwargs.get("first", DEFAULT_PAGE_SIZE),
        "script_filters": toe_lines_filters["script_filters"],
        "sort_by": [
            {f"state.{sort_field}": {"order": sort_order}},
            {"_id": {"order": sort_order}},
        ],
    }


def create_toe_lines_connection(results: SearchResponse) -> ToeLinesConnection:
    toe_lines = tuple(format_toe_lines(result) for result in results.items)

    edges = tuple(
        ToeLinesEdge(
            cursor=results.page_info.end_cursor,
            node=toe_line,
        )
        for toe_line in toe_lines
    )

    return ToeLinesConnection(
        edges=edges,
        page_info=results.page_info,
        total=results.total,
    )


def toe_lines_filter(**kwargs: Any) -> dict[str, Any]:
    vulns_must_filters: list[dict[str, Any]] = must_filter(**kwargs)
    vulns_must_match_prefix_filters: list[
        dict[str, Any]
    ] = must_match_prefix_filter(**kwargs)
    exec_must_range_filters: list[dict[str, Any]] = must_range_filter(**kwargs)
    script_filters: list[ScriptQuery] = _get_script_filters(**kwargs)

    filters: dict[str, Any] = {
        "must_filters": vulns_must_filters,
        "must_match_filters": vulns_must_match_prefix_filters,
        "must_range_filters": exec_must_range_filters,
        "script_filters": script_filters,
    }

    return filters


def get_items_to_filter(
    filters: dict[str, Any],
    kwargs: Any,
    parameter: str | None = None,
    range_condition: str | None = None,
) -> list[dict[str, Any]]:
    items_to_filter = [
        {
            (field if path == "common" else f"{path}.{field}"): (
                {range_condition: filter_value}
                if range_condition
                else filter_value
            ),
        }
        for path, fields in filters.items()
        for field in fields
        if (
            filter_value := kwargs.get(
                f"{parameter}_{field}" if parameter else field
            )
        )
        not in [None, ""]
    ]
    return items_to_filter


def must_filter(**kwargs: Any) -> list[dict[str, Any]]:
    filters: dict[str, Any] = {
        "common": ["root_id"],
        "state": ["be_present", "has_vulnerabilities"],
    }
    must_filters = get_items_to_filter(filters, kwargs)

    return must_filters


def must_match_prefix_filter(**kwargs: Any) -> list[dict[str, Any]]:
    filters: dict[str, Any] = {
        "common": ["filename"],
        "state": ["attacked_by", "comments", "last_commit", "last_author"],
    }

    must_match_filters = get_items_to_filter(filters, kwargs)

    return must_match_filters


def must_range_filter(**kwargs: Any) -> list[dict[str, Any]]:
    from_to_filters: dict[str, Any] = {
        "state": [
            "seen_at",
            "first_attack_at",
            "attacked_at",
            "be_present_until",
            "last_commit_date",
        ],
    }

    min_max_filters: dict[str, Any] = {
        "state": [
            "loc",
            "attacked_lines",
            "sorts_priority_factor",
            "sorts_risk_level",
        ]
    }

    must_range_filters: list[dict[str, Any]] = [
        *get_items_to_filter(from_to_filters, kwargs, "from", "gte"),
        *get_items_to_filter(min_max_filters, kwargs, "min", "gte"),
        *get_items_to_filter(from_to_filters, kwargs, "to", "lte"),
        *get_items_to_filter(min_max_filters, kwargs, "max", "lte"),
    ]

    return must_range_filters


def _get_script_filters(**kwargs: Any) -> list[ScriptQuery]:
    script_filters: list[ScriptQuery] = []
    coverage = """
        doc['state.loc'].value == 0
            ? 1
            : doc['state.attacked_lines'].value / doc['state.loc'].value
    """
    coverage_formatted = f"Math.round(({coverage}) * 100)"

    if min_coverage := kwargs.get("min_coverage"):
        source = f"{coverage_formatted} >= params.min_coverage"
        params = {"min_coverage": min_coverage}
        script_filters.append(ScriptQuery(source=source, params=params))

    if max_coverage := kwargs.get("max_coverage"):
        source = f"{coverage_formatted} <= params.max_coverage"
        params = {"max_coverage": max_coverage}
        script_filters.append(ScriptQuery(source=source, params=params))

    return script_filters
