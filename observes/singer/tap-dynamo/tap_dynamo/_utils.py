from fa_purity import (
    Cmd,
    FrozenList,
)
from fa_purity.cmd.transform import (
    merge,
)
from pathos.pools import (  # type: ignore[import]
    ThreadPool,
)
from typing import (
    TypeVar,
)

_T = TypeVar("_T")


def threads_map(cmds: FrozenList[Cmd[_T]]) -> Cmd[FrozenList[_T]]:
    pool = ThreadPool()  # type: ignore[misc]
    result = merge(
        lambda u, items: tuple(pool.map(u, items)),  # type: ignore[misc]
        cmds,
    )
    return result
