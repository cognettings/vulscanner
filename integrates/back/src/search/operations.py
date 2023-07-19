from dynamodb.types import (
    Item,
    PageInfo,
)
import logging
from opensearchpy import (
    NotFoundError,
)
from search.client import (
    get_client,
)
from search.enums import (
    Sort,
)
from search.types import (
    BoolQuery,
    ScriptQuery,
    SearchResponse,
)
import simplejson as json
from typing import (
    Any,
)

LOGGER = logging.getLogger(__name__)


def _get_end_cursor(*, hits: list[Item], sort_by: list[Item] | None) -> Any:
    if hits:
        if sort_by and "sort" in hits[-1] and hits[-1]["sort"]:
            return json.dumps([str(attr) for attr in hits[-1]["sort"]])
        return hits[-1]["_id"]

    if sort_by:
        return json.dumps([])
    return ""


def _get_terms_queries(exact_filters: Item | None) -> list[Item]:
    return (
        [
            {"terms": {key: value}}
            for key, value in exact_filters.items()
            if isinstance(value, list)
        ]
        if exact_filters
        else []
    )


def _get_term_queries(exact_filters: Item | None) -> list[Item]:
    return (
        [
            {"term": {key: value}}
            for key, value in exact_filters.items()
            if not isinstance(value, list)
        ]
        if exact_filters
        else []
    )


def _get_full_text_queries(query: str | None) -> list[Item]:
    return [{"multi_match": {"query": query}}] if query else []


def _get_full_match_prefix_filters(
    must_match_prefix_filters: list[Item] | None,
) -> list[Item]:
    return (
        [
            {"match_phrase_prefix": {key: value}}
            for attrs in must_match_prefix_filters
            for key, value in attrs.items()
        ]
        if must_match_prefix_filters
        else []
    )


def _get_query_range(range_filters: list[Item] | None) -> list[Item]:
    return (
        [{"range": range} for range in range_filters] if range_filters else []
    )


def _get_full_or_filters(should_filters: list[Item] | None) -> list[Item]:
    return (
        [
            {"match": {key: value}}
            for attrs in should_filters
            for key, value in attrs.items()
        ]
        if should_filters
        else []
    )


def _get_full_should_must_filters(
    should_filters: list[Item] | None,
) -> list[Item]:
    return [{"bool": {"must": should_filters}}] if should_filters else []


def _get_full_and_filters(must_filters: list[Item] | None) -> list[Item]:
    return (
        [
            {"match": {key: {"query": value, "operator": "and"}}}
            for attrs in must_filters
            for key, value in attrs.items()
        ]
        if must_filters
        else []
    )


def _get_not_exists_filters(fields: list[str] | None) -> list[Item]:
    return [
        {"bool": {"must_not": [{"exists": {"field": field}}]}}
        for field in fields or []
    ]


def _get_bool_queries(bool_filters: list[BoolQuery] | None) -> list[Item]:
    def _get_bool_query(bool_filter: BoolQuery) -> Item:
        return {
            "must": [
                *_get_terms_queries(bool_filter.get("and_exact_filters")),
                *_get_not_exists_filters(
                    bool_filter.get("and_not_exists_filters")
                ),
            ],
            "should": [
                *_get_bool_queries(bool_filter.get("or_bool_filters")),
                *_get_query_range(bool_filter.get("or_range_filters")),
            ],
        }

    return (
        [
            {"bool": _get_bool_query(bool_filter)}
            for bool_filter in bool_filters
        ]
        if bool_filters
        else []
    )


def _get_wildcards_queries(queries: list[Item] | None) -> list[Item]:
    return (
        [
            {"wildcard": {key: {"value": value}}}
            for attrs in queries
            for key, value in attrs.items()
        ]
        if queries
        else []
    )


def _get_must_script_queries(queries: list[ScriptQuery] | None) -> list[Item]:
    return (
        [
            {
                "script": {
                    "script": {
                        "source": attrs.source,
                        "lang": "painless",
                        "params": attrs.params,
                    }
                }
            }
            for attrs in queries
        ]
        if queries
        else []
    )


