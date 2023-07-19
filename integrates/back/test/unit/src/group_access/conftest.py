from collections.abc import (
    Callable,
)
import pytest
from typing import (
    Any,
)

pytestmark = [
    pytest.mark.asyncio,
]


MOCK_DATA = {
    "group_access.domain.authz.get_group_level_role": {
        '["unittesting"]': [
            "user_manager",
            "user_manager",
            "customer_manager",
            "service_forces",
            "hacker",
            "admin",
            "admin",
            "reattacker",
            "resourcer",
            "reviewer",
            "service_forces",
            "user",
            "user",
            "user_manager",
            "customer_manager",
            "admin",
            "vulnerability_manager",
        ],
    },
    "group_access.domain.get_group_stakeholders_emails": {
        '["unittesting"]': [
            "continuoushack2@gmail.com",
            "continuoushacking@gmail.com",
            "customer_manager@fluidattacks.com",
            "forces.unittesting@fluidattacks.com",
            "integrateshacker@fluidattacks.com",
            "integratesmanager@fluidattacks.com",
            "integratesmanager@gmail.com",
            "integratesreattacker@fluidattacks.com",
            "integratesresourcer@fluidattacks.com",
            "integratesreviewer@fluidattacks.com",
            "integratesserviceforces@fluidattacks.com",
            "integratesuser2@fluidattacks.com",
            "integratesuser2@gmail.com",
            "integratesuser@gmail.com",
            "unittest2@fluidattacks.com",
            "unittest@fluidattacks.com",
            "vulnmanager@gmail.com",
        ]
    },
}


@pytest.fixture
def mock_data_for_module(
    *,
    resolve_mock_data: Any,
) -> Any:
    def _mock_data_for_module(
        mock_path: str, mock_args: list[Any], module_at_test: str
    ) -> Callable[[str, list[Any], str], Any]:
        return resolve_mock_data(
            mock_data=MOCK_DATA,
            mock_path=mock_path,
            mock_args=mock_args,
            module_at_test=module_at_test,
        )

    return _mock_data_for_module
