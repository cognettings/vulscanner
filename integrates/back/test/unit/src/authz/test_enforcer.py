import authz
from authz import (
    get_group_level_roles_model,
    get_organization_level_roles_model,
)
from authz.enforcer import (
    get_group_level_enforcer,
    get_organization_level_enforcer,
    get_user_level_enforcer,
)
from back.test.unit.src.utils import (
    get_module_at_test,
    set_mocks_return_values,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
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
from db_model.types import (
    Policies,
)
from decimal import (
    Decimal,
)
import pytest
from typing import (
    Any,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]

MODULE_AT_TEST = get_module_at_test(file_path=__file__)
TABLE_NAME = "integrates_vms"


@pytest.mark.parametrize(
    ["email", "organization_id", "role"],
    [
        [
            "integrates@fluidattacks.com",
            "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2",
            "admin",
        ],
        [
            "integratesuser@gmail.com",
            "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            "user_manager",
        ],
        [
            "unittesting@fluidattacks.com",
            "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            "user",
        ],
        [
            "unittesting@gmail.com",
            "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2",
            "admin",
        ],
    ],
)
@patch(MODULE_AT_TEST + "get_user_level_role", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "Dataloaders.stakeholder_organizations_access",
    new_callable=AsyncMock,
)
async def test_organization_level_enforcer(
    # pylint: disable=too-many-arguments
    mock_dataloaders_stakeholder_organizations_access: AsyncMock,
    mock_get_user_level_role: AsyncMock,
    email: str,
    organization_id: str,
    role: str,
    mocked_data_for_module: Any,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_dataloaders_stakeholder_organizations_access.load,
            "Dataloaders.stakeholder_organizations_access",
            [email],
        ),
        (
            mock_get_user_level_role,
            "get_user_level_role",
            [email],
        ),
    ]
    # Set up mocks' results using mocked_data_for_module fixture
    for mock_item in mocks_setup_list:
        mock, path, arguments = mock_item
        mock.return_value = mocked_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )

    model = get_organization_level_roles_model()
    enforcer = await get_organization_level_enforcer(get_new_context(), email)
    for action in model[role]["actions"]:
        assert enforcer(
            organization_id, action
        ), f"{role} should be able to do {action}"
    for other_role in model:  # pylint: disable=consider-using-dict-items
        for action in model[other_role]["actions"] - model[role]["actions"]:
            assert not enforcer(
                organization_id, action
            ), f"{role} should not be able to do {action}"


@pytest.mark.parametrize(
    ["email", "group", "role"],
    [
        [
            "integratesuser@gmail.com",
            "unittesting",
            "user_manager",
        ],
        [
            "integrateshacker@fluidattacks.com",
            "unittesting",
            "hacker",
        ],
        [
            "continuoushacking@gmail.com",
            "oneshottest",
            "user_manager",
        ],
        [
            "integrateshacker@fluidattacks.com",
            "oneshottest",
            "reattacker",
        ],
        [
            "integratesuser@gmail.com",
            "oneshottest",
            "user",
        ],
    ],
)
@patch(MODULE_AT_TEST + "get_user_level_role", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "Dataloaders.stakeholder_groups_access",
    new_callable=AsyncMock,
)
async def test_get_group_level_enforcer(
    mock_dataloaders_stakeholder_groups_access: AsyncMock,
    mock_get_user_level_role: AsyncMock,
    email: str,
    group: str,
    role: str,
) -> None:
    mocked_objects, mocked_paths, mocks_args = [
        [
            mock_dataloaders_stakeholder_groups_access.load,
            mock_get_user_level_role,
        ],
        ["Dataloaders.stakeholder_groups_access", "get_user_level_role"],
        [
            [email],
            [email],
        ],
    ]
    assert set_mocks_return_values(
        mocks_args=mocks_args,
        mocked_objects=mocked_objects,
        module_at_test=MODULE_AT_TEST,
        paths_list=mocked_paths,
    )
    model = get_group_level_roles_model()
    loaders: Dataloaders = get_new_context()
    enforcer = await get_group_level_enforcer(loaders, email)
    for action in model[role]["actions"]:
        assert enforcer(group, action), f"{role} should be able to do {action}"
    for other_role in model:  # pylint: disable=consider-using-dict-items
        for action in model[other_role]["actions"] - model[role]["actions"]:
            assert not enforcer(
                group, action
            ), f"{role} should not be able to do {action}"
    assert all(mock_object.called is True for mock_object in mocked_objects)


@pytest.mark.parametrize(
    ["email", "bad_action", "good_action"],
    [
        [
            "integrateshacker@fluidattacks.com",
            "api_mutations_submit_group_machine_execution_mutate",
            "api_mutations_update_stakeholder_phone_mutate",
        ],
    ],
)
@patch(MODULE_AT_TEST + "get_user_level_role", new_callable=AsyncMock)
async def test_get_user_level_enforcer(
    mock_get_user_level_role: AsyncMock,
    email: str,
    bad_action: str,
    good_action: str,
) -> None:
    loaders: Dataloaders = get_new_context()
    assert set_mocks_return_values(
        mocks_args=[[email]],
        mocked_objects=[mock_get_user_level_role],
        module_at_test=MODULE_AT_TEST,
        paths_list=["get_user_level_role"],
    )
    enforcer = await get_user_level_enforcer(loaders, email)
    assert not enforcer(bad_action)
    assert enforcer(good_action)


