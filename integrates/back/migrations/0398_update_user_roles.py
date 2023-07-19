# type: ignore

# pylint: disable=invalid-name
"""
update user roles

Execution Time:    -
Finalization Time: -
"""

from aioextensions import (
    collect,
    run,
)
from db_model.stakeholders import (
    get_all_stakeholders,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderMetadataToUpdate,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from stakeholders import (
    domain as stakeholders_domain,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")

roles_to_update = [
    "user",
]


async def process_user(user: Stakeholder, progress: float) -> None:
    if (
        user.email.endswith("@fluidattacks.com")
        and user.role in roles_to_update
    ):
        await stakeholders_domain.update(
            email=user.email,
            metadata=StakeholderMetadataToUpdate(
                role="hacker",
            ),
        )

        LOGGER_CONSOLE.info(
            "User updated",
            extra={
                "extra": {
                    "user email": user.email,
                    "progress": round(progress, 2),
                }
            },
        )


async def main() -> None:
    all_stakeholders = await get_all_stakeholders()
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
