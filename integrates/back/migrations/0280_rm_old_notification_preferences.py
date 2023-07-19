# pylint: disable=invalid-name
"""
Remove old notification preferences from stakeholders
https://gitlab.com/fluidattacks/universe/-/issues/7520

Execution Time:    2022-09-27 at 20:07:35 UTC
Finalization Time: 2022-09-27 at 20:08:17 UTC
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
    rm_preferences = ["DAILY_DIGEST", "ROOT_MOVED", "FILE_UPLOADED"]
    if any(
        item in user.state.notifications_preferences.email
        for item in rm_preferences
    ):
        new_preferences = [
            item
            for item in user.state.notifications_preferences.email
            if item not in rm_preferences
        ]
        await update_notification_preferences(
            email=user.email,
            preferences=NotificationsPreferences(email=new_preferences),
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
    LOGGER_CONSOLE.info(
        "Active users",
        extra={"extra": {"users_len": len(all_stakeholders)}},
    )
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
