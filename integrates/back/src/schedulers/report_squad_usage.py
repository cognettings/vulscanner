from aioextensions import (
    collect,
)
from billing.subscriptions import (
    utils as subs_utils,
)
from custom_exceptions import (
    NoActiveBillingSubscription,
)
from custom_utils import (
    bugsnag as bugsnag_utils,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.enums import (
    GroupTier,
)
from db_model.groups.types import (
    Group,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
    utils as orgs_utils,
)
from settings.logger import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)

bugsnag_utils.start_scheduler_session()


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    active_groups = await orgs_domain.get_all_active_groups(loaders)
    squad_groups: tuple[Group, ...] = tuple(
        group for group in active_groups if group.state.tier == GroupTier.SQUAD
    )
    squad_orgs_ids: list[str] = [
        group.organization_id for group in squad_groups
    ]
    squad_orgs = await collect(
        list(
            orgs_utils.get_organization(loaders, squad_orgs_id)
            for squad_orgs_id in squad_orgs_ids
        )
    )
    try:
        await collect(
            [
                subs_utils.report_subscription_usage(
                    group_name=group.name,
                    org_billing_customer=org.billing_customer,
                )
                for group, org in zip(squad_groups, squad_orgs)
                if org.billing_customer is not None
            ]
        )
    except NoActiveBillingSubscription as exc:
        LOGGER.exception(exc, extra={"squad_orgs": squad_orgs})
