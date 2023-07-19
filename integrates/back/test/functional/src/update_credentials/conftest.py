# pylint: disable=import-error
from back.test import (
    db,
)
from custom_utils.datetime import (
    get_now_plus_delta,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsState,
    HttpsPatSecret,
    HttpsSecret,
    OauthGitlabSecret,
    SshSecret,
)
from db_model.enums import (
    CredentialType,
    GitCloningStatus,
)
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
)
import os
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("update_credentials")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data = {
        "credentials": (
            Credentials(
                id="261bf518-f8f4-4f82-b996-3d034df44a27",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="user_manager@fluidattacks.com",
                state=CredentialsState(
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-11 11:32:15+00:00"
                    ),
                    name="Ssh key",
                    type=CredentialType.SSH,
                    secret=SshSecret(key=os.environ["TEST_SSH_KEY"]),
                    is_pat=False,
                ),
            ),
            Credentials(
                id="9edc56a8-2743-437e-a6a9-4847b28e1fd5",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="user@gmail.com",
                state=CredentialsState(
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-11 11:32:15+00:00"
                    ),
                    name="Token",
                    type=CredentialType.HTTPS,
                    secret=HttpsPatSecret(token="token test"),
                    is_pat=False,
                ),
            ),
            Credentials(
                id="1a5dacda-1d52-465c-9158-f6fd5dfe0998",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="admin@gmail.com",
                state=CredentialsState(
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-12T14:58:10+00:00"
                    ),
                    name="oauth lab token",
                    type=CredentialType.OAUTH,
                    secret=OauthGitlabSecret(
                        refresh_token="UFUzdCBTU0gK",
                        redirect_uri="",
                        access_token="TETzdCBTU0gK",
                        valid_until=get_now_plus_delta(hours=2),
                    ),
                    is_pat=False,
                ),
            ),
            Credentials(
                id="42143c0c-a12c-4774-9d02-285b94e698e4",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="user@gmail.com",
                state=CredentialsState(
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-11 11:32:15+00:00"
                    ),
                    name="User and password",
                    type=CredentialType.HTTPS,
                    secret=HttpsSecret(
                        user="user test", password="password test"
                    ),
                    is_pat=False,
                ),
            ),
        ),
        "roots": [
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-11 11:32:15+00:00"
                        ),
                        reason="Repo added",
                        status=GitCloningStatus.UNKNOWN,
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-02-11 11:32:15+00:00"
                    ),
                    group_name="group1",
                    id="e22a3a0d-05ac-4d13-8c81-7c829f8f96e3",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        credential_id="261bf518-f8f4-4f82-b996-3d034df44a27",
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-11 11:32:15+00:00"
                        ),
                        nickname="nickname1",
                        other=None,
                        reason=None,
                        status=RootStatus.ACTIVE,
                        url="git@gitlab.com:fluidattacks/universe.git",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-11 11:32:15+00:00"
                        ),
                        reason="Repo added",
                        status=GitCloningStatus.UNKNOWN,
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-02-11 11:32:15+00:00"
                    ),
                    group_name="group1",
                    id="888648ed-a71c-42e5-b3e5-c3a370d26c68",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        credential_id="9edc56a8-2743-437e-a6a9-4847b28e1fd5",
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-11 11:32:15+00:00"
                        ),
                        nickname="nickname2",
                        other=None,
                        reason=None,
                        status=RootStatus.ACTIVE,
                        url="git@gitlab.com:fluidattacks/universe_2.git",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-11 11:32:15+00:00"
                        ),
                        reason="Repo added",
                        status=GitCloningStatus.UNKNOWN,
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-02-11 11:32:15+00:00"
                    ),
                    group_name="group1",
                    id="3626aca5-099c-42b9-aa25-d8c6e0aab98f",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-11 11:32:15+00:00"
                        ),
                        nickname="nickname3",
                        other=None,
                        reason=None,
                        status=RootStatus.ACTIVE,
                        url="git@gitlab.com:fluidattacks/universe.git",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-11 11:32:15+00:00"
                        ),
                        reason="Repo added",
                        status=GitCloningStatus.UNKNOWN,
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-02-11 11:32:15+00:00"
                    ),
                    group_name="group1",
                    id="58167a02-08c2-4cdf-a5e4-568398cbe7cb",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-11 11:32:15+00:00"
                        ),
                        nickname="nickname4",
                        other=None,
                        reason=None,
                        status=RootStatus.INACTIVE,
                        url="git@gitlab.com:fluidattacks/universe.git",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-11 11:32:15+00:00"
                        ),
                        reason="Repo added",
                        status=GitCloningStatus.UNKNOWN,
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-02-11 11:32:15+00:00"
                    ),
                    group_name="group1",
                    id="c75f9c2c-1984-49cf-bd3f-c628175a569c",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        credential_id="9edc56a8-2743-437e-a6a9-4847b28e1fd5",
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-11 11:32:15+00:00"
                        ),
                        nickname="nickname5",
                        other=None,
                        reason=None,
                        status=RootStatus.ACTIVE,
                        url="git@gitlab.com:fluidattacks/universe.git",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
