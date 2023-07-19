from . import (
    _decode,
)
from ._decode import (
    JobObj,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    FrozenList,
    JsonObj,
    JsonValue,
    Maybe,
    PureIter,
    UnfoldedJVal,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json.factory import (
    from_unfolded_dict,
)
from fa_purity.json.transform import (
    dumps,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
import logging
from tap_gitlab import (
    _utils,
)
from tap_gitlab.api.core import (
    JobStatus,
)
from tap_gitlab.api.core.ids import (
    JobId,
    PipelineId,
    ProjectId,
)
from tap_gitlab.api.http_json_client import (
    HttpJsonClient,
    Page,
)
from typing import (
    Dict,
    FrozenSet,
    TypeVar,
)

_K = TypeVar("_K")
_T = TypeVar("_T")
LOG = logging.getLogger(__name__)


def _to_unfolded(item: UnfoldedJVal) -> UnfoldedJVal:
    return item


def _merge(items: FrozenList[FrozenDict[_K, _T]]) -> FrozenDict[_K, _T]:
    result: Dict[_K, _T] = {}
    for i in items:
        result = result | dict(i)
    return freeze(result)


def _chain(
    items: FrozenList[Maybe[FrozenDict[str, _T]]]
) -> FrozenDict[str, _T]:
    empty: Dict[str, _T] = {}
    return _merge(tuple(i.value_or(freeze(empty)) for i in items))


@dataclass(frozen=True)
class JobsFilter:
    scope: Maybe[FrozenSet[JobStatus]]
    include_retried: bool

    def to_json(self) -> JsonObj:
        scope = self.scope.map(
            lambda scopes: {
                "scope[]": _to_unfolded(
                    tuple(JsonValue(s.value) for s in scopes)
                )
            }
        ).map(lambda x: freeze(x))
        include_retried = freeze(
            {"include_retried": _to_unfolded(self.include_retried)}
        )
        return from_unfolded_dict(_merge((_chain((scope,)), include_retried)))


@dataclass(frozen=True)
class JobsClient:
    _client: HttpJsonClient
    _project: ProjectId
    _filter: Maybe[JobsFilter]

    def _raw_jobs_page(self, page: Page) -> Cmd[FrozenList[JsonObj]]:
        default_args: FrozenDict[str, JsonValue] = freeze(
            {
                "page": JsonValue(page.page_num),
                "per_page": JsonValue(page.per_page),
            }
        )
        args = self._filter.map(
            lambda f: _merge((default_args, f.to_json()))
        ).value_or(default_args)
        return self._client.legacy_get_list(
            "/projects/" + self._project.str_val + "/jobs", args
        )

    def jobs_page(self, page: Page) -> Cmd[FrozenList[JobObj]]:
        return self._raw_jobs_page(page).map(
            lambda js: from_flist(js)
            .map(
                lambda j: _decode.decode_job_obj(j)
                .alt(lambda e: _utils.raise_and_log(LOG, e, dumps(j)))  # type: ignore[misc]
                .unwrap()
            )
            .to_list()
        )

    def jobs_ids_page(self, page: Page) -> Cmd[FrozenList[JobId]]:
        return self._raw_jobs_page(page).map(
            lambda js: from_flist(js)
            .map(lambda j: _decode.decode_job_id(j).unwrap())
            .to_list()
        )

    def pipeline_jobs_page(
        self, pipeline: PipelineId, page: Page
    ) -> Cmd[FrozenList[JobObj]]:
        default_args: FrozenDict[str, JsonValue] = freeze(
            {
                "page": JsonValue(page.page_num),
                "per_page": JsonValue(page.per_page),
            }
        )
        args = self._filter.map(
            lambda f: _merge((default_args, f.to_json()))
        ).value_or(default_args)
        return self._client.legacy_get_list(
            "/projects/"
            + self._project.str_val
            + "/pipelines/"
            + _utils.int_to_str(pipeline.global_id)
            + "/jobs",
            args,
        ).map(
            lambda x: from_flist(x)
            .map(lambda j: _decode.decode_job_obj(j).unwrap())
            .to_list()
        )

    def cancel(self, job: JobId) -> Cmd[None]:
        proj_id: str = self._project.str_val
        job_id: str = _utils.int_to_str(job.job_id)
        return self._client.post(f"/projects/{proj_id}/jobs/{job_id}/cancel")
