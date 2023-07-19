from . import (
    _decode,
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
    Cmd,
    FrozenDict,
    FrozenList,
    JsonObj,
    JsonValue,
    Maybe,
    PureIter,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json.factory import (
    from_unfolded_dict,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_purity.result.transform import (
    all_ok,
)
from tap_gitlab import (
    _utils,
)
from tap_gitlab.api.core.ids import (
    PipelineId,
    PipelineRelativeId,
    ProjectId,
)
from tap_gitlab.api.core.pipeline import (
    PipelineStatus,
)
from tap_gitlab.api.http_json_client import (
    HttpJsonClient,
    Page,
)
from typing import (
    Tuple,
)


class OrderBy(Enum):
    id = "id"
    status = "status"
    ref = "ref"
    updated_at = "updated_at"
    user_id = "user_id"


class Sort(Enum):
    asc = "asc"
    desc = "desc"


@dataclass(frozen=True)
class PipelineFilter:
    status: Maybe[PipelineStatus]
    updated_after: Maybe[datetime]
    updated_before: Maybe[datetime]
    order_by: Maybe[OrderBy]
    sort: Maybe[Sort]

    def to_json(self) -> JsonObj:
        after = self.updated_after.map(
            lambda d: {"updated_after": _utils.to_unfolded(d.isoformat())}
        ).map(lambda x: freeze(x))
        before = self.updated_before.map(
            lambda d: {"updated_before": _utils.to_unfolded(d.isoformat())}
        ).map(lambda x: freeze(x))
        status = self.status.map(
            lambda s: {"status": _utils.to_unfolded(s.value)}
        ).map(lambda x: freeze(x))
        order_by = self.order_by.map(
            lambda s: {"order_by": _utils.to_unfolded(s.value)}
        ).map(lambda x: freeze(x))
        sort = self.sort.map(
            lambda s: {"sort": _utils.to_unfolded(s.value)}
        ).map(lambda x: freeze(x))
        return from_unfolded_dict(
            _utils.chain_maybe_dicts((after, before, status, order_by, sort))
        )


@dataclass(frozen=True)
class PipelineClient:
    _client: HttpJsonClient
    _project: ProjectId
    _filter: Maybe[PipelineFilter]

    def _pipelines_page(self, page: Page) -> Cmd[PureIter[JsonObj]]:
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
            "/projects/" + self._project.str_val + "/pipelines", args
        ).map(lambda x: from_flist(x))

    def pipelines_ids_page(
        self,
        page: Page,
    ) -> Cmd[FrozenList[Tuple[PipelineId, PipelineRelativeId]]]:
        return self._pipelines_page(page).map(
            lambda i: all_ok(
                i.map(_decode.decode_pipeline_ids).to_list()
            ).unwrap()
        )

    def get_updated_at(self, pipeline: PipelineId) -> Cmd[datetime]:
        return self._client.legacy_get_item(
            "/projects/"
            + self._project.str_val
            + "/pipelines/"
            + _utils.int_to_str(pipeline.global_id),
            freeze({}),
        ).map(lambda j: _decode.decode_updated_at(j).unwrap())
