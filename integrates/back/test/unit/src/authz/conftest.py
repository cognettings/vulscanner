from authz import (
    get_group_level_actions_by_role,
    get_organization_level_actions_by_role,
    get_user_level_actions_by_role,
)
from collections.abc import (
    Callable,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessState,
)
from db_model.organization_access.types import (
    OrganizationAccess,
)
from db_model.stakeholders.types import (
    NotificationsParameters,
    NotificationsPreferences,
    Stakeholder,
    StakeholderPhone,
    StakeholderSessionToken,
    StakeholderState,
    StakeholderTours,
    StateSessionType,
)
from decimal import (
    Decimal,
)
import pytest
from typing import (
    Any,
)

pytestmark = [
    pytest.mark.asyncio,
]


MOCK_GROUP_ACCESS = {
    "continuoushacking@gmail.com": [
        GroupAccess(
            email="continuoushacking@gmail.com",
            group_name="oneshottest",
            state=GroupAccessState(modified_date=None),
            confirm_deletion=None,
            expiration_time=None,
            has_access=True,
            invitation=None,
            responsibility=None,
            role="user_manager",
        ),
        GroupAccess(
            email="continuoushacking@gmail.com",
            group_name="unittesting",
            state=GroupAccessState(modified_date=None),
            confirm_deletion=None,
            expiration_time=None,
            has_access=True,
            invitation=None,
            responsibility=None,
            role="user_manager",
        ),
    ],
    "integrateshacker@fluidattacks.com": [
        GroupAccess(
            email="integrateshacker@fluidattacks.com",
            group_name="oneshottest",
            state=GroupAccessState(modified_date=None),
            confirm_deletion=None,
            expiration_time=None,
            has_access=True,
            invitation=None,
            responsibility=None,
            role="reattacker",
        ),
        GroupAccess(
            email="integrateshacker@fluidattacks.com",
            group_name="unittesting",
            state=GroupAccessState(modified_date=None),
            confirm_deletion=None,
            expiration_time=None,
            has_access=True,
            invitation=None,
            responsibility=None,
            role="hacker",
        ),
    ],
    "integratesuser@gmail.com": [
        GroupAccess(
            email="integratesuser@gmail.com",
            group_name="oneshottest",
            state=GroupAccessState(modified_date=None),
            confirm_deletion=None,
            expiration_time=None,
            has_access=True,
            invitation=None,
            responsibility=None,
            role="user",
        ),
        GroupAccess(
            email="integratesuser@gmail.com",
            group_name="unittesting",
            state=GroupAccessState(modified_date=None),
            confirm_deletion=None,
            expiration_time=None,
            has_access=True,
            invitation=None,
            responsibility=None,
            role="user_manager",
        ),
    ],
    "unittest@fluidattacks.com": [
        GroupAccess(
            email="unittest@fluidattacks.com",
            group_name="unittesting",
            state=GroupAccessState(
                modified_date=datetime.fromisoformat(
                    "2020-01-01T20:07:57+00:00"
                )
            ),
            confirm_deletion=None,
            expiration_time=None,
            has_access=True,
            invitation=None,
            responsibility="Tester",
            role=None,
        )
    ],
}

MOCK_ORGANIZATION_ACCESS = {
    "org_testgroupmanager1@gmail.com": [
        OrganizationAccess(
            organization_id="ORG#f2e2777d-a168-4bea-93cd-d79142b294d2",
            email="org_testgroupmanager1@gmail.com",
            expiration_time=None,
            has_access=None,
            invitation=None,
            role="customer_manager",
        )
    ],
    "unittest2@fluidattacks.com": [
        OrganizationAccess(
            organization_id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            email="unittest2@fluidattacks.com",
            expiration_time=None,
            has_access=None,
            invitation=None,
            role="customer_manager",
        )
    ],
}

MOCK_USERS_ROLES: dict[str, str] = {
    "continuoushacking@gmail.com": "hacker",
    "integrateshacker@fluidattacks.com": "hacker",
    "integratesuser@gmail.com": "user",
    "integratesuser2@gmail.com": "user",
    "org_testgroupmanager1@gmail.com": "",
    "unittest@fluidattacks.com": "admin",
    "unittest2@fluidattacks.com": "hacker",
}

