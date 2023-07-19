from custom_utils.datetime import (
    get_minus_delta,
    get_plus_delta,
    get_utc_now,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsRequest,
    CredentialsState,
    OauthAzureSecret,
    OauthBitbucketSecret,
    OauthGitlabSecret,
)
from oauth.utils import (
    update_token,
)
import pytest
import pytz


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_oauth_credentials_token")
@pytest.mark.parametrize(
    ["secret", "modified_date", "credential_request"],
    [
        [
            OauthBitbucketSecret(
                brefresh_token="new_token",
                access_token="new_access_token",
                valid_until=get_plus_delta(
                    get_minus_delta(get_utc_now(), seconds=60),
                    seconds=int(36000),
                ),
            ),
            datetime.now(tz=pytz.timezone("UTC")),
            CredentialsRequest(
                id="b124134-22ca-4bca-96a8-448f80a6580f",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            ),
        ],
        [
            OauthAzureSecret(
                access_token="new_access_token",
                redirect_uri="https://fluidattacks/home",
                arefresh_token="refresh_token",
                valid_until=get_plus_delta(
                    get_minus_delta(get_utc_now(), seconds=60),
                    seconds=int(36000),
                ),
            ),
            datetime.now(tz=pytz.timezone("UTC")),
            CredentialsRequest(
                id="b224134-22ca-4bca-96a8-448f80a6580f",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            ),
        ],
        [
            OauthGitlabSecret(
                access_token="new_access_token",
                redirect_uri="https://fluidattacks/home",
                refresh_token="refresh_token",
                valid_until=get_plus_delta(
                    get_minus_delta(get_utc_now(), seconds=60),
                    seconds=int(36000),
                ),
            ),
            datetime.now(tz=pytz.timezone("UTC")),
            CredentialsRequest(
                id="b324134-22ca-4bca-96a8-448f80a6580f",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            ),
        ],
    ],
)
async def test_update_token(
    populate: bool,
    secret: OauthAzureSecret | OauthBitbucketSecret | OauthGitlabSecret,
    modified_date: datetime,
    credential_request: CredentialsRequest,
) -> None:
    assert populate
    loaders = get_new_context()
    credential: Credentials | None = await loaders.credentials.load(
        credential_request
    )
    assert credential
    new_state = CredentialsState(
        modified_by=credential.state.modified_by,
        modified_date=modified_date,
        name=credential.state.name,
        secret=secret,
        is_pat=credential.state.is_pat,
        azure_organization=credential.state.azure_organization,
        type=credential.state.type,
    )

    await update_token(
        credential_id=credential_request.id,
        organization_id=credential_request.organization_id,
        loaders=loaders,
        secret=secret,
        modified_date=modified_date,
    )
    loaders.credentials.clear_all()
    updated_credential: Credentials | None = await loaders.credentials.load(
        credential_request
    )
    assert updated_credential
    assert updated_credential.state == new_state
