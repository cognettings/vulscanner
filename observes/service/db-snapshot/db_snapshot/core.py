import boto3
from fa_purity import (
    Cmd,
    FrozenList,
    Maybe,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
)
from fa_purity.date_time import (
    DatetimeFactory,
    DatetimeUTC,
)
import logging
import sys
from typing import (
    NoReturn,
    TypeVar,
)

LOG = logging.getLogger(__name__)

_T = TypeVar("_T")


def snapshot_name() -> Cmd[str]:
    def _name(now: DatetimeUTC) -> str:
        diff = (
            now.date_time - DatetimeFactory.EPOCH_START.date_time
        ).total_seconds()
        return f"db-snapshot-{round(diff)}"

    return DatetimeFactory.date_now().map(_name)


def _get(items: FrozenList[_T], index: int) -> Maybe[_T]:
    try:
        return Maybe.from_value(items[index])
    except IndexError:
        return Maybe.empty()


def create_snapshot(dry_run: bool) -> Cmd[None]:
    def _action(unwrapper: CmdUnwrapper) -> None:
        client = boto3.client("redshift")
        name = unwrapper.act(snapshot_name())
        if dry_run:
            LOG.info(f"The snapshot `{name}` would have been created")
        else:
            LOG.info(f"Creating snapshot `{name}`")
            client.create_cluster_snapshot(
                SnapshotIdentifier=name,
                ClusterIdentifier="observes",
                ManualSnapshotRetentionPeriod=20 * 30,  # 20 months
            )

    return Cmd.new_cmd(_action)


def _cmd_selection(flag: str) -> Cmd[None]:
    if flag == "--help":
        return Cmd.from_cmd(lambda: None)
    if flag == "--dry-run":
        return create_snapshot(True)
    raise Exception(f"Unexpected flag {flag}")


def cmd_selection(flag: Maybe[str]) -> Cmd[None]:
    return flag.map(_cmd_selection).value_or(create_snapshot(False))


def main() -> NoReturn:
    """
    Main entrypoint

    [WARNING] Hidden inputs required:
    - AWS credentials with power to create a cluster snapshot
    """
    args = tuple(sys.argv[1:])
    cmd_selection(_get(args, 0)).compute()
