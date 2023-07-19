# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupManaged,
    GroupService,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupState,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationState,
)
from db_model.stakeholders.types import (
    NotificationsPreferences,
    Stakeholder,
    StakeholderState,
)
from db_model.types import (
    Policies,
)
import pytest
import pytest_asyncio


@pytest.mark.resolver_test_group("newsletter_notification")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate() -> bool:
    data = {
        "organizations": [
            {
                "organization": Organization(
                    created_by="johndoe@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2022-11-24T15:58:31.280182"
                    ),
                    country="Colombia",
                    id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    name="trialorg",
                    policies=Policies(
                        modified_by="johndoe@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-11-24T15:58:31.280182+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="johndoe@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-11-24T15:58:31.280182+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
        ],
        "groups": [
            {
                "group": Group(
                    created_by="unknown",
                    created_date=datetime.fromisoformat(
                        "2022-11-24T22:00:00+00:00"
                    ),
                    description="-",
                    language=GroupLanguage.EN,
                    name="group",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="unknown",
                        modified_date=datetime.fromisoformat(
                            "2022-11-24T22:00:00+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    sprint_start_date=datetime.fromisoformat(
                        "2022-10-24T00:00:00+00:00"
                    ),
                ),
            },
        ],
        "policies": [
            {
                "level": "group",
                "subject": "johndoe@fluidattacks.com",
                "object": "group",
                "role": "user_manager",
            }
        ],
        "stakeholders": [
            Stakeholder(
                email="johndoe@fluidattacks.com",
                first_name="John",
                is_registered=True,
                last_name="Doe",
                registration_date=datetime.fromisoformat(
                    "2022-10-21T15:50:31.280182"
                ),
                state=StakeholderState(
                    modified_by="unknown",
                    modified_date=datetime.fromisoformat(
                        "2022-10-24T00:00:00+00:00"
                    ),
                    notifications_preferences=NotificationsPreferences(
                        email=["UPDATED_TREATMENT"],
                    ),
                ),
            ),
        ],
    }
    return await db.populate(data)
