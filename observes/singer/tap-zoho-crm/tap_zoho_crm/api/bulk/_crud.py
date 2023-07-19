from . import (
    _create,
    _download,
    _get,
)
from ._objs import (
    BulkData,
    BulkJob,
    BulkJobId,
    BulkJobObj,
    ModuleName,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from fa_purity.cmd import (
    unsafe_unwrap,
)
from fa_purity.lock import (
    ThreadLock,
)
import logging
from pure_requests.rate_limit import (
    RateLimiter,
)
from tap_zoho_crm.api.common import (
    API_URL,
    Token,
)
from typing import (
    Callable,
)

API_ENDPOINT = API_URL + "/crm/bulk/v2/read"
LOG = logging.getLogger(__name__)
_rate_limiter = ThreadLock.new().map(
    lambda lock: RateLimiter.new(10, 60, lock).unwrap()
)
rate_limiter = unsafe_unwrap(_rate_limiter)


@dataclass(frozen=True)
class BulkJobApi:
    get: Callable[[BulkJobId], Cmd[BulkJob]]
    new: Callable[[ModuleName, int], Cmd[BulkJobObj]]  # (module, page) -> job
    download: Callable[[BulkJobId], Cmd[BulkData]]


@dataclass(frozen=True)
class BulkJobApiFactory:
    @staticmethod
    def bulk_job_api(token: Token) -> BulkJobApi:
        return BulkJobApi(
            lambda j: _get.get_bulk_job(token, j),
            lambda module, page: _create.create_bulk_read_job(
                rate_limiter, token, module, page
            ),
            lambda j: _download.download_result(rate_limiter, token, j),
        )
