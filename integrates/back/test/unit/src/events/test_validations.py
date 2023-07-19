from custom_exceptions import (
    InvalidParameter,
)
from db_model.events.enums import (
    EventType,
)
from events.validations import (
    validate_type,
    validate_type_deco,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


def test_validate_type() -> None:
    validate_type(event_type=EventType.CLONING_ISSUES)
    with pytest.raises(InvalidParameter):
        validate_type(event_type=EventType.INCORRECT_MISSING_SUPPLIES)


def test_validate_type_deco() -> None:
    @validate_type_deco(event_type_field="event_type")
    def decorated_func(event_type: EventType) -> EventType:
        return event_type

    assert decorated_func(event_type=EventType.CLONING_ISSUES)
    with pytest.raises(InvalidParameter):
        decorated_func(event_type=EventType.INCORRECT_MISSING_SUPPLIES)
