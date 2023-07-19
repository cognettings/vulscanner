from aioextensions import (
    collect,
)
from collections.abc import (
    Awaitable,
    Callable,
)
from custom_exceptions import (
    UnableToSendMail,
)
from custom_utils import (
    datetime as datetime_utils,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from decorators import (
    retry_on_exceptions,
)
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from mailer import (
    trial as trial_mail,
)
from mailer.types import (
    TrialEngagementInfo,
)
from organizations import (
    domain as orgs_domain,
)

mail_add_members_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(trial_mail.send_add_members_notification)

mail_send_define_treatments_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(trial_mail.send_define_treatments_notification)

mail_send_add_repositories_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(trial_mail.send_add_repositories_notification)

mail_support_channels_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(trial_mail.send_support_channels_notification)

mail_devsecops_agent_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(trial_mail.send_devsecops_agent_notification)

mail_trial_reports_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(trial_mail.send_trial_reports_notification)

mail_upgrade_squad_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(trial_mail.send_upgrade_squad_notification)

mail_trial_ending_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(trial_mail.send_trial_ending_notification)

mail_how_improve_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(trial_mail.send_how_improve_notification)

mail_trial_ended_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(trial_mail.send_trial_ended_notification)


async def send_trial_engagement_notification() -> None:
    notifications: dict[
        int, Callable[[Dataloaders, TrialEngagementInfo], Awaitable[None]]
    ] = {
        3: mail_add_members_notification,
        5: mail_send_define_treatments_notification,
        7: mail_send_add_repositories_notification,
        9: mail_support_channels_notification,
        13: mail_devsecops_agent_notification,
        15: mail_trial_reports_notification,
        17: mail_upgrade_squad_notification,
        19: mail_trial_ending_notification,
        20: mail_how_improve_notification,
        22: mail_trial_ended_notification,
    }
    loaders = get_new_context()
    groups = await orgs_domain.get_all_trial_groups(loaders)
    emails = [group.created_by for group in groups]
    trials = await loaders.trial.load_many(emails)

    await collect(
        tuple(
            notification(
                loaders,
                TrialEngagementInfo(
                    email_to=group.created_by,
                    group_name=group.name,
                    start_date=trial.start_date,
                ),
            )
            for group, trial in zip(groups, trials)
            if trial
            and trial.start_date
            and (
                notification := notifications.get(
                    datetime_utils.get_days_since(trial.start_date)
                )
            )
        )
    )


async def main() -> None:
    await send_trial_engagement_notification()
