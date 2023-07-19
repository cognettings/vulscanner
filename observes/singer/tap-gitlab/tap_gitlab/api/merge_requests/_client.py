from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from enum import (
    Enum,
)
from fa_purity import (
    FrozenDict,
    FrozenList,
    JsonObj,
    JsonValue,
    Maybe,
    Result,
    ResultE,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json.factory import (
    from_unfolded_dict,
)
from tap_gitlab import (
    _utils,
)
from tap_gitlab.api.core.ids import (
    ProjectId,
)
from tap_gitlab.api.http_json_client import (
    HttpJsonClient,
    Page,
)


class State(Enum):
    # locked: transitional state while a merge is happening
    opened = "opened"
    closed = "closed"
    locked = "locked"
    merged = "merged"
    all = "all"

    @staticmethod
    def from_raw(raw: str) -> ResultE[State]:
        try:
            return Result.success(State(raw))
        except ValueError as err:
            return Result.failure(Exception(err))


class Scope(Enum):
    created_by_me = "created_by_me"
    assigned_to_me = "assigned_to_me"
    all = "all"

    @staticmethod
    def from_raw(raw: str) -> ResultE[Scope]:
        try:
            return Result.success(Scope(raw))
        except ValueError as err:
            return Result.failure(Exception(err))


class OrderBy(Enum):
    created_at = "created_at"
    title = "title"
    updated_at = "updated_at"


class Sort(Enum):
    ascendant = "asc"
    descendant = "desc"


@dataclass(frozen=True)
class MrFilter:
    updated_after: Maybe[datetime]
    updated_before: Maybe[datetime]
    scope: Maybe[Scope]
    state: Maybe[State]
    order_by: Maybe[OrderBy]
    sort: Maybe[Sort]

    def to_json(self) -> JsonObj:
        updated_after = self.updated_after.map(
            lambda u: {"updated_after": _utils.to_unfolded(u.isoformat())}
        ).map(lambda x: freeze(x))
        updated_before = self.updated_before.map(
            lambda u: {"updated_before": _utils.to_unfolded(u.isoformat())}
        ).map(lambda x: freeze(x))
        scope = self.scope.map(
            lambda s: {"scope": _utils.to_unfolded(s.value)}
        ).map(lambda x: freeze(x))
        state = self.state.map(
            lambda s: {"state": _utils.to_unfolded(s.value)}
        ).map(lambda x: freeze(x))
        order_by = self.order_by.map(
            lambda s: {"order_by": _utils.to_unfolded(s.value)}
        ).map(lambda x: freeze(x))
        sort = self.sort.map(
            lambda s: {"sort": _utils.to_unfolded(s.value)}
        ).map(lambda x: freeze(x))
        _all = (
            updated_after,
            updated_before,
            scope,
            state,
            order_by,
            sort,
        )
        return from_unfolded_dict(_utils.chain_maybe_dicts(_all))


@dataclass(frozen=True)
class MrsClient:
    _client: HttpJsonClient
    _project: ProjectId
    _filter: Maybe[MrFilter]

    def mrs_page(self, page: Page) -> Cmd[FrozenList[JsonObj]]:
        default_args: FrozenDict[str, JsonValue] = freeze(
            {
                "page": JsonValue(page.page_num),
                "per_page": JsonValue(page.per_page),
            }
        )
        args = self._filter.map(
            lambda f: _utils.merge_dicts((default_args, f.to_json()))
        ).value_or(default_args)
        return self._client.legacy_get_list(
            "/projects/" + self._project.str_val + "/merge_requests", args
        )
