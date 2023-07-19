from fa_purity import (
    Cmd,
    Result,
)
from fa_purity.pure_iter.factory import (
    from_range,
)
from fa_purity.stream.factory import (
    from_piter,
)
import logging
from time import (
    sleep,
)
from typing import (
    Callable,
    TypeVar,
)

LOG = logging.getLogger(__name__)
_S = TypeVar("_S")
_F = TypeVar("_F")


class MaxRetriesReached(Exception):
    pass


def retry_cmd(
    cmd: Cmd[Result[_S, _F]],
    next_cmd: Callable[[int, Result[_S, _F]], Cmd[Result[_S, _F]]],
    max_retries: int,
) -> Cmd[Result[_S, MaxRetriesReached]]:
    cmds = from_range(range(0, max_retries + 1)).map(
        lambda i: cmd.bind(
            lambda r: next_cmd(i + 1, r)
            if i + 1 <= max_retries
            else Cmd.from_cmd(lambda: r)
        )
    )
    return (
        from_piter(cmds)
        .find_first(
            lambda x: x.map(lambda _: True).alt(lambda _: False).to_union()
        )
        .map(
            lambda x: x.map(lambda r: r.unwrap())
            .to_result()
            .alt(lambda _: MaxRetriesReached(max_retries))
        )
    )


def cmd_if_fail(
    result: Result[_S, _F],
    cmd: Cmd[None],
) -> Cmd[Result[_S, _F]]:
    def _cmd(err: _F) -> Cmd[Result[_S, _F]]:
        fail: Result[_S, _F] = Result.failure(err)
        return cmd.map(lambda _: fail)

    return (
        result.map(lambda _: Cmd.from_cmd(lambda: result)).alt(_cmd).to_union()
    )


def sleep_cmd(delay: float) -> Cmd[None]:
    return Cmd.from_cmd(lambda: sleep(delay))
