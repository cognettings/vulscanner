from context import (
    FI_TEST_ORGS,
    FI_TEST_PROJECTS,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import logging
import logging.config
from organizations.domain import (
    iterate_organizations_and_groups,
)
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def send_numerator_report() -> None:
    loaders: Dataloaders = get_new_context()
    test_groups = FI_TEST_PROJECTS.split(",")
    orgs_groups = []
    async for _, org_name, org_groups in iterate_organizations_and_groups(
        loaders
    ):
        if org_name not in FI_TEST_ORGS.lower().split(","):
            orgs_groups.append(org_groups)

    groups = [
        group_name
        for group_list in orgs_groups
        for group_name in group_list
        if group_name not in test_groups
    ]

    LOGGER.info("info", extra={"extra": {"info": groups}})


async def main() -> None:
    await send_numerator_report()
