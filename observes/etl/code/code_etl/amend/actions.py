from . import (
    core,
)
from .core import (
    AmendUsers,
)
from code_etl.client import (
    Client,
    CommitStampDiff,
)
from code_etl.clients import (
    new_client as code_client,
)
from code_etl.mailmap import (
    Mailmap,
)
from code_etl.objs import (
    CommitStamp,
    RepoRegistration,
)
from fa_purity import (
    Cmd,
    Maybe,
    Stream,
)
from fa_purity.union import (
    Coproduct,
)
import logging
from redshift_client.sql_client import (
    new_client,
)
from redshift_client.sql_client.connection import (
    DbConnection,
)
from typing import (
    Callable,
)

LOG = logging.getLogger(__name__)


def fetch_and_transform_per_namespace(
    connection: DbConnection,
    namespace: str,
    action: Callable[
        [Client, Stream[Coproduct[CommitStamp, RepoRegistration]]], Cmd[None]
    ],
) -> Cmd[None]:
    sql_client_1 = new_client(connection, LOG.getChild("sql_client_1"))
    sql_client_2 = new_client(connection, LOG.getChild("sql_client_2"))
    fetch_client = sql_client_1.map(code_client)
    client2 = sql_client_2.map(code_client)

    def _classify(
        item: CommitStamp | RepoRegistration,
    ) -> Coproduct[CommitStamp, RepoRegistration]:
        if isinstance(item, CommitStamp):
            return Coproduct.inl(item)
        return Coproduct.inr(item)

    data = fetch_client.bind(
        lambda c: c.namespace_data(namespace).map(
            lambda s: s.map(lambda r: r.map(_classify).unwrap())
        )
    )
    return data.bind(lambda data: client2.bind(lambda c: action(c, data)))


def amend_stamp(
    client: Client,
    mailmap: Maybe[Mailmap],
    item: CommitStamp,
) -> Cmd[None]:
    fixed = (
        mailmap.map(AmendUsers)
        .map(lambda a: a.amend_commit_stamp_users(item))
        .value_or(item)
    )
    return client.delta_update(
        CommitStampDiff.from_stamps(item, fixed).unwrap()
    )


def re_calculate_hash_action(
    client: Client,
    item: CommitStamp,
) -> Cmd[None]:
    fixed = core.re_calculate_hash(item)
    msg = Cmd.from_cmd(
        lambda: LOG.info(
            "Re-calculating fa-hash for %s", item.commit.commit_id.hash.hash
        )
    )
    return msg + client.delta_update(
        CommitStampDiff.from_stamps(item, fixed).unwrap()
    )
