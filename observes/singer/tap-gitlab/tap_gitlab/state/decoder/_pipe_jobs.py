from . import (
    _core,
)
from fa_purity import (
    FrozenDict,
    ResultE,
)
from fa_purity.json_2 import (
    JsonPrimitiveFactory,
    JsonPrimitiveUnfolder,
    JsonValue,
)
from fa_purity.json_2.value import (
    JsonObj,
    Unfolder,
)
from fa_purity.result.transform import (
    all_ok,
)
from tap_gitlab._utils import (
    decode as _decode,
)
from tap_gitlab.api.core.job import (
    JobStatus,
)
from tap_gitlab.api.core.pipeline import (
    PipelineStatus,
)
from tap_gitlab.state._objs import (
    EncodedObj,
    PipeJobsStreamKey,
    PipelineJobsState,
)
from typing import (
    FrozenSet,
    Tuple,
)


def _decode_key(
    raw: JsonObj,
) -> ResultE[PipeJobsStreamKey]:
    pipe_status = _decode.decode_required_key(
        raw,
        "pipe_status",
        lambda v: Unfolder.to_primitive(v).bind(JsonPrimitiveUnfolder.to_str),
    ).bind(PipelineStatus.from_raw)
    job_status = _decode.decode_required_key(
        raw,
        "job_status",
        lambda v: Unfolder.to_list_of(
            v,
            lambda x: Unfolder.to_primitive(x)
            .bind(JsonPrimitiveUnfolder.to_str)
            .bind(JobStatus.from_raw),
        ),
    )
    return pipe_status.bind(
        lambda ps: job_status.map(
            lambda js: PipeJobsStreamKey(ps, frozenset(js))
        )
    )


def _decode_value(raw: JsonValue) -> ResultE[PipelineJobsState]:
    return (
        Unfolder.to_json(raw)
        .bind(_core.i_decoder.decode_f_progress)
        .map(PipelineJobsState)
    )


def _decode_pair(
    key: JsonValue, value: JsonValue
) -> ResultE[Tuple[PipeJobsStreamKey, PipelineJobsState]]:
    return (
        Unfolder.to_json(key)
        .bind(_decode_key)
        .bind(lambda k: _decode_value(value).map(lambda v: (k, v)))
    )


def decode(
    item: EncodedObj,
) -> ResultE[FrozenDict[PipeJobsStreamKey, PipelineJobsState]]:
    return (
        _core.decode_dict(item)
        .map(lambda d: tuple(d.items()))
        .bind(lambda i: all_ok(tuple(_decode_pair(t[0], t[1]) for t in i)))
        .map(lambda d: FrozenDict(dict(d)))
    )
