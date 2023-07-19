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
    Stakeholder,
)
from db_model.trials.types import (
    Trial,
)
from db_model.types import (
    Policies,
)
import pytest
import pytest_asyncio


@pytest.mark.resolver_test_group("expire_free_trial")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate() -> bool:
    data = {
        "trials": [
            Trial(
                email="johndoe@johndoe.com",
                completed=False,
                extension_date=None,
                extension_days=0,
                start_date=datetime.fromisoformat(
                    "2022-10-21T15:58:31.280182+00:00"
                ),
            ),
            Trial(
                email="janedoe@janedoe.com",
                completed=False,
                extension_date=None,
                extension_days=0,
                start_date=datetime.fromisoformat(
                    "2022-10-22T15:58:31.280182"
                ),
            ),
            Trial(
                email="uiguaran@uiguaran.com",
                completed=False,
                extension_date=datetime.fromisoformat(
                    "2022-11-11T15:58:31.280182"
                ),
                extension_days=1,
                start_date=datetime.fromisoformat(
                    "2022-10-21T15:58:31.280182+00:00"
                ),
            ),
            Trial(
                email="abuendia@abuendia.com",
                completed=True,
                extension_date=None,
                extension_days=0,
                start_date=datetime.fromisoformat(
                    "2022-10-21T15:58:31.280182+00:00"
                ),
            ),
            Trial(
                email="atoriyama@atoriyama.com",
                completed=True,
                extension_date=None,
                extension_days=0,
                start_date=datetime.fromisoformat(
                    "2022-09-20T15:58:31.280182+00:00"
                ),
            ),
            Trial(
                email="hanno@hanno.com",
                completed=True,
                extension_date=None,
                extension_days=0,
                start_date=datetime.fromisoformat(
                    "2022-09-21T15:58:31.280182+00:00"
                ),
            ),
        ],
        "groups": [
            {
                "group": Group(
                    created_by="johndoe@johndoe.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup",
                    organization_id="e314a87c-223f-44bc-8317-75900f2ffbc7",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.TRIAL,
                        modified_by="johndoe@johndoe.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.FREE,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                ),
            },
            {
                "group": Group(
                    created_by="janedoe@janedoe.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup2",
                    organization_id="5ee9880b-5e19-44ba-baf1-f2601bdf7d25",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.TRIAL,
                        modified_by="janedoe@janedoe.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.FREE,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                ),
            },
            {
                "group": Group(
                    created_by="uiguaran@uiguaran.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup3",
                    organization_id="a2204896-fbd0-4c55-8163-4cb3b018551c",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.TRIAL,
                        modified_by="uiguaran@uiguaran.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.FREE,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                ),
            },
            {
                "group": Group(
                    created_by="abuendia@abuendia.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup4",
                    organization_id="5399f49f-6e2c-4712-af72-5ea6e34cf15d",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.MANAGED,
                        modified_by="abuendia@abuendia.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.FREE,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                ),
            },
            {
                "group": Group(
                    created_by="atoriyama@atoriyama.com",
                    created_date=datetime.fromisoformat(
                        "2022-09-20T15:58:31.280182+00:00"
                    ),
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup5",
                    organization_id="5399f49f-6e2c-4712-af72-5ea6e34cf155",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.UNDER_REVIEW,
                        modified_by="atoriyama@atoriyama.com",
                        modified_date=datetime.fromisoformat(
                            "2022-09-20T15:58:31.280182+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.FREE,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                ),
            },
            {
                "group": Group(
                    created_by="hanno@hanno.com",
                    created_date=datetime.fromisoformat(
                        "2022-09-21T15:58:31.280182+00:00"
                    ),
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup6",
                    organization_id="5399f49f-6e2c-4712-af72-5ea6e34cf156",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.UNDER_REVIEW,
                        modified_by="hanno@hanno.com",
                        modified_date=datetime.fromisoformat(
                            "2022-09-21T15:58:31.280182+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.FREE,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                ),
            },
        ],
        "organizations": [
            {
                "organization": Organization(
                    created_by="johndoe@johndoe.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="e314a87c-223f-44bc-8317-75900f2ffbc7",
                    name="testorg",
                    policies=Policies(
                        modified_by="johndoe@johndoe.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="johndoe@johndoe.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    created_by="janedoe@janedoe.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="5ee9880b-5e19-44ba-baf1-f2601bdf7d25",
                    name="testorg2",
                    policies=Policies(
                        modified_by="janedoe@janedoe.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="janedoe@janedoe.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    created_by="uiguaran@uiguaran.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="a2204896-fbd0-4c55-8163-4cb3b018551c",
                    name="testorg3",
                    policies=Policies(
                        modified_by="uiguaran@uiguaran.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="uiguaran@uiguaran.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    created_by="abuendia@abuendia.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="5399f49f-6e2c-4712-af72-5ea6e34cf15d",
                    name="testorg4",
                    policies=Policies(
                        modified_by="abuendia@abuendia.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="abuendia@abuendia.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    created_by="atoriyama@atoriyama.com",
                    created_date=datetime.fromisoformat(
                        "2022-09-20T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="5399f49f-6e2c-4712-af72-5ea6e34cf155",
                    name="testorg5",
                    policies=Policies(
                        modified_by="atoriyama@atoriyama.com",
                        modified_date=datetime.fromisoformat(
                            "2022-09-20T15:58:31.280182+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="atoriyama@atoriyama.com",
                        modified_date=datetime.fromisoformat(
                            "2022-09-20T15:58:31.280182+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    created_by="hanno@hanno.com",
                    created_date=datetime.fromisoformat(
                        "2022-09-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="5399f49f-6e2c-4712-af72-5ea6e34cf156",
                    name="testorg6",
                    policies=Policies(
                        modified_by="hanno@hanno.com",
                        modified_date=datetime.fromisoformat(
                            "2022-09-21T15:58:31.280182+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="hanno@hanno.com",
                        modified_date=datetime.fromisoformat(
                            "2022-09-21T15:58:31.280182+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
        ],
        "stakeholders": [
            Stakeholder(
                email="johndoe@johndoe.com",
                first_name="John",
                is_registered=True,
                last_name="Doe",
            ),
            Stakeholder(
                email="janedoe@janedoe.com",
                first_name="Jane",
                is_registered=True,
                last_name="Doe",
            ),
            Stakeholder(
                email="uiguaran@uiguaran.com",
                first_name="Ursula",
                is_registered=True,
                last_name="Iguaran",
            ),
            Stakeholder(
                email="abuendia@abuendia.com",
                first_name="Amaranta",
                is_registered=True,
                last_name="Buendia",
            ),
            Stakeholder(
                email="atoriyama@atoriyama.com",
                first_name="Akira",
                is_registered=True,
                last_name="Toriyama",
            ),
            Stakeholder(
                email="hanno@hanno.com",
                first_name="Hideaki",
                is_registered=True,
                last_name="Anno",
            ),
        ],
    }
    return await db.populate(data)
