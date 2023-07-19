from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    date,
)
from fa_purity import (
    Cmd,
    FrozenList,
    Result,
    ResultE,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
    new_cmd,
)
import logging
from os import (
    environ,
)
from pathos.threading import (  # type: ignore[import]
    ThreadPool,
)
from redshift_client.sql_client import (
    DbConnection,
)
from redshift_client.sql_client.connection import (
    Credentials,
    DatabaseId,
)
from typing import (
    Callable,
    TypeVar,
)

LOG = logging.getLogger(__name__)
COMMIT_HASH_SENTINEL: str = "-" * 40


def get_db_id() -> DatabaseId:
    return DatabaseId(
        environ["REDSHIFT_DATABASE"],
        environ["REDSHIFT_HOST"],
        int(environ["REDSHIFT_PORT"]),
    )


def get_db_creds() -> Credentials:
    return Credentials(
        environ["REDSHIFT_USER"],
        environ["REDSHIFT_PASSWORD"],
    )


_T = TypeVar("_T")


def log_info(log: logging.Logger, msg: str, *args: str) -> Cmd[None]:
    return Cmd.from_cmd(lambda: log.info(msg, *args))


def wrap_connection(
    new_connection: Cmd[DbConnection],
    action: Callable[[DbConnection], Cmd[_T]],
) -> Cmd[_T]:
    """Ensures that connection is closed regardless of action errors"""

    def _inner(connection: DbConnection) -> Cmd[_T]:
        def _action(act: CmdUnwrapper) -> _T:
            try:
                return act.unwrap(action(connection))
            finally:
                act.unwrap(connection.close())

        return new_cmd(_action)

    return new_connection.bind(_inner)


def cmds_in_threads(cmds: FrozenList[Cmd[None]]) -> Cmd[None]:
    def _action(act: CmdUnwrapper) -> None:
        pool = ThreadPool()  # type: ignore[misc]
        LOG.debug("Concurrent action started!")
        pool.map(  # type: ignore[misc]
            act.unwrap,
            cmds,
        )

    return new_cmd(_action)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class Date:
    "Purified `date` wrapper"
    _private: _Private = field(repr=False, hash=False, compare=False)
    _inner: date
    year: int
    month: int
    day: int

    @staticmethod
    def new(year: int, month: int, day: int) -> ResultE[Date]:
        try:
            obj = date(year, month, day)
            return Result.success(
                Date(_Private(), obj, obj.year, obj.month, obj.day)
            )
        except ValueError as err:
            return Result.failure(Exception(err))

    def strftime(self, _format: str) -> str:
        return self._inner.strftime(_format)
