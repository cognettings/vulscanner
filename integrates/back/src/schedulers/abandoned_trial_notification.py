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
from db_model import (
    stakeholders as stakeholders_model,
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

# Constants
INACTIVE_HOURS = [1, 24]


mail_abandoned_trial_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(trial_mail.send_abandoned_trial_notification)


async def send_abandoned_trial_notification() -> None:
    loaders: Dataloaders = get_new_context()
    for stakeholder in await stakeholders_model.get_all_stakeholders():
        if (
            not stakeholder.enrolled
            and stakeholder.registration_date
            and (
                delta_hours := (
                    datetime_utils.get_utc_now()
                    - stakeholder.registration_date
                ).total_seconds()
                // 3600
            )
            and delta_hours in INACTIVE_HOURS
        ):
            await mail_abandoned_trial_notification(
                loaders, stakeholder.email, delta_hours == 1
            )


async def main() -> None:
    await send_abandoned_trial_notification()
