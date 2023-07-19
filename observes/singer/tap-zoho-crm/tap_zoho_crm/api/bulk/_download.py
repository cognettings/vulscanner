from ._objs import (
    BulkData,
    BulkJobId,
)
from fa_purity import (
    Cmd,
    FrozenDict,
)
from fa_purity.json_2 import (
    JsonObj,
    Primitive,
    UnfoldedFactory,
)
from fa_purity.utils import (
    raise_exception,
)
import logging
from pure_requests import (
    basic,
)
from pure_requests.rate_limit import (
    RateLimiter,
)
from requests import (
    Response,
)
from tap_zoho_crm.api.common import (
    API_URL,
    Token,
    UnexpectedResponse,
)
import tempfile
from typing import (
    Dict,
    IO,
)
from zipfile import (
    ZipFile,
)

API_ENDPOINT = API_URL + "/crm/bulk/v2/read"
LOG = logging.getLogger(__name__)


def download_result(
    rate_limiter: RateLimiter, token: Token, job_id: BulkJobId
) -> Cmd[BulkData]:
    def _unzip(response: Response) -> Cmd[BulkData]:
        def _action() -> BulkData:
            # pylint: disable=consider-using-with
            # need refac of BulkData for enabling the above check
            tmp_zipdir = tempfile.mkdtemp()
            file_zip: IO[bytes] = tempfile.NamedTemporaryFile(mode="wb+")
            file_unzip: IO[str] = tempfile.NamedTemporaryFile(
                mode="w+", encoding="utf-8"
            )
            file_zip.write(response.content)
            file_zip.seek(0)
            LOG.debug("Unzipping file")
            with ZipFile(file_zip, "r") as zip_obj:
                files = zip_obj.namelist()
                if len(files) > 1:
                    raise UnexpectedResponse("Zip file with multiple files.")
                zip_obj.extract(files[0], tmp_zipdir)
            LOG.debug("Generating BulkData")
            with open(
                tmp_zipdir + f"/{files[0]}", "r", encoding="UTF-8"
            ) as unzipped:
                file_unzip.write(unzipped.read())
            LOG.debug("Unzipped size: %s", file_unzip.tell())
            return BulkData(job_id, file_unzip)

        return Cmd.from_cmd(_action)

    msg = Cmd.from_cmd(lambda: LOG.info("API: Download bulk job #%s", job_id))
    endpoint = f"{API_ENDPOINT}/" + job_id.job_id + "/result"
    headers: Dict[str, Primitive] = {
        "Authorization": "Zoho-oauthtoken " + token.raw_token
    }
    empty: JsonObj = FrozenDict({})
    cmd = msg + (
        basic.get(endpoint, UnfoldedFactory.from_dict(headers), empty)
        .map(lambda r: r.alt(raise_exception).unwrap())
        .bind(_unzip)
    )
    return rate_limiter.call_or_wait(cmd)
