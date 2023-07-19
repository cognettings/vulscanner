from custom_exceptions import (
    ErrorUpdatingCredential,
)
from custom_utils.datetime import (
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
    CredentialsRequest,
    CredentialsState,
    OauthAzureSecret,
    OauthBitbucketSecret,
    OauthGitlabSecret,
)
from db_model.credentials.update import (
    update_credential_state,
)
from decorators import (
    retry_on_exceptions,
)


async def get_credential_or_token(
    *, credential: Credentials, loaders: Dataloaders
) -> str | Credentials:
    loaders.credentials.clear(
        CredentialsRequest(
            id=credential.id,
            organization_id=credential.organization_id,
        )
    )
    _credential = await loaders.credentials.load(
        CredentialsRequest(
            id=credential.id,
            organization_id=credential.organization_id,
        )
    )
    if not _credential:
        return credential

    if (
        _credential.state.modified_date > credential.state.modified_date
        and isinstance(
            _credential.state.secret,
            (OauthAzureSecret | OauthBitbucketSecret | OauthGitlabSecret),
        )
        and _credential.state.secret.valid_until > get_utc_now()
    ):
        return _credential.state.secret.access_token

    return _credential


@retry_on_exceptions(
    exceptions=(ErrorUpdatingCredential,),
    max_attempts=3,
    sleep_seconds=float("2"),
)
async def update_token(
    credential_id: str,
    loaders: Dataloaders,
    organization_id: str,
    secret: (OauthAzureSecret | OauthBitbucketSecret | OauthGitlabSecret),
    modified_date: datetime,
) -> None:
    loaders.credentials.clear(
        CredentialsRequest(
            id=credential_id,
            organization_id=organization_id,
        )
    )
    credential = await loaders.credentials.load(
        CredentialsRequest(
            id=credential_id,
            organization_id=organization_id,
        )
    )
    if not credential:
        return

    if (
        not isinstance(secret, type(credential.state.secret))
        or credential.state.modified_date > modified_date
    ):
        return

    new_state = CredentialsState(
        modified_by=credential.state.modified_by,
        modified_date=modified_date,
        name=credential.state.name,
        secret=secret,
        is_pat=credential.state.is_pat,
        azure_organization=credential.state.azure_organization,
        type=credential.state.type,
    )
    await update_credential_state(
        current_value=credential.state,
        credential_id=credential.id,
        organization_id=credential.organization_id,
        state=new_state,
        force_update_owner=False,
    )
