from app.app import (
    APP,
)
from datetime import (
    datetime,
)
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessState,
    GroupInvitation,
)
from db_model.organization_access.types import (
    OrganizationAccess,
    OrganizationInvitation,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationState,
)
from db_model.types import (
    Policies,
)
from httpx import (
    AsyncClient,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    Dict,
)

MOCK_DATA: Dict[str, Dict[str, Dict[str, Any]]] = {
    "app.app.": {
        "test_confirm_access": {
            "mock_get_access_by_url_token": GroupAccess(
                email="testing@fluidattacks.com",
                group_name="group",
                state=GroupAccessState(
                    datetime.fromisoformat("2020-09-12T13:45:48+00:00")
                ),
            ),
        },
        "test_confirm_access_organization": {
            "mock_get_access_by_url_token": OrganizationAccess(
                organization_id="tes@134145f95onf9i",
                email="testing@fluidattacks.com",
                expiration_time=None,
                has_access=True,
                invitation=OrganizationInvitation(
                    is_used=False, role="user", url_token="test_token"
                ),
                role="user",
            ),
            "mock_get_organization": Organization(
                name="unit_testing",
                created_by="testing_team",
                created_date=datetime.fromisoformat(
                    "2020-09-12T13:45:48+00:00"
                ),
                id="tes@134145f95onf9i",
                policies=Policies(
                    modified_date=datetime.fromisoformat(
                        "2020-09-12T13:45:48+00:00"
                    ),
                    modified_by="testing_team",
                    inactivity_period=0,
                    max_acceptance_days=100,
                    max_number_acceptances=6,
                ),
                state=OrganizationState(
                    status=OrganizationStateStatus.ACTIVE,
                    modified_by="testing_team",
                    modified_date=datetime.fromisoformat(
                        "2020-09-12T13:45:48+00:00"
                    ),
                ),
                country="Colombia",
            ),
        },
        "test_reject_access": {
            "mock_group_access_domain_get_access_by_url_token": GroupAccess(
                email="testing@fluidattacks.com",
                group_name="testing",
                state=GroupAccessState(
                    modified_date=datetime.fromisoformat(
                        "2020-09-12T13:45:48+00:00"
                    )
                ),
                invitation=GroupInvitation(
                    is_used=False,
                    role="user",
                    url_token="test_token",
                ),
            )
        },
    }
}


@pytest.fixture
def mock_data_for_module() -> Callable[[str, str, str], Any]:
    def _mock_data_for_module(
        test_name: str,
        mock_name: str,
        module_at_test: str,
    ) -> Any:
        return MOCK_DATA[module_at_test][test_name][mock_name]

    return _mock_data_for_module


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=APP, base_url="http://testserver") as _client:
        yield _client
