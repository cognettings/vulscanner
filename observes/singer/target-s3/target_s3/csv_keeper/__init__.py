from ._core import (
    CsvKeeper,
)
from ._format import (
    RawFormatedRecord,
)
from ._writer import (
    multifile_save,
    save_raw,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    PureIter,
)
from fa_purity.pure_iter.factory import (
    from_list,
)
import logging
from target_s3 import (
    _utils,
)
from target_s3._parallel import (
    ThreadPool,
)
from target_s3.core import (
    RecordGroup,
    TempReadOnlyFile,
)
from typing import (
    Callable,
    TypeVar,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


def _save_group(
    group: RecordGroup,
    str_limit: int,
    save_cmd: Callable[[PureIter[RawFormatedRecord]], Cmd[_T]],
) -> Cmd[_T]:
    msg = _utils.log_cmd(
        lambda: LOG.info(
            "Saving stream `%s` data into temp", group.schema.stream
        ),
        None,
    )
    return msg + RawFormatedRecord.format_group_records(
        group, str_limit
    ).transform(save_cmd).bind(
        lambda t: _utils.log_cmd(
            lambda: LOG.info(
                "Stream `%s` saved into temp file!", group.schema.stream
            ),
            t,
        )
    )


@dataclass(frozen=True)
class CsvKeeperFactory:
    pool: ThreadPool

    def keeper_1(self, str_limit: int) -> CsvKeeper[TempReadOnlyFile]:
        return CsvKeeper(
            lambda r: _save_group(
                r, str_limit, lambda d: save_raw(self.pool, d)
            )
        )

    def keeper_2(
        self, str_limit: int, chunks: int, parts: int
    ) -> CsvKeeper[PureIter[TempReadOnlyFile]]:
        return CsvKeeper(
            lambda r: _save_group(
                r,
                str_limit,
                lambda d: multifile_save(self.pool, d, chunks, parts),
            ).map(from_list)
        )


__all__ = [
    "CsvKeeper",
]
