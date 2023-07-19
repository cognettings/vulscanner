from collections.abc import (
    Callable,
)
from datetime import (
    datetime,
)
from db_model.events.enums import (
    EventStateStatus,
    EventType,
)
from db_model.events.types import (
    Event,
    EventEvidences,
    EventState,
    EventUnreliableIndicators,
)
import pytest
from typing import (
    Any,
)

pytestmark = [
    pytest.mark.asyncio,
]


MOCKED_DATA: dict[str, dict[str, Any]] = {
    "events.domain.event_comments_domain.add": {
        '[["538745942", "1672323259183", "0", '
        '"2022-12-29 14:14:19.182591+00:00", "comment test", '
        '"integratesmanager@gmail.com", "group1", "John Doe"]]': None,
    },
    "events.domain.get_event": {
        '["538745942"]': Event(
            client="test",
            created_by="unittest@fluidattacks.com",
            created_date=datetime.fromisoformat("2019-09-19T15:43:43+00:00"),
            description="Esta eventualidad fue levantada para poder realizar "
            "pruebas de unittesting",
            event_date=datetime.fromisoformat("2019-09-19T13:09:00+00:00"),
            evidences=EventEvidences(
                file_1=None,
                image_1=None,
                image_2=None,
                image_3=None,
                image_4=None,
                image_5=None,
                image_6=None,
            ),
            group_name="unittesting",
            hacker="unittest@fluidattacks.com",
            id="538745942",
            state=EventState(
                modified_by="unittest@fluidattacks.com",
                modified_date=datetime.fromisoformat(
                    "2019-09-19T15:43:43+00:00"
                ),
                status=EventStateStatus.CREATED,
                comment_id=None,
                other=None,
                reason=None,
            ),
            type=EventType.AUTHORIZATION_SPECIAL_ATTACK,
            root_id=None,
            unreliable_indicators=EventUnreliableIndicators(
                unreliable_solving_date=None
            ),
        ),
    },
    "events.domain._check_invalid_comment": {
        '["comment test", "integratesmanager@gmail.com", "0", '
        '"538745942"]': None
    },
}


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
