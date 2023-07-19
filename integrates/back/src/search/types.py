from dynamodb.types import (
    PageInfo,
)
from typing import (
    Any,
    NamedTuple,
    TypedDict,
)

Item = dict[str, Any]


class SearchResponse(NamedTuple):
    items: tuple[Item, ...]
    page_info: PageInfo
    total: int


class BoolQuery(TypedDict, total=False):
    and_exact_filters: Item | None
    and_not_exists_filters: list[str] | None
    or_bool_filters: list["BoolQuery"] | None
    or_range_filters: list[Item] | None


class ScriptQuery(NamedTuple):
    source: str
    params: Item
