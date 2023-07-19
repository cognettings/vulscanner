from . import (
    _core,
    _mr,
    _pipe_jobs,
)
from fa_purity import (
    ResultE,
)
from fa_purity.json_2.value import (
    JsonObj,
    Unfolder,
)
from tap_gitlab._utils import (
    decode,
)
from tap_gitlab.state._objs import (
    EtlState,
)


def decode_etl_state(raw: JsonObj) -> ResultE[EtlState]:
    _type = decode.require_restricted_str(raw, "type", ("EtlState",))
    raw_mrs = decode.decode_required_nested_keys(
        raw,
        ("obj", "mrs"),
        lambda v: Unfolder.to_json(v).bind(_mr.decode_mrstate_map),
    )
    raw_pipe_jobs = decode.decode_required_nested_keys(
        raw,
        ("obj", "pipe_jobs"),
        lambda v: _core.decode_obj(v).bind(_pipe_jobs.decode),
    )
    return _type.bind(
        lambda _: raw_mrs.bind(
            lambda mrs: raw_pipe_jobs.map(lambda pj: EtlState(pj, mrs))
        )
    )
