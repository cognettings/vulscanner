from authz.validations import (
    validate_fluidattacks_staff_on_group,
    validate_fluidattacks_staff_on_group_deco,
    validate_handle_comment_scope,
    validate_handle_comment_scope_deco,
    validate_role_fluid_reqs,
    validate_role_fluid_reqs_deco,
)
from back.test.unit.src.utils import (
    get_module_at_test,
)
from collections.abc import (
    Callable,
)
from custom_exceptions import (
    InvalidUserProvided,
    PermissionDenied,
    UnexpectedUserRole,
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
    NamedTuple,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

FLUIDATTACKS_EMAIL_SUFFIX = "@fluidattacks.com"
MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    [
        "group",
        "email",
        "role",
    ],
    [
        [
            Group(
                created_by="unknown",
                created_date=datetime.fromisoformat("2019-01-20"),
                description="oneshot testing",
                language=GroupLanguage.EN,
                name="oneshottest",
                organization_id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                state=GroupState(
                    has_machine=True,
                    has_squad=False,
                    managed=GroupManaged.NOT_MANAGED,
                    modified_by="unknown",
                    modified_date=datetime.fromisoformat("2019-01-20"),
                    status=GroupStateStatus.ACTIVE,
                    tier=GroupTier.ONESHOT,
                    type=GroupSubscriptionType.ONESHOT,
                    tags={
                        "test-groups",
                        "another-tag",
                        "test-tag",
                        "test-updates",
                    },
                    comments=None,
                    justification=None,
                    payment_id=None,
                    pending_deletion_date=None,
                    service=GroupService.BLACK,
                ),
                agent_token=None,
                business_id="14441323",
                business_name="Testing Company and Sons",
                context=None,
                disambiguation=None,
                files=None,
                policies=Policies(
                    modified_date=datetime.fromisoformat(
                        "2021-11-22T20:07:57+00:00"
                    ),
                    modified_by="integratesmanager@gmail.com",
                    inactivity_period=None,
                    max_acceptance_days=90,
                    max_acceptance_severity=Decimal("3.9"),
                    max_number_acceptances=3,
                    min_acceptance_severity=Decimal("0"),
                    min_breaking_severity=Decimal("3.9"),
                    vulnerability_grace_period=10,
                ),
                sprint_duration=2,
                sprint_start_date=datetime.fromisoformat("2023-02-20"),
            ),
            "test@fluidattacks.com",
            "hacker",
        ],
        [
            Group(
                created_by="unknown",
                created_date=datetime.fromisoformat("2019-01-20"),
                description="oneshot testing",
                language=GroupLanguage.EN,
                name="oneshottest",
                organization_id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                state=GroupState(
                    has_machine=True,
                    has_squad=False,
                    managed=GroupManaged.NOT_MANAGED,
                    modified_by="unknown",
                    modified_date=datetime.fromisoformat("2019-01-20"),
                    status=GroupStateStatus.ACTIVE,
                    tier=GroupTier.ONESHOT,
                    type=GroupSubscriptionType.ONESHOT,
                    tags={
                        "test-groups",
                        "another-tag",
                        "test-tag",
                        "test-updates",
                    },
                    comments=None,
                    justification=None,
                    payment_id=None,
                    pending_deletion_date=None,
                    service=GroupService.BLACK,
                ),
                agent_token=None,
                business_id="14441323",
                business_name="Testing Company and Sons",
                context=None,
                disambiguation=None,
                files=None,
                policies=Policies(
                    modified_date=datetime.fromisoformat(
                        "2021-11-22T20:07:57+00:00"
                    ),
                    modified_by="integratesmanager@gmail.com",
                    inactivity_period=None,
                    max_acceptance_days=90,
                    max_acceptance_severity=Decimal("3.9"),
                    max_number_acceptances=3,
                    min_acceptance_severity=Decimal("0"),
                    min_breaking_severity=Decimal("3.9"),
                    vulnerability_grace_period=10,
                ),
                sprint_duration=2,
                sprint_start_date=datetime.fromisoformat("2023-02-20"),
            ),
            "test@gmail.com",
            "user",
        ],
    ],
)
async def test_validate_fluidattacks_staff_on_group(
    group: Group, email: str, role: str
) -> None:
    assert validate_fluidattacks_staff_on_group(group, email, role)
    if not email.endswith(FLUIDATTACKS_EMAIL_SUFFIX):
        with pytest.raises(UnexpectedUserRole):
            validate_fluidattacks_staff_on_group(group, email, "hacker")


