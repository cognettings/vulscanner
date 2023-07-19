from aioextensions import (
    collect,
)
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
from db_model.enums import (
    Notification,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from db_model.trials.types import (
    Trial,
)
from groups.domain import (
    get_group,
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

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
INACTIVE_DAYS = 21


async def is_trial_end(loaders: Dataloaders, email: str) -> bool:
    trial: Trial | None = await loaders.trial.load(email)
    return trial.completed if trial else False


async def send_reminder_notification() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = await orgs_domain.get_all_active_group_names(loaders)

    if FI_ENVIRONMENT == "production":
        group_names = [
            group_name
            for group_name in group_names
            if group_name not in FI_TEST_PROJECTS.split(",")
        ]

    groups = await collect(
        [get_group(loaders, group_name) for group_name in group_names]
    )
    orgs_ids: set[str] = set(group.organization_id for group in groups)

    inactive_stakeholders: list[Stakeholder] = [
        stakeholder
        for org_id in orgs_ids
        for stakeholder in await orgs_domain.get_stakeholders(loaders, org_id)
        if stakeholder
        and (
            stakeholder.last_login_date
            and (
                datetime_utils.get_utc_now() - stakeholder.last_login_date
            ).days
            == INACTIVE_DAYS
            and await orgs_domain.get_stakeholder_role(
                loaders=loaders,
                email=stakeholder.email,
                is_registered=stakeholder.is_registered,
                organization_id=org_id,
            )
            in ["customer_manager", "user_manager"]
        )
    ]

    inactive_stakeholders_email = {
        stakeholder.email
        for stakeholder in inactive_stakeholders
        if Notification.REMINDER_NOTIFICATION
        in stakeholder.state.notifications_preferences.email
        and await is_trial_end(loaders, stakeholder.email)
    }

    if inactive_stakeholders_email:
        await groups_mail.send_mail_reminder(
            loaders=loaders,
            context={},
            email_to=list(inactive_stakeholders_email),
        )
    else:
        LOGGER.info("- reminder notification NOT sent")


async def main() -> None:
    await send_reminder_notification()
