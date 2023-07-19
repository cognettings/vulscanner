from fa_purity.json_2 import (
    LegacyAdapter,
)
from fa_singer_io.singer import (
    SingerState,
)
from tap_gitlab.state import (
    EtlState,
)
from tap_gitlab.state.encoder import (
    encode_etl_state,
)


def state_to_singer(state: EtlState) -> SingerState:
    encoded = LegacyAdapter.to_legacy_json(encode_etl_state(state))
    return SingerState(encoded)