MOCKED_DATA: dict[str, dict[str, Any]] = {
    "authz.enforcer.Dataloaders.stakeholder_organizations_access": {
        '["integrates@fluidattacks.com"]': [
            OrganizationAccess(
                organization_id="ORG#f2e2777d-a168-4bea-93cd-d79142b294d2",
                email="integrates@fluidattacks.com",
                expiration_time=None,
                has_access=None,
                invitation=None,
                role="admin",
            )
        ],
        '["integratesuser@gmail.com"]': [
            OrganizationAccess(
                organization_id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                email="integratesuser@gmail.com",
                expiration_time=None,
                has_access=None,
                invitation=None,
                role="user_manager",
            )
        ],
        '["unittesting@fluidattacks.com"]': [
            OrganizationAccess(
                organization_id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                email="unittesting@fluidattacks.com",
                expiration_time=None,
                has_access=None,
                invitation=None,
                role="user",
            )
        ],
        '["unittesting@gmail.com"]': [
            OrganizationAccess(
                organization_id="ORG#f2e2777d-a168-4bea-93cd-d79142b294d2",
                email="unittesting@gmail.com",
                expiration_time=None,
                has_access=None,
                invitation=None,
                role="admin",
            )
        ],
    },
    "authz.enforcer.get_user_level_role": {
        '["integrates@fluidattacks.com"]': "admin",
        '["integratesuser@gmail.com"]': "user",
        '["unittesting@fluidattacks.com"]': "user",
        '["unittesting@gmail.com"]': "admin",
    },
    "authz.policy.Dataloaders.stakeholder": {
        '["integrateshacker@fluidattacks.com"]': Stakeholder(
            email="integrateshacker@fluidattacks.com",
            enrolled=True,
            first_name="Integrates",
            is_concurrent_session=False,
            is_registered=True,
            last_login_date=datetime.fromisoformat(
                "2020-12-31T18:40:37+00:00"
            ),
            last_name="Hacker",
            legal_remember=False,
            phone=StakeholderPhone(
                country_code="CO",
                calling_country_code="57",
                national_number="1234567895",
            ),
            registration_date=datetime.fromisoformat(
                "2018-02-28T16:54:12+00:00"
            ),
            role="hacker",
            session_key=None,
            session_token=None,
            state=StakeholderState(
                modified_by=None,
                modified_date=None,
                notifications_preferences=NotificationsPreferences(
                    available=[],
                    email=[],
                    sms=[],
                    parameters=NotificationsParameters(
                        min_severity=Decimal("3.0")
                    ),
                ),
            ),
            tours=StakeholderTours(
                new_group=False,
                new_root=False,
                new_risk_exposure=False,
                welcome=False,
            ),
        ),
        '["integratesuser@gmail.com"]': Stakeholder(
            email="integratesuser@gmail.com",
            enrolled=True,
            first_name="Integrates",
            is_concurrent_session=False,
            is_registered=True,
            last_login_date=datetime.fromisoformat(
                "2020-12-31T18:40:37+00:00"
            ),
            last_name="User",
            legal_remember=True,
            phone=None,
            registration_date=datetime.fromisoformat(
                "2018-02-28T16:54:12+00:00"
            ),
            role="user",
            session_key=None,
            session_token=StakeholderSessionToken(
                jti="0f98c8",
                state=StateSessionType.IS_VALID,
            ),
            state=StakeholderState(
                modified_by="integratesuser@gmail.com",
                modified_date=datetime.fromisoformat(
                    "2018-02-28T16:54:12+00:00"
                ),
                notifications_preferences=NotificationsPreferences(
                    available=[],
                    email=[
                        "ACCESS_GRANTED",
                        "AGENT_TOKEN",
                        "EVENT_REPORT",
                        "FILE_UPDATE",
                        "GROUP_INFORMATION",
                        "GROUP_REPORT",
                        "NEW_COMMENT",
                        "NEW_DRAFT",
                        "PORTFOLIO_UPDATE",
                        "REMEDIATE_FINDING",
                        "REMINDER_NOTIFICATION",
                        "ROOT_UPDATE",
                        "SERVICE_UPDATE",
                        "UNSUBSCRIPTION_ALERT",
                        "UPDATED_TREATMENT",
                        "VULNERABILITY_ASSIGNED",
                        "VULNERABILITY_REPORT",
                    ],
                    sms=[],
                    parameters=NotificationsParameters(
                        min_severity=Decimal("3.0")
                    ),
                ),
            ),
            tours=StakeholderTours(
                new_group=False,
                new_root=False,
                new_risk_exposure=False,
                welcome=False,
            ),
        ),
    },
    "authz.policy.stakeholders_model.update_metadata": {
        '["integrateshacker@fluidattacks.com"]': None,
        '["integratesuser@gmail.com"]': None,
    },
}


