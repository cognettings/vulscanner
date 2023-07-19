from fa_purity import (
    Cmd,
)
from fa_purity.pure_iter import (
    factory as PureIterFactory,
)
import pytest
from target_s3._parallel import (
    ThreadPool,
)
from time import (
    sleep,
)


def mock_job() -> Cmd[None]:
    return Cmd.from_cmd(lambda: sleep(1))


@pytest.mark.timeout(5)
def test_threads() -> None:
    # this tests needs at least 2 threads to succeed
    jobs = PureIterFactory.from_range(range(10)).map(lambda _: mock_job())
    with pytest.raises(SystemExit):
        try:
            ThreadPool.new(10).bind(lambda p: p.in_threads(jobs)).compute()
        except SystemExit as sys_exit:
            assert sys_exit.code == 0
            raise sys_exit
