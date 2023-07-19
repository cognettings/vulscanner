from __future__ import (
    annotations,
)

from collections.abc import (
    Iterable,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    Maybe,
    PureIter,
    Result,
    ResultE,
)
from fa_purity.cmd import (
    CmdUnwrapper,
)
import logging
from pathos.threading import (  # type: ignore[import]
    ThreadPool as _RawThreadPool,
)
from redshift_client.client.table import (
    TableClient,
)
from redshift_client.core.id_objs import (
    DbTableId,
)
from redshift_client.core.table import (
    Table,
)
from redshift_client.sql_client import (
    Query,
    QueryValues,
    SqlClient,
)
from typing import (
    cast,
    Tuple,
)

LOG = logging.getLogger(__name__)


def set_queue_group(client: SqlClient, group: str) -> Cmd[None]:
    statement = "SET query_group TO %(group)s"
    args = QueryValues(FrozenDict({"group": group}))
    return client.execute(Query.new_query(statement), args)


@dataclass(frozen=True)  # type: ignore[misc]
class _ThreadPool:  # type: ignore[no-any-unimported]
    pool: _RawThreadPool  # type: ignore[no-any-unimported]


@dataclass(frozen=True)
class ThreadPool:
    _inner: _ThreadPool

    @staticmethod
    def new(nodes: int) -> Cmd[ThreadPool]:
        return Cmd.from_cmd(
            lambda: ThreadPool(_ThreadPool(_RawThreadPool(nodes=nodes)))  # type: ignore[misc]
        )

    def in_threads(self, commands: PureIter[Cmd[None]]) -> Cmd[None]:
        def _action(act: CmdUnwrapper) -> None:
            results: Iterable[None] = cast(
                Iterable[None],
                self._inner.pool.imap(lambda c: act.unwrap(c), commands),  # type: ignore[misc]
            )
            for _ in results:
                # compute ThreadPool jobs
                pass

        return Cmd.new_cmd(_action)


def add_missing_columns(
    client: TableClient,
    source: Table,
    target: Tuple[DbTableId, Table],
) -> Cmd[None]:
    "add missing columns to target in respect to source"
    missing_columns = frozenset(source.columns.keys()) - frozenset(
        target[1].columns.keys()
    )
    missing = FrozenDict(
        {
            m: Maybe.from_optional(source.columns.get(m)).unwrap()
            for m in missing_columns
        }
    )
    msg = Cmd.from_cmd(
        lambda: LOG.info(
            "adding missing columns (%s) into %s", missing_columns, target[0]
        )
    )
    return msg + client.add_columns(target[0], missing)
