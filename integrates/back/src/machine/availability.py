from custom_utils.env import (
    guess_environment,
)
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from enum import (
    Enum,
)
import holidays
import json
import os


def _json_load(path: str) -> dict[str, dict[str, str]]:
    with open(path, encoding="utf-8") as file:
        return json.load(file)


QUEUES: dict[str, dict[str, str]] = _json_load(os.environ["MACHINE_QUEUES"])


class AvailabilityEnum(str, Enum):
    ALWAYS: str = "ALWAYS"
    WORKING_HOURS: str = "WORKING_HOURS"

    def is_available_right_now(self) -> bool:
        now: datetime = datetime.now(timezone(timedelta(hours=-5)))  # Colombia

        if (
            guess_environment() == "production"
            and self == AvailabilityEnum.WORKING_HOURS
        ):
            in_working_days = 0 <= now.weekday() <= 5  # Monday to Friday
            in_working_hours = 9 <= now.hour < 16  # [9:00, 15:59] Col
            is_holiday = now.strftime("%y-%m-%d") in holidays.CO()
            return in_working_days and in_working_hours and not is_holiday
        return True


def is_check_available(finding_code: str) -> bool:
    for data in QUEUES.values():
        if finding_code in data["findings"]:
            return AvailabilityEnum(
                data["availability"]
            ).is_available_right_now()

    raise NotImplementedError(f"{finding_code} does not belong to a queue")
