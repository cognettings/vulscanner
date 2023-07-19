# pylint: disable=invalid-name
"""
Migrate an undisclosed email from user to user_manager at the org level.

Start Time:        2023-06-09 at 18:35:22 UTC
Finalization Time: 2023-06-09 at 18:35:30 UTC
"""
from aioextensions import (
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    email = "undisclosed@fluidattacks.com"
    orgs_access = await loaders.stakeholder_organizations_access.load(email)
    print(f"{len(orgs_access)=}")

    for access in orgs_access:
        if access.role != "user":
            continue

        await orgs_domain.update_stakeholder_role(
            loaders=loaders,
            user_email=email,
            organization_id=access.organization_id,
            organization_access=access,
            new_role="user_manager",
        )
        print(f"Updated {access.organization_id} from_role={access.role}")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Start Time:        %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    LOGGER_CONSOLE.info("\n%s\n%s", execution_time, finalization_time)
