from .bin_sdk.tap import (
    TapConfig,
    TapGoogleSheets,
)
from .utils.get_secret import (
    get_secret,
)
from fa_purity import (
    Cmd,
    FrozenList,
    Maybe,
)
import logging
from pathlib import (
    Path,
)
import sys
from typing import (
    NoReturn,
    TypeVar,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


def _get_index(items: FrozenList[_T], index: int) -> Maybe[_T]:
    try:
        return Maybe.from_value(items[index])
    except IndexError:
        return Maybe.empty()


def main() -> NoReturn:
    def _conf_ctx(conf: TapConfig) -> Cmd[None]:
        return (
            TapGoogleSheets.new(conf)
            .discover(sys.stdout, sys.stderr)
            .map(lambda r: r.unwrap())
        )

    execute = (
        _get_index(tuple(sys.argv), 1)
        .map(lambda x: x == "run")
        .value_or(False)
    )
    cmd: Cmd[None] = (
        (
            get_secret(Path("./secrets/conf.json"))
            .map(lambda r: TapConfig.decode(r).unwrap())
            .bind(_conf_ctx)
        )
        if execute
        else Cmd.from_cmd(lambda: None)
    )
    cmd.compute()
