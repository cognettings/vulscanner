# pylint: disable=invalid-name,import-error
# type: ignore
"""
Remove stakeholders subscriptions

Execution Time:    2023-04-11 at 03:42:39 UTC
Finalization Time: 2023-04-11 at 03:43:18 UTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    stakeholders as stakeholders_model,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from db_model.subscriptions.remove import (
    remove,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_user(
    user: Stakeholder, loaders: Dataloaders, progress: float
) -> None:
    subscriptions = await loaders.stakeholder_subscriptions.load(user.email)
    await collect(
        tuple(
            remove(
                entity=subscription.entity,
                subject=subscription.subject,
                email=user.email,
            )
            for subscription in subscriptions
        ),
        workers=8,
    )
    LOGGER_CONSOLE.info(
        "User processed",
        extra={
            "extra": {
                "user email": user.email,
                "progress": round(progress, 2),
                "subscriptions": subscriptions,
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    all_stakeholders = await stakeholders_model.get_all_stakeholders()

    await collect(
        tuple(
            process_user(
                user=stakeholder,
                loaders=loaders,
                progress=count / len(all_stakeholders),
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
