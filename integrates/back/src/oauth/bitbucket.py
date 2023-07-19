from aiohttp import (
    BasicAuth,
    ClientSession,
    FormData,
)
from aiohttp.client_exceptions import (
    ClientError,
)
import asyncio
from context import (
    FI_BITBUCKET_OAUTH2_REPOSITORY_APP_ID,
    FI_BITBUCKET_OAUTH2_REPOSITORY_SECRET,
)
from custom_exceptions import (
    ErrorUpdatingCredential,
    InvalidAuthorization,
)
from custom_utils.datetime import (
    get_minus_delta,
    get_plus_delta,
    get_utc_now,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    Credentials,
    OauthBitbucketSecret,
)
import json
import logging
import logging.config
from oauth.utils import (
    get_credential_or_token,
    update_token,
)
import pytz
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
BITBUCKET_REFRESH_URL = "https://bitbucket.org/site/oauth2/access_token"
BITBUCKET_AUTHZ_URL = "https://bitbucket.org/site/oauth2/authorize"

BITBUCKET_REPOSITORY_ARGS = dict(
    name="bitbucket",
    authorize_url=BITBUCKET_AUTHZ_URL,
    client_id=FI_BITBUCKET_OAUTH2_REPOSITORY_APP_ID,
    client_secret=FI_BITBUCKET_OAUTH2_REPOSITORY_SECRET,
    client_kwargs={"scope": "account project"},
)


async def get_bitbucket_refresh_token(
    *,
    code: str,
    redirect_uri: str,
) -> dict | None:
    request_parameters: dict[str, str] = dict(
        code=code,
        grant_type="authorization_code",
        redirect_uri=redirect_uri,
    )
    data = FormData()
    for key, value in request_parameters.items():
        data.add_field(key, value)
    retries: int = 0
    retry: bool = True
    async with ClientSession() as session:
        while retry and retries < 5:
            retry = False
            async with session.post(
                BITBUCKET_REFRESH_URL,
                data=data,
                auth=BasicAuth(
                    login=FI_BITBUCKET_OAUTH2_REPOSITORY_APP_ID,
                    password=FI_BITBUCKET_OAUTH2_REPOSITORY_SECRET,
                ),
            ) as response:
                try:
                    result = await response.json()
                except (
                    json.decoder.JSONDecodeError,
                    ClientError,
                ) as exc:
                    LOGGER.exception(exc, extra=dict(extra=locals()))
                    break
                if not response.ok:
                    retry = True
                    retries += 1
                    await asyncio.sleep(0.2)
                    continue

                return result

    return None


async def get_bitbucket_token(
    *,
    credential: Credentials,
    loaders: Dataloaders,
) -> str | None:
    _credential = await get_credential_or_token(
        credential=credential,
        loaders=loaders,
    )
    if isinstance(_credential, str):
        return _credential

    credential = _credential
    if not isinstance(credential.state.secret, OauthBitbucketSecret):
        return None

    request_parameters: dict[str, str] = dict(
        grant_type="refresh_token",
        refresh_token=credential.state.secret.brefresh_token,
    )
    data = FormData()
    for key, value in request_parameters.items():
        data.add_field(key, value)
    retries: int = 0
    retry: bool = True
    async with ClientSession() as session:
        while retry and retries < 5:
            retry = False
            async with session.post(
                BITBUCKET_REFRESH_URL,
                data=data,
                auth=BasicAuth(
                    login=FI_BITBUCKET_OAUTH2_REPOSITORY_APP_ID,
                    password=FI_BITBUCKET_OAUTH2_REPOSITORY_SECRET,
                ),
            ) as response:
                try:
                    result = await response.json()
                except (
                    json.decoder.JSONDecodeError,
                    ClientError,
                ) as exc:
                    LOGGER.exception(exc, extra=dict(extra=locals()))
                    break
                if not response.ok:
                    retry = True
                    retries += 1
                    await asyncio.sleep(0.2)
                    continue

                try:
                    await update_token(
                        credential_id=credential.id,
                        loaders=loaders,
                        organization_id=credential.organization_id,
                        secret=OauthBitbucketSecret(
                            brefresh_token=result["refresh_token"],
                            access_token=result["access_token"],
                            valid_until=get_plus_delta(
                                get_minus_delta(get_utc_now(), seconds=60),
                                seconds=int(result["expires_in"]),
                            ),
                        ),
                        modified_date=datetime.now(tz=pytz.timezone("UTC")),
                    )
                except ErrorUpdatingCredential as error:
                    LOGGER.error(
                        error, extra=dict(credential_owner=credential.owner)
                    )
                    raise InvalidAuthorization() from error

                loaders.credentials.clear_all()
                loaders.organization_credentials.clear(
                    credential.organization_id
                )

                return result["access_token"]

    return None
