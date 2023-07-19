from collections.abc import (
    Callable,
)
from datetime import (
    datetime,
)
from db_model.stakeholders.types import (
    NotificationsParameters,
    NotificationsPreferences,
    Stakeholder,
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

MOCKED_DATA: dict[str, dict[str, Any]] = {
    "notifications.domain.Dataloaders.stakeholder": {
        '["forces.unittesting@fluidattacks.com"]': Stakeholder(
            email="forces.unittesting@fluidattacks.com",
            enrolled=True,
            first_name="",
            is_concurrent_session=False,
            is_registered=True,
            last_login_date=None,
            last_name="",
            legal_remember=True,
            phone=None,
            registration_date=None,
            role="user",
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
                jti="0f98c", state=StateSessionType.IS_VALID
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
    }
}


@pytest.fixture
def mock_data_for_module(
    *,
    resolve_mock_data: Callable,
) -> Any:
    def _mock_data_for_module(
        mock_path: str, mock_args: list[Any], module_at_test: str
    ) -> Callable[[str, list[Any], str], Any]:
        return resolve_mock_data(
            mock_data=MOCKED_DATA,
            mock_path=mock_path,
            mock_args=mock_args,
            module_at_test=module_at_test,
        )

    return _mock_data_for_module