@pytest.mark.parametrize(
    [
        "group",
        "email",
        "role",
    ],
    [
        [
            Group(
                created_by="unknown",
                created_date=datetime.fromisoformat("2019-01-20"),
                description="oneshot testing",
                language=GroupLanguage.EN,
                name="oneshottest",
                organization_id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                state=GroupState(
                    has_machine=True,
                    has_squad=False,
                    managed=GroupManaged.NOT_MANAGED,
                    modified_by="unknown",
                    modified_date=datetime.fromisoformat("2019-01-20"),
                    status=GroupStateStatus.ACTIVE,
                    tier=GroupTier.ONESHOT,
                    type=GroupSubscriptionType.ONESHOT,
                    tags={
                        "test-groups",
                        "another-tag",
                        "test-tag",
                        "test-updates",
                    },
                    comments=None,
                    justification=None,
                    payment_id=None,
                    pending_deletion_date=None,
                    service=GroupService.BLACK,
                ),
                agent_token=None,
                business_id="14441323",
                business_name="Testing Company and Sons",
                context=None,
                disambiguation=None,
                files=None,
                policies=Policies(
                    modified_date=datetime.fromisoformat(
                        "2021-11-22T20:07:57+00:00"
                    ),
                    modified_by="integratesmanager@gmail.com",
                    inactivity_period=None,
                    max_acceptance_days=90,
                    max_acceptance_severity=Decimal("3.9"),
                    max_number_acceptances=3,
                    min_acceptance_severity=Decimal("0"),
                    min_breaking_severity=Decimal("3.9"),
                    vulnerability_grace_period=10,
                ),
                sprint_duration=2,
                sprint_start_date=datetime.fromisoformat("2023-02-20"),
            ),
            "test@fluidattacks.com",
            "hacker",
        ],
        [
            Group(
                created_by="unknown",
                created_date=datetime.fromisoformat("2019-01-20"),
                description="oneshot testing",
                language=GroupLanguage.EN,
                name="oneshottest",
                organization_id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                state=GroupState(
                    has_machine=True,
                    has_squad=False,
                    managed=GroupManaged.NOT_MANAGED,
                    modified_by="unknown",
                    modified_date=datetime.fromisoformat("2019-01-20"),
                    status=GroupStateStatus.ACTIVE,
                    tier=GroupTier.ONESHOT,
                    type=GroupSubscriptionType.ONESHOT,
                    tags={
                        "test-groups",
                        "another-tag",
                        "test-tag",
                        "test-updates",
                    },
                    comments=None,
                    justification=None,
                    payment_id=None,
                    pending_deletion_date=None,
                    service=GroupService.BLACK,
                ),
                agent_token=None,
                business_id="14441323",
                business_name="Testing Company and Sons",
                context=None,
                disambiguation=None,
                files=None,
                policies=Policies(
                    modified_date=datetime.fromisoformat(
                        "2021-11-22T20:07:57+00:00"
                    ),
                    modified_by="integratesmanager@gmail.com",
                    inactivity_period=None,
                    max_acceptance_days=90,
                    max_acceptance_severity=Decimal("3.9"),
                    max_number_acceptances=3,
                    min_acceptance_severity=Decimal("0"),
                    min_breaking_severity=Decimal("3.9"),
                    vulnerability_grace_period=10,
                ),
                sprint_duration=2,
                sprint_start_date=datetime.fromisoformat("2023-02-20"),
            ),
            "test@gmail.com",
            "user",
        ],
    ],
)
async def test_validate_fluidattacks_staff_on_group_deco(
    group: Group, email: str, role: str
) -> None:
    @validate_fluidattacks_staff_on_group_deco("group", "email", "role")
    def decorated_func(
        group: Group, email: str, role: str
    ) -> tuple[Group, str, str]:
        return (group, email, role)

    assert decorated_func(
        group=group,
        email=email,
        role=role,
    )
    if not email.endswith(FLUIDATTACKS_EMAIL_SUFFIX):
        with pytest.raises(UnexpectedUserRole):
            decorated_func(
                group=group,
                email="test@gmail.com",
                role="hacker",
            )

    class TestClass(NamedTuple):
        group: Group
        email: str
        role: str

    if not email.endswith(FLUIDATTACKS_EMAIL_SUFFIX):
        test_obj_fail = TestClass(group=group, email=email, role="hacker")
    else:
        test_obj = TestClass(group=group, email=email, role=role)

    @validate_fluidattacks_staff_on_group_deco(
        "test_obj.group",
        "test_obj.email",
        "test_obj.role",
    )
    def decorated_func_obj(test_obj: TestClass) -> TestClass:
        return test_obj

    if not email.endswith(FLUIDATTACKS_EMAIL_SUFFIX):
        with pytest.raises(UnexpectedUserRole):
            decorated_func_obj(test_obj=test_obj_fail)
    else:
        assert decorated_func_obj(test_obj=test_obj)


