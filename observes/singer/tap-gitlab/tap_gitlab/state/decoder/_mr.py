from . import (
    _core,
)
from fa_purity import (
    FrozenList,
    ResultE,
)
from fa_purity.json_2.value import (
    JsonObj,
    JsonValue,
    Unfolder,
)
from tap_gitlab._utils import (
    decode,
)
from tap_gitlab.state._objs import (
    MrStateMap,
    MrStreamState,
)
from tap_gitlab.streams import (
    MrStream,
)
from typing import (
    Tuple,
)


def decode_mrstm_state(raw: JsonObj) -> ResultE[MrStreamState]:
    _type = decode.require_restricted_str(raw, "type", ("MrStreamState",))
    return _type.bind(
        lambda _: decode.decode_required_nested_keys(
            raw,
            ("obj", "state"),
            lambda v: Unfolder.to_json(v).bind(
                _core.i_decoder.decode_f_progress
            ),
        ).map(MrStreamState)
    )


def _decode_mrstate_map_pair(
    raw: FrozenList[JsonValue],
) -> ResultE[Tuple[MrStream, MrStreamState]]:
    raw_stm = (
        decode.require_index(raw, 0)
        .bind(Unfolder.to_json)
        .bind(_core.s_decoder.decode_mr_stream)
    )
    raw_state = (
        decode.require_index(raw, 1)
        .bind(Unfolder.to_json)
        .bind(decode_mrstm_state)
    )
    return raw_stm.bind(lambda stm: raw_state.map(lambda s: (stm, s)))


def _decode_mrstate_map_obj(raw: JsonValue) -> ResultE[MrStateMap]:
    return Unfolder.to_list_of(
        raw,
        lambda v: Unfolder.to_list(v).bind(_decode_mrstate_map_pair),
    ).map(lambda x: MrStateMap(dict(x)))


def decode_mrstate_map(raw: JsonObj) -> ResultE[MrStateMap]:
    _type = decode.require_restricted_str(raw, "type", ("MrStateMap",))
    return _type.bind(
        lambda _: decode.decode_required_nested_keys(
            raw,
            ("obj", "items"),
            _decode_mrstate_map_obj,
        )
    )
