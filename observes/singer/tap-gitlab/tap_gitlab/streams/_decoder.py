from ._core import (
    JobStream,
    MrStream,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    ResultE,
)
from fa_purity.json_2.primitive import (
    JsonPrimitiveUnfolder,
)
from fa_purity.json_2.value import (
    JsonObj,
    JsonValue,
    Unfolder,
)
from tap_gitlab._utils import (
    decode,
)
from tap_gitlab.api.core.ids import (
    ProjectId,
)
from tap_gitlab.api.jobs import (
    JobStatus,
)
from tap_gitlab.api.merge_requests import (
    Scope as MrScope,
    State as MrState,
)

_require = decode.decode_required_key


def _decode_proj(raw: JsonValue) -> ResultE[ProjectId]:
    return (
        Unfolder.to_primitive(raw)
        .bind(JsonPrimitiveUnfolder.to_str)
        .map(ProjectId.from_name)
    )


def _decode_mr_stream_obj(raw: JsonObj) -> ResultE[MrStream]:
    _project = _require(raw, "project", _decode_proj)
    _scope = _require(
        raw,
        "scope",
        lambda v: Unfolder.to_primitive(v)
        .bind(JsonPrimitiveUnfolder.to_str)
        .bind(MrScope.from_raw),
    )
    _state = _require(
        raw,
        "mr_state",
        lambda v: Unfolder.to_primitive(v)
        .bind(JsonPrimitiveUnfolder.to_str)
        .bind(MrState.from_raw),
    )
    return _project.bind(
        lambda proj: _scope.bind(
            lambda scope: _state.map(
                lambda state: MrStream(proj, scope, state)
            )
        )
    )


def _decode_job_stream_obj(raw: JsonObj) -> ResultE[JobStream]:
    _project = _require(raw, "project", _decode_proj)
    _scopes = _require(
        raw,
        "scopes",
        lambda v: Unfolder.to_list_of(
            v,
            lambda i: Unfolder.to_primitive(i).bind(
                lambda p: JsonPrimitiveUnfolder.to_str(p).bind(
                    JobStatus.from_raw
                )
            ),
        ),
    )
    return _project.bind(lambda p: _scopes.map(lambda s: JobStream(p, s)))


@dataclass(frozen=True)
class StreamDecoder:
    @staticmethod
    def decode_mr_stream(raw: JsonObj) -> ResultE[MrStream]:
        _type = decode.require_restricted_str(raw, "type", ("MrStream",))
        return _type.bind(
            lambda _: _require(
                raw,
                "obj",
                lambda v: Unfolder.to_json(v).bind(_decode_mr_stream_obj),
            )
        )

    @staticmethod
    def decode_job_stream(raw: JsonObj) -> ResultE[JobStream]:
        _type = decode.require_restricted_str(raw, "type", ("JobStream",))
        return _type.bind(
            lambda _: _require(
                raw,
                "obj",
                lambda v: Unfolder.to_json(v).bind(_decode_job_stream_obj),
            )
        )
