from fa_purity import (
    Cmd,
)
from fa_purity.cmd import (
    CmdUnwrapper,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    from_range,
)
from os import (
    kill,
)
import pytest
from random import (
    random,
)
from tap_dynamo._utils import (
    threads_map,
)
from tempfile import (
    NamedTemporaryFile,
)
from time import (
    sleep,
)
from typing import (
    IO,
)


def random_sleep() -> Cmd[None]:
    return Cmd.from_cmd(lambda: sleep(random()))


def emit(file: IO[str], index: int) -> Cmd[None]:
    return random_sleep() + Cmd.from_cmd(
        lambda: file.write(f"test-{index}\n")
    ).map(lambda _: None)


def test_parallel_write() -> None:
    expected = frozenset(from_range(range(10)).map(lambda i: f"test-{i}"))
    out = NamedTemporaryFile("w", delete=False)

    def _save(unwrapper: CmdUnwrapper) -> None:
        with open(out.name, "w") as f:
            cmds = from_range(range(10)).map(lambda i: emit(f, i)).to_list()
            unwrapper.act(threads_map(cmds))

    save = Cmd.new_cmd(_save)

    def _read() -> None:
        with open(out.name, "r") as f:
            result = from_flist(tuple(f.readlines())).map(lambda s: s.rstrip())
            print(result.to_list())
            assert frozenset(result) == expected

    read = Cmd.from_cmd(_read)

    with pytest.raises(SystemExit):
        (save + read).compute()
