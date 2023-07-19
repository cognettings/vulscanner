from fa_purity import (
    PureIter,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_singer_io.singer import (
    SingerRecord,
)
from tap_gitlab.singer._core import (
    SingerStreams,
)
from tap_gitlab.streams.mrs import (
    MrsPage,
)


def mr_record(
    page: MrsPage,
) -> PureIter[SingerRecord]:
    return from_flist(page.data).map(
        lambda mr: SingerRecord(
            SingerStreams.merge_requests.value,
            mr,
            None,
        ),
    )