def test_validate_role_fluid_reqs() -> None:
    assert validate_role_fluid_reqs(email="test@gmail.com", role="hacker")
    assert validate_role_fluid_reqs(
        email="test@fluidattacks.com", role="customer_manager"
    )
    with pytest.raises(InvalidUserProvided):
        validate_role_fluid_reqs(
            email="test@gmail.com", role="customer_manager"
        )


def test_validate_role_fluid_reqs_deco() -> None:
    @validate_role_fluid_reqs_deco("email", "role")
    def decorated_func(email: str, role: str) -> str:
        return email + role

    assert decorated_func(email="test@gmail.com", role="hacker")
    assert decorated_func(
        email="test@fluidattacks.com", role="customer_manager"
    )
    with pytest.raises(InvalidUserProvided):
        decorated_func(email="test@gmail.com", role="customer_manager")


@pytest.mark.parametrize(
    ["content", "user_email", "group_name", "parent_comment"],
    [
        ["#internal", "unittest@fluidattacks.com", "unittesting", "0"],
        ["test_content", "unittest@fluidattacks.com", "unittesting", ""],
    ],
)
@patch(MODULE_AT_TEST + "get_group_level_enforcer", new_callable=AsyncMock)
async def test_validate_handle_comment_scope(
    # pylint: disable=too-many-arguments
    mock_get_group_level_enforcer: AsyncMock,
    content: str,
    user_email: str,
    group_name: str,
    parent_comment: str,
    side_effect_get_group_level_enforcer: Callable[[str, str], bool],
) -> None:
    # Set up mock's side_effect using side_effect_get_group_level_enforcer
    # fixture
    mock_get_group_level_enforcer.side_effect = (
        side_effect_get_group_level_enforcer
    )
    if content.strip() in {"#external", "#internal"}:
        with pytest.raises(PermissionDenied):
            await validate_handle_comment_scope(
                loaders=get_new_context(),
                content=content,
                user_email=user_email,
                group_name=group_name,
                parent_comment=parent_comment,
            )
        assert mock_get_group_level_enforcer.called is True
    else:
        await validate_handle_comment_scope(
            loaders=get_new_context(),
            content=content,
            user_email=user_email,
            group_name=group_name,
            parent_comment=parent_comment,
        )
        assert mock_get_group_level_enforcer.called is True


@patch(MODULE_AT_TEST + "get_group_level_enforcer", new_callable=AsyncMock)
async def test_validate_handle_comment_scope_deco(
    mock_get_group_level_enforcer: AsyncMock,
    side_effect_get_group_level_enforcer: Callable[[str, str], bool],
) -> None:
    # Set up mock's side_effect using side_effect_get_group_level_enforcer
    # fixture
    mock_get_group_level_enforcer.side_effect = (
        side_effect_get_group_level_enforcer
    )

    @validate_handle_comment_scope_deco(
        "loaders", "content", "user_email", "group_name", "parent_comment"
    )
    async def decorated_function(
        loaders: Dataloaders,
        content: str,
        user_email: str,
        group_name: str,
        parent_comment: str,
    ) -> tuple:
        return (loaders, content, user_email, group_name, parent_comment)

    with pytest.raises(PermissionDenied):
        await decorated_function(
            loaders=get_new_context(),
            content="#internal",
            user_email="unittest@fluidattacks.com",
            group_name="unittesting",
            parent_comment="0",
        )
    assert mock_get_group_level_enforcer.called is True