async def search(  # pylint: disable=too-many-locals
    *,  # NOSONAR
    bool_filters: list[BoolQuery] | None = None,
    exact_filters: Item | None = None,
    index: str,
    limit: int,
    after: str | list[str] | None = None,
    query: str | None = None,
    collapse: str | None = None,
    should_filters: list[Item] | None = None,
    should_and_filters: list[Item] | None = None,
    should_match_prefix_filters: list[Item] | None = None,
    minimum_should_match: int = 1,
    must_filters: list[Item] | None = None,
    must_match_prefix_filters: list[Item] | None = None,
    range_filters: list[Item] | None = None,
    must_not_filters: list[Item] | None = None,
    paginate: bool = True,
    script_filters: list[ScriptQuery] | None = None,
    sort_by: list[Item] | None = None,
    wildcard_queries: list[Item] | None = None,
) -> SearchResponse:
    """
    Searches for items matching both the user input (full-text)
    and the provided filters (exact matches)

    https://opensearch.org/docs/1.2/opensearch/query-dsl/index/
    https://opensearch-project.github.io/opensearch-py/api-ref/client.html#opensearchpy.OpenSearch.search
    """
    client = await get_client()
    full_and_filters = _get_full_and_filters(must_filters)
    full_must_not_filters = _get_full_and_filters(must_not_filters)
    full_or_filters = _get_full_or_filters(should_filters)
    full_or_and_filters = _get_full_should_must_filters(should_and_filters)
    query_range = _get_query_range(range_filters)
    full_match_prefix_filters = _get_full_match_prefix_filters(
        must_match_prefix_filters
    )
    full_should_match_prefix_filters = _get_full_match_prefix_filters(
        should_match_prefix_filters
    )
    full_text_queries = _get_full_text_queries(query)
    term_queries = _get_term_queries(exact_filters)
    terms_queries = _get_terms_queries(exact_filters)
    wildcards_queries = _get_wildcards_queries(wildcard_queries)
    bool_queries = _get_bool_queries(bool_filters)
    script_queries = _get_must_script_queries(script_filters)
    body: dict = {
        "query": {
            "bool": {
                "must": [
                    *full_and_filters,
                    *full_text_queries,
                    *query_range,
                    *term_queries,
                    *terms_queries,
                    *full_match_prefix_filters,
                    *bool_queries,
                    *wildcards_queries,
                    *script_queries,
                ],
                "should": [
                    *full_or_filters,
                    *full_or_and_filters,
                    *full_should_match_prefix_filters,
                ],
                "minimum_should_match": minimum_should_match
                if full_or_filters
                or full_should_match_prefix_filters
                or full_or_and_filters
                else 0,
                "must_not": [*full_must_not_filters],
            }
        },
        "sort": sort_by
        if sort_by
        else [{"_id": {"order": Sort.DESCENDING.value}}],
    }

    if after:
        body["search_after"] = [after] if isinstance(after, str) else after

    if collapse:
        body["collapse"] = {"field": collapse}

    try:
        response = await client.search(
            body=body,
            index=index,
            size=limit,
        )
        hits: list[Item] = response["hits"]["hits"]
        total: int = response["hits"]["total"]["value"]
        end_cursor = _get_end_cursor(hits=hits, sort_by=sort_by)
        has_next_page = len(hits) == limit
        if not paginate:
            while has_next_page:
                body["search_after"] = [end_cursor]
                response = await client.search(
                    body=body,
                    index=index,
                    size=limit,
                )
                hits += response["hits"]["hits"]
                end_cursor = _get_end_cursor(hits=hits, sort_by=sort_by)
                has_next_page = len(response["hits"]["hits"]) == limit
            total = len(hits)

    except NotFoundError as ex:
        LOGGER.warning(ex)
        hits = []
        total = 0
        end_cursor = ""
        has_next_page = False

    return SearchResponse(
        items=tuple(hit["_source"] for hit in hits),
        page_info=PageInfo(
            end_cursor=end_cursor,
            has_next_page=has_next_page,
        ),
        total=total,
    )
