from . import (
    actions,
)
from code_etl import (
    _utils,
)
from code_etl.client import (
    Client,
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
from fa_purity.stream.transform import (
    consume,
)
from fa_purity.union import (
    Coproduct,
)
import logging
from redshift_client.sql_client.connection import (
    connect,
    Credentials,
    DatabaseId,
    IsolationLvl,
)
from typing import (
    Callable,
)

LOG = logging.getLogger(__name__)


def _base(
    db_id: DatabaseId,
    creds: Credentials,
    namespace: str,
    action: Callable[
        [Client, Stream[Coproduct[CommitStamp, RepoRegistration]]], Cmd[None]
    ],
) -> Cmd[None]:
    connection = connect(
        db_id,
        creds,
        False,
        IsolationLvl.AUTOCOMMIT,
    )
    return _utils.wrap_connection(
        connection,
        lambda c: actions.fetch_and_transform_per_namespace(
            c,
            namespace,
            action,
        ),
    )


def amend_users(
    db_id: DatabaseId,
    creds: Credentials,
    namespace: str,
    mailmap: Maybe[Mailmap],
) -> Cmd[None]:
    mutation_msg = Cmd.from_cmd(
        lambda: LOG.info("Mutation `amend_users` started")
    )
    return _base(
        db_id,
        creds,
        namespace,
        lambda client, data: mutation_msg
        + data.map(
            lambda u: u.map(
                lambda stamp: actions.amend_stamp(client, mailmap, stamp),
                lambda _: Cmd.from_cmd(lambda: None),
            )
        ).transform(consume),
    )


def re_calc_fa_hash(
    db_id: DatabaseId,
    creds: Credentials,
    namespace: str,
) -> Cmd[None]:
    mutation_msg = Cmd.from_cmd(
        lambda: LOG.info("Mutation `re_calc_fa_hash` started")
    )
    return _base(
        db_id,
        creds,
        namespace,
        lambda client, data: mutation_msg
        + data.map(
            lambda u: u.map(
                lambda stamp: actions.re_calculate_hash_action(client, stamp),
                lambda _: Cmd.from_cmd(lambda: None),
            )
        ).transform(consume),
    )
