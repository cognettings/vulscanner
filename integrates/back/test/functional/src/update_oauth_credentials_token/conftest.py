# pylint: disable=import-error
from back.test import (
    db,
)
from custom_utils.datetime import (
    get_minus_delta,
    get_plus_delta,
    get_utc_now,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsState,
    OauthAzureSecret,
    OauthBitbucketSecret,
    OauthGitlabSecret,
)
from db_model.enums import (
    CredentialType,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("update_oauth_credentials_token")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    valid_until = get_plus_delta(
        get_minus_delta(get_utc_now(), seconds=60),
        seconds=int(3600),
    )
    data = {
        "credentials": [
            Credentials(
                id="b124134-22ca-4bca-96a8-448f80a6580f",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="unit test",
                state=CredentialsState(
                    modified_by="unitest@fluid.com",
                    modified_date=datetime(2022, 11, 21),
                    name="unittest",
                    type=CredentialType.OAUTH,
                    is_pat=False,
                    secret=OauthBitbucketSecret(
                        brefresh_token="refresh_token",
                        access_token="access_token",
                        valid_until=valid_until,
                    ),
                ),
            ),
            Credentials(
                id="b224134-22ca-4bca-96a8-448f80a6580f",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="unit test",
                state=CredentialsState(
                    modified_by="unitest@fluid.com",
                    modified_date=datetime(2022, 11, 21),
                    name="unittest",
                    type=CredentialType.OAUTH,
                    is_pat=False,
                    secret=OauthAzureSecret(
                        arefresh_token="refresh_token",
                        access_token="access_token",
                        redirect_uri="https://fluidattacks/home",
                        valid_until=valid_until,
                    ),
                ),
            ),
            Credentials(
                id="b324134-22ca-4bca-96a8-448f80a6580f",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="unit test",
                state=CredentialsState(
                    modified_by="unitest@fluid.com",
                    modified_date=datetime(2022, 11, 21),
                    name="unittest",
                    type=CredentialType.OAUTH,
                    is_pat=False,
                    secret=OauthGitlabSecret(
                        refresh_token="refresh_token",
                        access_token="access_token",
                        redirect_uri="https://fluidattacks/home",
                        valid_until=valid_until,
                    ),
                ),
            ),
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
