# pylint: disable=invalid-name
"""
Remove charts_report notification preferences from stakeholders

Execution Time:    2023-04-04 at 02:56:35 UTC
Finalization Time: 2023-04-04 at 02:57:16 UTC
Execution Time:    2023-04-04 at 04:51:36 UTC
Finalization Time: 2023-04-04 at 04:52:36 UTC

"""

from aioextensions import (
    collect,
    run,
)
from db_model import (
    stakeholders as stakeholders_model,
)
from db_model.stakeholders.types import (
    NotificationsPreferences,
    Stakeholder,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from stakeholders.domain import (
    update_notification_preferences,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_user(user: Stakeholder, progress: float) -> None:
    preference_to_rm = {"CHARTS_REPORT"}

    if any(
        item in user.state.notifications_preferences.email
        for item in preference_to_rm
    ):
        new_preferences = [
            item
            for item in user.state.notifications_preferences.email
            if item not in preference_to_rm
        ]
        await update_notification_preferences(
            email=user.email,
            preferences=NotificationsPreferences(
                sms=user.state.notifications_preferences.email,
                email=new_preferences,
                parameters=user.state.notifications_preferences.parameters,
                available=user.state.notifications_preferences.available,
            ),
        )
        LOGGER_CONSOLE.info(
            "User processed",
            extra={
                "extra": {
                    "user email": user.email,
                    "progress": round(progress, 2),
                }
            },
        )


async def main() -> None:
    all_stakeholders = await stakeholders_model.get_all_stakeholders()

    await collect(
        tuple(
            process_user(
                user=stakeholder, progress=count / len(all_stakeholders)
            )
            for count, stakeholder in enumerate(all_stakeholders)
        ),
        workers=16,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