@pytest.mark.parametrize(
    ["group", "attributes", "results"],
    [
        [
            Group(
                business_name="Testing Company and Sons",
                policies=Policies(
                    max_number_acceptances=3,
                    min_acceptance_severity=Decimal("0"),
                    vulnerability_grace_period=10,
                    modified_by="integratesmanager@gmail.com",
                    min_breaking_severity=Decimal("3.9"),
                    max_acceptance_days=90,
                    modified_date=datetime.fromisoformat(
                        "2021-11-22T20:07:57+00:00"
                    ),
                    max_acceptance_severity=Decimal("3.9"),
                ),
                context="Group context test",
                disambiguation="Disambiguation test",
                description="Integrates unit test group",
                language=GroupLanguage.EN,
                created_by="integratesmanager@gmail.com",
                organization_id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                name="unittesting",
                created_date=datetime.fromisoformat(
                    "2018-03-08T00:43:18+00:00"
                ),
                state=GroupState(
                    has_machine=True,
                    has_squad=True,
                    managed=GroupManaged.NOT_MANAGED,
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-03-08T00:43:18+00:00"
                    ),
                    status=GroupStateStatus.ACTIVE,
                    tier=GroupTier.MACHINE,
                    type=GroupSubscriptionType.CONTINUOUS,
                    tags=set(("test-groups", "test-updates", "test-tag")),
                    service=GroupService.WHITE,
                ),
                business_id="14441323",
                sprint_duration=2,
            ),
            [
                "can_report_vulnerabilities",
                "can_request_zero_risk",
                "has_asm",
                "has_forces",
                "has_service_black",
                "has_service_white",
                "has_squad",
                "is_continuous",
                "is_fluidattacks_customer",
                "must_only_have_fluidattacks_hackers",
                "non_existing_attribute",
            ],
            [
                True,
                True,
                True,
                True,
                False,
                True,
                True,
                True,
                True,
                True,
                False,
            ],
        ],
        [
            Group(
                business_name="Testing Company and Sons",
                policies=Policies(
                    max_number_acceptances=3,
                    min_acceptance_severity=Decimal("0"),
                    vulnerability_grace_period=10,
                    modified_by="integratesmanager@gmail.com",
                    min_breaking_severity=Decimal("3.9"),
                    max_acceptance_days=90,
                    modified_date=datetime.fromisoformat(
                        "2021-11-22T20:07:57+00:00"
                    ),
                    max_acceptance_severity=Decimal("3.9"),
                ),
                context="Group context test",
                disambiguation="Disambiguation test",
                description="Oneshottest test group",
                language=GroupLanguage.EN,
                created_by="integratesmanager@gmail.com",
                organization_id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                name="oneshottest",
                created_date=datetime.fromisoformat(
                    "2019-01-20T22:00:00+00:00"
                ),
                state=GroupState(
                    has_machine=True,
                    has_squad=False,
                    managed=GroupManaged.NOT_MANAGED,
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2019-01-20T22:00:00+00:00"
                    ),
                    status=GroupStateStatus.ACTIVE,
                    tier=GroupTier.ONESHOT,
                    type=GroupSubscriptionType.ONESHOT,
                    tags=set(("test-tag")),
                    service=GroupService.BLACK,
                ),
                business_id="14441323",
                sprint_duration=2,
            ),
            [
                "can_report_vulnerabilities",
                "can_request_zero_risk",
                "has_asm",
                "has_forces",
                "has_service_black",
                "has_service_white",
                "has_squad",
                "is_continuous",
                "is_fluidattacks_customer",
                "must_only_have_fluidattacks_hackers",
                "non_existing_attribute",
            ],
            [
                True,
                True,
                True,
                False,
                True,
                False,
                False,
                False,
                True,
                True,
                False,
            ],
        ],
    ],
)
async def test_group_service_attributes_enforcer(
    group: Group,
    attributes: list,
    results: list,
) -> None:
    # All attributes must be tested for this test to succeed
    # This prevents someone to add a new attribute without testing it

    attributes_remaining_to_test: set[str] = {
        (attr)
        for attrs in authz.SERVICE_ATTRIBUTES.values()
        for attr in set(attrs).union({"non_existing_attribute"})
    }

    enforcer = authz.get_group_service_attributes_enforcer(group)

    for attribute, result in zip(attributes, results):
        assert (
            enforcer(attribute) == result
        ), f"{group.name} attribute: {attribute}, should have value {result}"

        attributes_remaining_to_test.remove(attribute)

    assert not attributes_remaining_to_test, (
        f"Please add tests for the following pairs of (group, attribute)"
        f": {attributes_remaining_to_test}"
    )
