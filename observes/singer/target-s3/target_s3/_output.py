from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    Stream,
)
from fa_purity.stream.transform import (
    squash,
)
from fa_singer_io.singer import (
    SingerMessage,
)
from fa_singer_io.singer.emitter import (
    emit,
)
from typing import (
    TextIO,
)


@dataclass(frozen=True)
class OutputEmitter:
    _data: Stream[SingerMessage]
    _target: TextIO

    def re_emit(self) -> Stream[SingerMessage]:
        return squash(
            self._data.map(
                lambda m: emit(self._target, m) + Cmd.from_cmd(lambda: m)
            )
        )
