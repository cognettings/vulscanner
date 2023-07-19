from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from dateutil.parser import (
    isoparse,
)
from decimal import (
    Decimal,
)
from fa_purity import (
    JsonObj,
    JsonValue,
    Maybe,
    Result,
    ResultE,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.json_2 import (
    LegacyAdapter,
    Unfolder as Unfolder2,
)
from fa_purity.json_2.primitive import (
    JsonPrimitiveUnfolder,
)
from fa_purity.utils import (
    raise_exception,
)
from tap_gitlab import (
    _utils,
)
from tap_gitlab._utils import (
    decode,
)
from tap_gitlab.api.core.ids import (
    PipelineId,
    PipelineRelativeId,
    ProjectId,
    UserId,
)
from tap_gitlab.api.core.pipeline import (
    Pipeline,
    PipelineStatus,
)
from typing import (
    Tuple,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class PipelineObj:
    obj_id: PipelineId
    iid: PipelineRelativeId
    obj: Pipeline


@dataclass(frozen=True)
class HandledException(Exception):
    exception: Exception


_opt = Maybe.from_optional


def _handled(result: ResultE[_T]) -> _T:
    return (
        result.alt(lambda e: Exception(HandledException(e)))
        .alt(raise_exception)
        .unwrap()
    )


def _decode_str(value: JsonValue) -> str:
    result = (
        Unfolder(value)
        .to_primitive(str)
        .alt(lambda e: Exception(HandledException(e)))
    )
    return _handled(result)


def _decode_datetime(value: JsonValue) -> datetime:
    result = (
        Unfolder(value)
        .to_primitive(str)
        .alt(lambda e: Exception(HandledException(e)))
    )
    return isoparse(_handled(result))


def _decode_int(value: JsonValue) -> int:
    result = (
        Unfolder(value)
        .to_primitive(int)
        .alt(lambda e: Exception(HandledException(e)))
    )
    return _handled(result)


def _decode_decimal(value: JsonValue) -> Decimal:
    result = (
        Unfolder(value)
        .to_primitive(Decimal)
        .alt(lambda e: Exception(HandledException(e)))
    )
    return _handled(result)


def decode_pipeline(raw: JsonObj) -> ResultE[Pipeline]:
    try:
        result = Pipeline(
            _decode_str(raw["sha"]),
            _opt(raw.get("before_sha")).map(_decode_str),
            _decode_str(raw["ref"]),
            PipelineStatus(_decode_str(raw["status"]).lower()),
            _decode_str(raw["source"]),
            _opt(raw.get("duration")).map(_decode_decimal),
            _opt(raw.get("queued_duration")).map(_decode_decimal),
            UserId(_decode_int(raw["user"])),
            _decode_datetime(raw["created_at"]),
            _opt(raw.get("updated_at")).map(_decode_datetime),
            _opt(raw.get("started_at")).map(_decode_datetime),
            _opt(raw.get("finished_at")).map(_decode_datetime),
        )
        return Result.success(result)
    except HandledException as err:
        return Result.failure(err, Pipeline).alt(Exception)
    except KeyError as err:
        return Result.failure(err, Pipeline).alt(Exception)
    except ValueError as err:
        # handles PipelineStatus constructor and isoparse function errors
        return Result.failure(err, Pipeline).alt(Exception)


def _require_int(raw: JsonObj, key: str) -> ResultE[int]:
    return (
        _opt(raw.get(key))
        .to_result()
        .alt(lambda _: Exception(KeyError(key)))
        .bind(lambda j: Unfolder(j).to_primitive(int).alt(Exception))
    )


def decode_pipeline_ids(
    raw: JsonObj,
) -> ResultE[Tuple[PipelineId, PipelineRelativeId]]:
    _id = _require_int(raw, "id").map(PipelineId)
    _iid = _require_int(raw, "iid")
    project_id = _require_int(raw, "project_id").map(ProjectId.from_id)
    _rel_id = _iid.bind(
        lambda i: project_id.map(lambda p: PipelineRelativeId(p, i))
    )
    return _id.bind(lambda i: _rel_id.map(lambda r: (i, r)))


def decode_pipeline_obj(raw: JsonObj) -> ResultE[PipelineObj]:
    return decode_pipeline_ids(raw).bind(
        lambda ids: decode_pipeline(raw).map(
            lambda p: PipelineObj(ids[0], ids[1], p)
        )
    )


def decode_updated_at(raw: JsonObj) -> ResultE[datetime]:
    return decode.decode_required_key(
        LegacyAdapter.json(raw),
        "updated_at",
        lambda v: Unfolder2.to_primitive(v)
        .bind(JsonPrimitiveUnfolder.to_str)
        .bind(_utils.str_to_datetime),
    )
