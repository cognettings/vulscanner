# type: ignore
# pylint: disable=invalid-name
"""
update user metadata

Start Time:        2023-06-20 at 13:37:14 UTC
Finalization Time: 2023-06-20 at 13:37:26 UTC
"""

from aioextensions import (
    collect,
    run,
)
from db_model.stakeholders import (
    get_all_stakeholders,
    update_metadata,
)
from db_model.stakeholders.types import (
    AccessTokens,
    Stakeholder,
    StakeholderMetadataToUpdate,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
import time
import uuid

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_user(user: Stakeholder, progress: float) -> None:
    if user.access_token and not user.access_tokens:
        await update_metadata(
            metadata=StakeholderMetadataToUpdate(
                access_tokens=[
                    AccessTokens(
                        id=str(uuid.uuid4()),
                        issued_at=user.access_token.iat,
                        jti_hashed=user.access_token.jti,
                        last_use=user.last_api_token_use_date,
                        salt=user.access_token.salt,
                    )
                ],
            ),
            email=user.email,
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
        "Start Time:        %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    LOGGER_CONSOLE.info("\n%s\n%s", execution_time, finalization_time)
