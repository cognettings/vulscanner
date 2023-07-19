from . import (
    _core,
)
from fa_purity import (
    FrozenDict,
)
from fa_purity.json_2 import (
    JsonPrimitiveFactory,
    JsonValue,
)
from tap_gitlab.state._objs import (
    EncodedObj,
    PipeJobsStreamKey,
    PipelineJobsState,
)


def _encode_key(item: PipeJobsStreamKey) -> JsonValue:
    _raw = {
        "pipe_status": JsonValue.from_primitive(
            JsonPrimitiveFactory.from_raw(item.status.value)
        ),
        "job_status": JsonValue.from_list(
            tuple(
                JsonValue.from_primitive(
                    JsonPrimitiveFactory.from_raw(i.value)
                )
                for i in item.jobs_status
            )
        ),
    }
    return JsonValue.from_json(FrozenDict(_raw))


def _encode_value(item: PipelineJobsState) -> JsonValue:
    return JsonValue.from_json(_core.i_encoder.encode_f_progress(item.state))


def encode(
    item: FrozenDict[PipeJobsStreamKey, PipelineJobsState]
) -> EncodedObj:
    return _core.encode_dict(item, _encode_key, _encode_value)
