# pylint: disable=invalid-name
"""
Fix expiration_time variable in group_access data

Start Time:        2023-06-09 at 22:17:38 UTC
Finalization Time: 2023-06-09 at 22:18:23 UTC
"""
from aioextensions import (
    collect,
    run,
)
from custom_utils import (
    datetime as datetime_utils,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.group_access.types import (
    GroupAccessMetadataToUpdate,
    GroupAccessState,
)
from group_access import (
    domain as group_access_domain,
)
from group_access.domain import (
    get_group_stakeholders_emails,
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


async def get_stakeholder_incorrect_access(
    loaders: Dataloaders, group_name: str, stakeholder_email: str
) -> bool:
    stakeholder_access = await loaders.stakeholder_groups_access.load(
        stakeholder_email
    )
    return [
        bool(access.has_access) and bool(access.expiration_time)
        for access in stakeholder_access
        if access.group_name == group_name
    ][0]


async def get_group_stakeholders_to_fix(
    loaders: Dataloaders, group_name: str
) -> list[str]:
    active_stakeholders = await get_group_stakeholders_emails(
        loaders, group_name, active=True
    )
    inactive_stakeholders = await get_group_stakeholders_emails(
        loaders, group_name, active=False
    )
    stakeholder_emails = active_stakeholders + inactive_stakeholders
    stakeholders_incorrect_access = await collect(
        [
            get_stakeholder_incorrect_access(loaders, group_name, email)
            for email in stakeholder_emails
        ]
    )
    return [
        email
        for email, incorrect_access in zip(
            stakeholder_emails, stakeholders_incorrect_access
        )
        if incorrect_access
    ]


async def update_group_access(
    loaders: Dataloaders, group_name: str, email: str
) -> str:
    await group_access_domain.update(
        loaders=loaders,
        email=email,
        group_name=group_name,
        metadata=GroupAccessMetadataToUpdate(
            expiration_time=0,
            state=GroupAccessState(modified_date=datetime_utils.get_utc_now()),
        ),
    )
    return email


async def process_group(loaders: Dataloaders, group_name: str) -> None:
    stakeholders_to_fix = await get_group_stakeholders_to_fix(
        loaders, group_name
    )
    stakeholders_fixed = await collect(
        [
            update_group_access(loaders, group_name, stakeholder)
            for stakeholder in stakeholders_to_fix
        ]
    )
    LOGGER_CONSOLE.info(
        "Processed group %s",
        group_name,
        extra={
            "extra": {
                "stakeholders_to_fix": sorted(stakeholders_to_fix),
                "stakeholders_fixed": sorted(stakeholders_fixed),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    all_groups = await orgs_domain.get_all_active_groups(loaders)
    await collect([process_group(loaders, group.name) for group in all_groups])


if __name__ == "__main__":
    execution_time = time.strftime(
        "Start Time:        %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    LOGGER_CONSOLE.info("\n%s\n%s", execution_time, finalization_time)
