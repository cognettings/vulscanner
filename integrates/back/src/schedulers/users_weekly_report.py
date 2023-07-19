from context import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
)
from custom_utils import (
    datetime as datetime_utils,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from group_access import (
    domain as group_access_domain,
)
import logging
from mailer import (
    groups as groups_mail,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
INACTIVE_DAYS = 7


def get_inactive_users(
    group_stakeholders: tuple[dict[str, Any], ...],
) -> list[str]:
    inactive_users: list[str] = [
        stakeholder["email"]
        for stakeholder in group_stakeholders
        if (
            stakeholder["last_login"]
            and (
                datetime_utils.get_utc_now()
                - datetime.fromisoformat(stakeholder["last_login"])
            ).days
            >= INACTIVE_DAYS
        )
    ]
    return inactive_users


async def send_users_weekly_report() -> None:
    loaders: Dataloaders = get_new_context()

    group_names = await orgs_domain.get_all_active_group_names(loaders)

    if FI_ENVIRONMENT == "production":
        group_names = [
            group_name
            for group_name in group_names
            if group_name not in FI_TEST_PROJECTS.split(",")
        ]

    users: dict[str, list[str]] = {}

    for group_name in group_names:
        group_stakeholders = await group_access_domain.get_group_stakeholders(
            loaders, group_name
        )
        for stakeholder in group_stakeholders:
            stakeholder_role = await group_access_domain.get_stakeholder_role(
                loaders,
                stakeholder.email,
                group_name,
                stakeholder.is_registered,
            )
            if stakeholder_role in ["customer_manager", "user_manager"]:
                if users.get(stakeholder.email):
                    users[stakeholder.email].append(group_name)
                else:
                    users[stakeholder.email] = [group_name]

    if users:
        email_context: dict[str, Any] = {}
        await groups_mail.send_mail_users_weekly_report(
            loaders=loaders,
            email_to=[],
            context=email_context,
        )
    else:
        LOGGER.info("- users weekly report NOT sent")


async def main() -> None:
    await send_users_weekly_report()
