from ..types import (
    MESSAGE_SCHEMA,
)
from contextlib import (
    suppress,
)
from jsonschema import (
    validate,
)
from jsonschema.exceptions import (
    ValidationError,
)

TASK_NAME_PREFIX = "task_queue"


class FailedValidation(Exception):
    pass


def validate_message(message: dict[str, object]) -> bool:
    with suppress(ValidationError):
        validate(message, MESSAGE_SCHEMA)
        return True
    return False


def inverse_proportional_distribution(
    amount: int, priorities: list[int]
) -> list[float]:
    inv_priorities = [1 / p for p in priorities]
    total_inv_priority = sum(inv_priorities)
    inv_proportions = [inv_p / total_inv_priority for inv_p in inv_priorities]
    amounts = [amount * p for p in inv_proportions]
    total_amounts = sum(amounts)
    amounts = [
        int(round(a + (amount - total_amounts) / len(amounts)))
        for a in amounts
    ]
    return amounts