def _mock_get_user_level_role(email: str) -> str:
    user_role: str = ""
    if MOCK_USERS_ROLES[email]:
        user_role = MOCK_USERS_ROLES[email]

    return user_role


def _mock_loaders_stakeholder_groups_access_load(
    email: str,
) -> list[GroupAccess]:
    group_access: list[GroupAccess]
    if MOCK_GROUP_ACCESS[email]:
        group_access = MOCK_GROUP_ACCESS[email]

    return group_access


@pytest.fixture
def mocked_data_for_module(
    *,
    resolve_mock_data: Callable,
) -> Any:
    def _mocked_data_for_module(
        mock_path: str, mock_args: list[Any], module_at_test: str
    ) -> Callable[[str, list[Any], str], Any]:
        return resolve_mock_data(
            mock_data=MOCKED_DATA,
            mock_path=mock_path,
            mock_args=mock_args,
            module_at_test=module_at_test,
        )

    return _mocked_data_for_module


def mock_loaders_stakeholder_organizations_access_load(
    email: str,
) -> list[OrganizationAccess]:
    organization_access: list[OrganizationAccess]
    if MOCK_ORGANIZATION_ACCESS[email]:
        organization_access = MOCK_ORGANIZATION_ACCESS[email]

    return organization_access


@pytest.fixture
def side_effect_get_group_level_enforcer() -> (
    Callable[[Dataloaders, str], Callable[[str, str], bool]]
):
    def _mock_get_group_level_enforcer(
        loaders: Dataloaders,
        email: str,
    ) -> Callable[[str, str], bool]:
        """Return a filtered group-level authorization
        for the provided email."""
        if loaders and email:
            groups_access = _mock_loaders_stakeholder_groups_access_load(email)
            user_level_role = _mock_get_user_level_role(email)

        def enforcer(group_name_to_test: str, action: str) -> bool:
            return any(
                # Regular user with a group policy set for the r_object
                group_name_to_test == access.group_name
                and access.role
                and action in get_group_level_actions_by_role(access.role)
                for access in groups_access
            ) or (
                # An admin
                user_level_role == "admin"
                and action in get_group_level_actions_by_role("admin")
            )

        return enforcer

    return _mock_get_group_level_enforcer


@pytest.fixture
def side_effect_get_organization_level_enforcer() -> (
    Callable[[Dataloaders, str], Callable[[str, str], bool]]
):
    def _mock_side_effect_get_organization_level_enforcer(
        loaders: Dataloaders,
        email: str,
    ) -> Callable[[str, str], bool]:
        """
        Return a filtered organization-level authorization
        for the provided email.
        """
        if loaders and email:
            orgs_access = mock_loaders_stakeholder_organizations_access_load(
                email
            )
            user_level_role = _mock_get_user_level_role(email)

        def enforcer(organization_id_to_test: str, action: str) -> bool:
            return any(
                # Regular user with an organization policy set for the r_object
                organization_id_to_test == access.organization_id
                and access.role
                and action
                in get_organization_level_actions_by_role(access.role)
                for access in orgs_access
            ) or (
                # An admin
                user_level_role == "admin"
                and action in get_organization_level_actions_by_role("admin")
            )

        return enforcer

    return _mock_side_effect_get_organization_level_enforcer


@pytest.fixture
def side_effect_get_user_level_enforcer() -> (
    Callable[[Dataloaders, str], Callable[[str], bool]]
):
    def _mock_get_user_level_enforcer(
        loaders: Dataloaders,
        email: str,
    ) -> Callable[[str], bool]:
        """Return a filtered group-level authorization
        for the provided email."""
        if loaders and email:
            user_level_role = _mock_get_user_level_role(email)

        def enforcer(action: str) -> bool:
            return bool(
                user_level_role
                and action in get_user_level_actions_by_role(user_level_role)
            )

        return enforcer

    return _mock_get_user_level_enforcer
