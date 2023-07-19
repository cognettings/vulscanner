# pylint: disable=too-many-lines
from back.test.unit.src.utils import (
    get_mock_response,
    get_mocked_path,
    get_module_at_test,
    set_mocks_return_values,
)
from collections.abc import (
    Callable,
)
from custom_exceptions import (
    InvalidGroupServicesConfig,
    RepeatedValues,
)
from custom_utils import (
    datetime as datetime_utils,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    date,
    datetime,
    timedelta,
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
    GroupTreatmentSummary,
)
from decimal import (
    Decimal,
)
from freezegun import (
    freeze_time,
)
from groups.domain import (
    add_group,
    get_closed_vulnerabilities,
    get_groups_by_stakeholder,
    get_mean_remediate_non_treated_severity,
    get_mean_remediate_non_treated_severity_cvssf,
    get_mean_remediate_severity,
    get_mean_remediate_severity_cvssf,
    get_open_findings,
    get_open_vulnerabilities,
    get_treatment_summary,
    get_vulnerabilities_with_pending_attacks,
    is_valid,
    remove_pending_deletion_date,
    send_mail_devsecops_agent,
    set_pending_deletion_date,
    validate_group_services_config,
    validate_group_services_config_deco,
    validate_group_tags,
)
import json
import pytest
from typing import (
    Any,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@patch(
    MODULE_AT_TEST + "notifications_domain.new_group", new_callable=AsyncMock
)
@patch(MODULE_AT_TEST + "authz.grant_group_level_role", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "group_access_domain.update", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "orgs_domain.add_group_access", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "groups_model.add", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "trials_domain.in_trial", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "exists", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "org_access.has_access", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "orgs_utils.get_organization", new_callable=AsyncMock)
async def test_add_group(
    # pylint: disable=too-many-arguments, too-many-locals
    mock_orgs_utils_get_organization: AsyncMock,
    mock_org_access_has_access: AsyncMock,
    mock_exists: AsyncMock,
    mock_trials_domain_in_trial: AsyncMock,
    moc_groups_model_add: AsyncMock,
    mock_orgs_domain_add_group_access: AsyncMock,
    mock_group_access_domain_update: AsyncMock,
    mock_authz_grant_group_level_role: AsyncMock,
    mock_notifications_domain_new_group: AsyncMock,
    mock_data_for_module: Callable,
) -> None:
    description = "This is a new group"
    email = "integratesuser@gmail.com"
    granted_role = "user_manager"
    group_name = "newavailablename"
    has_machine = True
    has_squad = True
    organization_name = "okada"
    group_service = GroupService.WHITE
    subscription = GroupSubscriptionType.CONTINUOUS

    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_orgs_utils_get_organization,
            "orgs_utils.get_organization",
            [organization_name],
        ),
        (
            mock_org_access_has_access,
            "org_access.has_access",
            [organization_name, email],
        ),
        (mock_exists, "exists", [group_name]),
        (
            mock_trials_domain_in_trial,
            "trials_domain.in_trial",
            [email, organization_name],
        ),
        (
            moc_groups_model_add,
            "groups_model.add",
            [
                email,
                description,
                has_machine,
                has_squad,
                group_service,
                subscription,
                organization_name,
            ],
        ),
        (
            mock_orgs_domain_add_group_access,
            "orgs_domain.add_group_access",
            [organization_name, group_name],
        ),
        (
            mock_group_access_domain_update,
            "group_access_domain.update",
            [email, group_name],
        ),
        (
            mock_authz_grant_group_level_role,
            "authz.grant_group_level_role",
            [email, group_name],
        ),
        (
            mock_notifications_domain_new_group,
            "notifications_domain.new_group",
            [
                description,
                group_name,
                has_machine,
                has_squad,
                organization_name,
                email,
                group_service,
                subscription,
            ],
        ),
    ]
    # Set up mocks' results using mock_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mock_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )

    loaders: Dataloaders = get_new_context()
    await add_group(
        loaders=loaders,
        description=description,
        email=email,
        granted_role=granted_role,
        group_name=group_name,
        has_machine=has_machine,
        has_squad=has_squad,
        organization_name=organization_name,
        service=group_service,
        subscription=subscription,
    )
    mocks_list = [mock[0] for mock in mocks_setup_list]
    assert all(mock_object.called is True for mock_object in mocks_list)


@pytest.mark.parametrize(
    ["group_name", "expected_output"],
    [["oneshottest", 1]],
)
@patch(
    MODULE_AT_TEST + "Dataloaders.finding_vulnerabilities_released_nzr",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "get_group_findings", new_callable=AsyncMock)
async def test_get_closed_vulnerabilities(
    mock_get_group_findings: AsyncMock,
    mock_dataloaders_finding_vulnerabilities_released_nzr: AsyncMock,
    group_name: str,
    expected_output: int,
    mock_data_for_module: Callable,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_get_group_findings,
            "get_group_findings",
            [group_name],
        ),
        (
            mock_dataloaders_finding_vulnerabilities_released_nzr.load_many_chained,  # noqa: E501 pylint: disable=line-too-long
            "Dataloaders.finding_vulnerabilities_released_nzr",
            [group_name],
        ),
    ]
    # Set up mocks' results using mock_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mock_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    closed_vulnerabilities = await get_closed_vulnerabilities(
        get_new_context(), group_name
    )
    assert closed_vulnerabilities == expected_output
    assert mock_get_group_findings.called is True
    assert (
        mock_dataloaders_finding_vulnerabilities_released_nzr.load_many_chained.called  # noqa: E501 pylint: disable=line-too-long
        is True
    )


@pytest.mark.parametrize(
    ["email", "expected_groups", "org_id", "expected_org_groups"],
    [
        [
            "integratesmanager@gmail.com",
            [
                "asgard",
                "barranquilla",
                "gotham",
                "metropolis",
                "oneshottest",
                "monteria",
                "unittesting",
            ],
            "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            ["oneshottest", "unittesting"],
        ]
    ],
)
@patch(MODULE_AT_TEST + "authz.get_group_level_roles", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "Dataloaders.organization_groups", new_callable=AsyncMock
)
@patch(
    MODULE_AT_TEST + "group_access_domain.get_stakeholder_groups_names",
    new_callable=AsyncMock,
)
async def test_get_groups_by_stakeholder(
    # pylint: disable=too-many-arguments, too-many-locals
    mock_group_access_domain_get_stakeholder_groups_names: AsyncMock,
    mock_dataloaders_organization_groups: AsyncMock,
    mock_authz_get_group_level_roles: AsyncMock,
    email: str,
    expected_groups: list[str],
    org_id: str,
    expected_org_groups: list[str],
    mock_data_for_module: Callable,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_group_access_domain_get_stakeholder_groups_names,
            "group_access_domain.get_stakeholder_groups_names",
            [email],
        ),
        (
            mock_dataloaders_organization_groups.load,
            "Dataloaders.organization_groups",
            [org_id],
        ),
        (
            mock_authz_get_group_level_roles,
            "authz.get_group_level_roles",
            [email],
        ),
    ]
    # Set up mocks' results using mock_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mock_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    loaders: Dataloaders = get_new_context()
    user_groups_names = await get_groups_by_stakeholder(loaders, email)
    assert user_groups_names == sorted(expected_groups)
    assert mock_group_access_domain_get_stakeholder_groups_names.called is True
    assert mock_authz_get_group_level_roles.called is True

    user_org_groups_names = await get_groups_by_stakeholder(
        loaders, email, organization_id=org_id
    )
    # Modify mock_authz_get_group_level_roles's result using
    # mock_data_for_module fixture
    mock_authz_get_group_level_roles.return_value = mock_data_for_module(
        mock_path="authz.get_group_level_roles",
        mock_args=[email, org_id],
        module_at_test=MODULE_AT_TEST,
    )
    assert user_org_groups_names == sorted(expected_org_groups)
    assert (
        mock_group_access_domain_get_stakeholder_groups_names.call_count == 2
    )
    assert mock_authz_get_group_level_roles.call_count == 2
    assert mock_dataloaders_organization_groups.load.called is True


@freeze_time("2020-12-01")
@pytest.mark.parametrize(
    [
        "group_name",
        "min_severity",
        "max_severity",
        "min_date",
        "expected_result",
    ],
    [
        [
            "unittesting",
            Decimal("0.0"),
            Decimal("10.0"),
            None,
            Decimal("387.0"),
        ],
        [
            "unittesting",
            Decimal("0.0"),
            Decimal("10.0"),
            date(2020, 10, 31),
            Decimal("0.0"),
        ],
        [
            "unittesting",
            Decimal("0.0"),
            Decimal("10.0"),
            date(2020, 9, 1),
            Decimal("0.0"),
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "Dataloaders.finding_vulnerabilities",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "get_group_findings", new_callable=AsyncMock)
async def test_get_mean_remediate_non_treated_severity(
    # pylint: disable=too-many-arguments
    mock_get_group_findings: AsyncMock,
    mock_dataloaders_finding_vulnerabilities: AsyncMock,
    group_name: str,
    min_severity: Decimal,
    max_severity: Decimal,
    min_date: date | None,
    expected_result: Decimal,
    mock_data_for_module: Callable,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_get_group_findings,
            "get_group_findings",
            [group_name],
        ),
        (
            mock_dataloaders_finding_vulnerabilities.load_many_chained,
            "Dataloaders.finding_vulnerabilities",
            [group_name, min_severity, max_severity],
        ),
    ]
    # Set up mocks' results using mock_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mock_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    context = get_new_context()

    assert (
        await get_mean_remediate_non_treated_severity(
            context, group_name, min_severity, max_severity, min_date
        )
        == expected_result
    )

    assert mock_get_group_findings.called is True
    assert (
        mock_dataloaders_finding_vulnerabilities.load_many_chained.called
        is True
    )


@freeze_time("2019-11-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (None, Decimal("183")),
        (30, Decimal("0")),
        (90, Decimal("0")),
    ),
)
@patch(
    MODULE_AT_TEST + "Dataloaders.finding_vulnerabilities",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "get_group_findings", new_callable=AsyncMock)
async def test_get_mean_remediate_non_treated_severity_medium(
    mock_get_group_findings: AsyncMock,
    mock_dataloaders_finding_vulnerabilities: AsyncMock,
    min_days: int | None,
    expected_output: Decimal,
    mock_data_for_module: Callable,
) -> None:
    group_name = "unittesting"
    min_severity = Decimal("4.0")
    max_severity = Decimal("6.9")
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_get_group_findings,
            "get_group_findings",
            [group_name],
        ),
        (
            mock_dataloaders_finding_vulnerabilities.load_many_chained,
            "Dataloaders.finding_vulnerabilities",
            [group_name, min_severity, max_severity],
        ),
    ]
    # Set up mocks' results using mock_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mock_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    loaders = get_new_context()
    medium_severity = await get_mean_remediate_non_treated_severity(
        loaders,
        group_name,
        min_severity,
        max_severity,
        (datetime_utils.get_utc_now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert medium_severity == expected_output

    assert mock_get_group_findings.called is True
    assert (
        mock_dataloaders_finding_vulnerabilities.load_many_chained.called
        is True
    )


@freeze_time("2020-12-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (0, Decimal("238.671")),
        (30, Decimal("0")),
        (90, Decimal("0")),
    ),
)
@patch(
    MODULE_AT_TEST + "Dataloaders.finding_vulnerabilities",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "get_group_findings", new_callable=AsyncMock)
async def test_get_mean_remediate_non_treated_cvssf(
    mock_get_group_findings: AsyncMock,
    mock_dataloaders_finding_vulnerabilities: AsyncMock,
    min_days: int,
    expected_output: Decimal,
    mock_data_for_module: Callable,
) -> None:
    group_name = "unittesting"
    min_severity = Decimal("0.0")
    max_severity = Decimal("10.0")
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_get_group_findings,
            "get_group_findings",
            [group_name],
        ),
        (
            mock_dataloaders_finding_vulnerabilities.load_many_chained,
            "Dataloaders.finding_vulnerabilities",
            [group_name, min_severity, max_severity],
        ),
    ]
    # Set up mocks' results using mock_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mock_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    loaders = get_new_context()
    mttr_no_treated_cvssf = (
        await get_mean_remediate_non_treated_severity_cvssf(
            loaders,
            group_name,
            min_severity,
            max_severity,
            (datetime_utils.get_utc_now() - timedelta(days=min_days)).date()
            if min_days
            else None,
        )
    )
    assert mttr_no_treated_cvssf == expected_output

    assert mock_get_group_findings.called is True
    assert (
        mock_dataloaders_finding_vulnerabilities.load_many_chained.called
        is True
    )


@freeze_time("2020-12-01")
@pytest.mark.parametrize(
    [
        "group_name",
        "min_severity",
        "max_severity",
        "min_days",
        "expected_output",
    ],
    [
        [
            "unittesting",
            Decimal("0.0"),
            Decimal("10.0"),
            0,
            Decimal("375.797"),
        ],
        ["unittesting", Decimal("0.0"), Decimal("10.0"), 30, Decimal("0")],
        [
            "unittesting",
            Decimal("0.0"),
            Decimal("10.0"),
            90,
            Decimal("83.0"),
        ],
        [
            "unittesting",
            Decimal("0.1"),
            Decimal("3.9"),
            0,
            Decimal("365.252"),
        ],
        [
            "unittesting",
            Decimal("0.1"),
            Decimal("3.9"),
            30,
            Decimal("0.0"),
        ],
        [
            "unittesting",
            Decimal("0.1"),
            Decimal("3.9"),
            90,
            Decimal("83.0"),
        ],
        [
            "unittesting",
            Decimal("4.0"),
            Decimal("6.9"),
            0,
            Decimal("377.003"),
        ],
        [
            "unittesting",
            Decimal("4.0"),
            Decimal("6.9"),
            30,
            Decimal("0"),
        ],
        [
            "unittesting",
            Decimal("4.0"),
            Decimal("6.9"),
            90,
            Decimal("0"),
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "Dataloaders.finding_vulnerabilities",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "get_group_findings", new_callable=AsyncMock)
async def test_get_mean_remediate_cvssf(  # pylint: disable=too-many-arguments
    mock_get_group_findings: AsyncMock,
    mock_dataloaders_finding_vulnerabilities: AsyncMock,
    group_name: str,
    min_severity: Decimal,
    max_severity: Decimal,
    min_days: int,
    expected_output: Decimal,
    mock_data_for_module: Callable,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_get_group_findings,
            "get_group_findings",
            [group_name],
        ),
        (
            mock_dataloaders_finding_vulnerabilities.load_many_chained,
            "Dataloaders.finding_vulnerabilities",
            [group_name, min_severity, max_severity],
        ),
    ]
    # Set up mocks' results using mock_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mock_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    loaders = get_new_context()
    mean_remediate_cvssf = await get_mean_remediate_severity_cvssf(
        loaders,
        group_name,
        min_severity,
        max_severity,
        (datetime_utils.get_utc_now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert mock_get_group_findings.called is True
    assert (
        mock_dataloaders_finding_vulnerabilities.load_many_chained.called
        is True
    )
    assert mean_remediate_cvssf == expected_output


@freeze_time("2019-10-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (None, Decimal("50.557")),
        (30, Decimal("11.534")),
        (90, Decimal("12.149")),
    ),
)
@patch(
    MODULE_AT_TEST + "Dataloaders.finding_vulnerabilities",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "get_group_findings", new_callable=AsyncMock)
async def test_get_mean_remediate_severity_low(
    mock_get_group_findings: AsyncMock,
    mock_dataloaders_finding_vulnerabilities: AsyncMock,
    min_days: int | None,
    expected_output: Decimal,
    mock_data_for_module: Callable,
) -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    min_severity = Decimal("0.1")
    max_severity = Decimal("3.9")
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_get_group_findings,
            "get_group_findings",
            [group_name],
        ),
        (
            mock_dataloaders_finding_vulnerabilities.load_many_chained,
            "Dataloaders.finding_vulnerabilities",
            [group_name, min_severity, max_severity],
        ),
    ]
    # Set up mocks' results using mock_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mock_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    low_severity = await get_mean_remediate_non_treated_severity_cvssf(
        loaders,
        group_name,
        min_severity,
        max_severity,
        (datetime_utils.get_utc_now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert low_severity == expected_output
    assert mock_get_group_findings.called is True
    assert (
        mock_dataloaders_finding_vulnerabilities.load_many_chained.called
        is True
    )


@freeze_time("2020-12-01")
@patch(
    MODULE_AT_TEST + "Dataloaders.finding_vulnerabilities",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "get_group_findings", new_callable=AsyncMock)
async def test_get_mean_remediate_severity(
    mock_get_group_findings: AsyncMock,
    mock_dataloaders_finding_vulnerabilities: AsyncMock,
    mock_data_for_module: Callable,
) -> None:
    group_name = "unittesting"
    min_severity: Decimal = Decimal("0.0")
    max_severity: Decimal = Decimal("10.0")
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_get_group_findings,
            "get_group_findings",
            [group_name],
        ),
        (
            mock_dataloaders_finding_vulnerabilities.load_many_chained,
            "Dataloaders.finding_vulnerabilities",
            [group_name, min_severity, max_severity],
        ),
    ]
    # Set up mocks' results using mock_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mock_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    context = get_new_context()
    assert await get_mean_remediate_severity(
        context, group_name, min_severity, max_severity
    ) == Decimal("385.0")

    min_date = datetime_utils.get_now_minus_delta(days=30).date()
    assert await get_mean_remediate_severity(
        context, group_name, min_severity, max_severity, min_date
    ) == Decimal("0.0")

    min_date = datetime_utils.get_now_minus_delta(days=90).date()
    assert await get_mean_remediate_severity(
        context, group_name, min_severity, max_severity, min_date
    ) == Decimal("83.0")
    assert mock_get_group_findings.called is True
    assert (
        mock_dataloaders_finding_vulnerabilities.load_many_chained.called
        is True
    )


@pytest.mark.parametrize(
    ["group_name", "expected_output"],
    [["unittesting", 5]],
)
@patch(MODULE_AT_TEST + "findings_domain.get_status", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "get_group_findings", new_callable=AsyncMock)
async def test_get_open_findings(
    mock_get_group_findings: AsyncMock,
    mock_findings_domain_get_status: AsyncMock,
    group_name: str,
    expected_output: int,
    mock_data_for_module: Callable,
) -> None:
    # Set up mock's result using mock_data_for_module fixture
    mock_get_group_findings.return_value = mock_data_for_module(
        mock_path="get_group_findings",
        mock_args=[group_name],
        module_at_test=MODULE_AT_TEST,
    )

    # Functions inside collect have to be mocked using side_effect
    # so that the iterations wor
    mock_findings_domain_get_status.side_effect = mock_data_for_module(
        mock_path="findings_domain.get_status",
        mock_args=[group_name],
        module_at_test=MODULE_AT_TEST,
    )
    open_findings = await get_open_findings(get_new_context(), group_name)

    assert open_findings == expected_output
    assert mock_get_group_findings.called is True
    assert mock_findings_domain_get_status.called is True


@pytest.mark.parametrize(
    ["group_name", "expected_output"],
    [["oneshottest", 2]],
)
@patch(
    MODULE_AT_TEST + "Dataloaders.finding_vulnerabilities_released_nzr",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "get_group_findings", new_callable=AsyncMock)
async def test_get_open_vulnerabilities(
    mock_get_group_findings: AsyncMock,
    mock_finding_vulnerabilities_released_nzr: AsyncMock,
    group_name: str,
    expected_output: int,
    mock_data_for_module: Callable,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_get_group_findings,
            "get_group_findings",
            [group_name],
        ),
        (
            mock_finding_vulnerabilities_released_nzr.load_many_chained,
            "Dataloaders.finding_vulnerabilities_released_nzr",
            [group_name],
        ),
    ]
    # Set up mocks' results using mock_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mock_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    open_vulns = await get_open_vulnerabilities(get_new_context(), group_name)
    assert open_vulns == expected_output
    assert mock_get_group_findings.called is True
    assert (
        mock_finding_vulnerabilities_released_nzr.load_many_chained.called
        is True
    )


@pytest.mark.parametrize(
    ["group_name", "expected_output"],
    [
        [
            "unittesting",
            GroupTreatmentSummary(
                accepted=2,
                accepted_undefined=1,
                in_progress=1,
                untreated=25,
            ),
        ]
    ],
)
@patch(
    MODULE_AT_TEST + "Dataloaders.finding_vulnerabilities_released_nzr",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "get_group_findings", new_callable=AsyncMock)
async def test_get_treatment_summary(
    mock_get_group_findings: AsyncMock,
    mock_dataloaders_finding_vulnerabilities_released_nzr: AsyncMock,
    group_name: str,
    expected_output: GroupTreatmentSummary,
    mock_data_for_module: Callable,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_get_group_findings,
            "get_group_findings",
            [group_name],
        ),
        (
            mock_dataloaders_finding_vulnerabilities_released_nzr.load_many_chained,  # noqa: E501 pylint: disable=line-too-long
            "Dataloaders.finding_vulnerabilities_released_nzr",
            [group_name],
        ),
    ]
    # Set up mocks' results using mock_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mock_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    loaders = get_new_context()
    test_data = await get_treatment_summary(loaders, group_name)
    assert test_data == expected_output
    assert mock_get_group_findings.called is True
    assert (
        mock_dataloaders_finding_vulnerabilities_released_nzr.load_many_chained.called  # noqa: E501 pylint: disable=line-too-long
        is True
    )


@pytest.mark.parametrize(
    ["group_name", "expected_output"],
    [["unittesting", 1]],
)
@patch(
    MODULE_AT_TEST + "Dataloaders.finding_vulnerabilities_released_nzr",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "get_group_findings", new_callable=AsyncMock)
async def test_get_vulnerabilities_with_pending_attacks(
    mock_get_group_findings: AsyncMock,
    mock_dataloaders_finding_vulnerabilities_released_nzr: AsyncMock,
    group_name: str,
    expected_output: int,
    mock_data_for_module: Callable,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_get_group_findings,
            "get_group_findings",
            [group_name],
        ),
        (
            mock_dataloaders_finding_vulnerabilities_released_nzr.load_many_chained,  # noqa: E501 pylint: disable=line-too-long
            "Dataloaders.finding_vulnerabilities_released_nzr",
            [group_name],
        ),
    ]
    # Set up mocks' results using mock_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mock_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    context = get_new_context()
    test_data = await get_vulnerabilities_with_pending_attacks(
        loaders=context, group_name=group_name
    )
    assert test_data == expected_output
    assert mock_get_group_findings.called is True
    assert (
        mock_dataloaders_finding_vulnerabilities_released_nzr.load_many_chained.called  # noqa: E501 pylint: disable=line-too-long
        is True
    )


@pytest.mark.parametrize(
    ["group_name", "expected_result"],
    [["unittesting", True], ["nonexistent_group", False]],
)
@patch(
    MODULE_AT_TEST + "Dataloaders.group",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "exists",
    new_callable=AsyncMock,
)
async def test_is_valid(
    mock_exists: AsyncMock,
    mock_dataloaders_group: AsyncMock,
    group_name: str,
    expected_result: str,
    mock_data_for_module: Callable,
) -> None:
    # Set up mock's result using mock_data_for_module fixture
    mock_exists.return_value = mock_data_for_module(
        mock_path="exists",
        mock_args=[group_name],
        module_at_test=MODULE_AT_TEST,
    )
    if expected_result:
        # Set up mock's result using mock_data_for_module fixture
        mock_dataloaders_group.load.return_value = mock_data_for_module(
            mock_path="Dataloaders.group",
            mock_args=[group_name],
            module_at_test=MODULE_AT_TEST,
        )
    loaders: Dataloaders = get_new_context()
    if expected_result:
        assert await is_valid(loaders, group_name)
        assert mock_exists.called is True
        assert mock_dataloaders_group.load.called is True
    else:
        assert not await is_valid(loaders, group_name)
        assert mock_exists.called is True
        assert mock_dataloaders_group.load.called is False


@pytest.mark.parametrize(
    ["group", "user_email"],
    [
        [
            Group(
                created_by="unknown",
                created_date=datetime.fromisoformat(
                    "2018-03-08T00:43:18+00:00"
                ),
                description="Integrates unit test group",
                language=GroupLanguage.EN,
                name="unittesting",
                organization_id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                state=GroupState(
                    has_machine=True,
                    has_squad=True,
                    managed=GroupManaged.NOT_MANAGED,
                    modified_by="unknown",
                    modified_date=datetime.fromisoformat(
                        "2018-03-08T00:43:18+00:00"
                    ),
                    status=GroupStateStatus.ACTIVE,
                    tier=GroupTier.MACHINE,
                    type=GroupSubscriptionType.CONTINUOUS,
                    tags={"test-updates", "test-tag", "test-groups"},
                    comments=None,
                    justification=None,
                    payment_id=None,
                    pending_deletion_date=None,
                    service=GroupService.WHITE,
                ),
                agent_token=None,
                business_id="14441323",
                business_name="Testing Company and Sons",
                context="Group context test",
                disambiguation="Disambiguation test",
                files=[],
                policies=None,
                sprint_duration=2,
                sprint_start_date=datetime.fromisoformat(
                    "2022-08-06T19:28:00+00:00"
                ),
            ),
            "integratesmanager@gmail.com",
        ],
    ],
)
@patch(get_mocked_path("update_state"), new_callable=AsyncMock)
async def test_remove_pending_deletion_date(
    mock_groups_domain_update_state: AsyncMock,
    group: Group,
    user_email: str,
) -> None:
    mock_groups_domain_update_state.return_value = get_mock_response(
        get_mocked_path("update_state"),
        json.dumps([group.name, user_email], default=str),
    )
    await remove_pending_deletion_date(group=group, modified_by=user_email)

    assert mock_groups_domain_update_state.called is True


@pytest.mark.parametrize(
    [
        "group_name",
        "responsible",
        "had_token",
    ],
    [
        [
            "unittesting",
            "integratesmanager@gmail.com",
            True,
        ],
        [
            "unittesting",
            "integratesmanager@gmail.com",
            False,
        ],
    ],
)
@patch(
    get_mocked_path("mailer_utils.get_group_emails_by_notification"),
    new_callable=AsyncMock,
)
@patch(
    get_mocked_path("groups_mail.send_mail_devsecops_agent_token"),
    new_callable=AsyncMock,
)
async def test_send_mail_devsecops_agent(
    mock_mailer_utils_get_group_emails_by_notification: AsyncMock,
    mock_groups_mail_send_mail_devsecops_agent_token: AsyncMock,
    group_name: str,
    responsible: str,
    had_token: bool,
) -> None:
    mocks_args: list[list[Any]]
    mocked_objects, mocked_paths, mocks_args = [
        [
            mock_mailer_utils_get_group_emails_by_notification,
            mock_groups_mail_send_mail_devsecops_agent_token,
        ],
        [
            "mailer_utils.get_group_emails_by_notification",
            "groups_mail.send_mail_devsecops_agent_token",
        ],
        [
            [group_name, "devsecops_agent"],
            [responsible, group_name, had_token],
        ],
    ]

    assert set_mocks_return_values(
        mocked_objects=mocked_objects,
        paths_list=mocked_paths,
        mocks_args=mocks_args,
    )
    await send_mail_devsecops_agent(
        loaders=get_new_context(),
        group_name=group_name,
        responsible=responsible,
        had_token=had_token,
    )
    assert all(mock_object.called is True for mock_object in mocked_objects)


@pytest.mark.parametrize(
    ["group", "user_email", "pending_deletion_date"],
    [
        [
            Group(
                created_by="unknown",
                created_date=datetime.fromisoformat(
                    "2018-03-08T00:43:18+00:00"
                ),
                description="Integrates unit test group",
                language=GroupLanguage.EN,
                name="unittesting",
                organization_id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                state=GroupState(
                    has_machine=True,
                    has_squad=True,
                    managed=GroupManaged.NOT_MANAGED,
                    modified_by="unknown",
                    modified_date=datetime.fromisoformat(
                        "2018-03-08T00:43:18+00:00"
                    ),
                    status=GroupStateStatus.ACTIVE,
                    tier=GroupTier.MACHINE,
                    type=GroupSubscriptionType.CONTINUOUS,
                    tags={"test-updates", "test-tag", "test-groups"},
                    comments=None,
                    justification=None,
                    payment_id=None,
                    pending_deletion_date=None,
                    service=GroupService.WHITE,
                ),
                agent_token=None,
                business_id="14441323",
                business_name="Testing Company and Sons",
                context="Group context test",
                disambiguation="Disambiguation test",
                files=[],
                policies=None,
                sprint_duration=2,
                sprint_start_date=datetime.fromisoformat(
                    "2022-08-06T19:28:00+00:00"
                ),
            ),
            "integratesmanager@gmail.com",
            datetime.fromisoformat("2022-04-06T16:46:23+00:00"),
        ],
    ],
)
@patch(get_mocked_path("update_state"), new_callable=AsyncMock)
async def test_set_pending_deletion_date(
    mock_groups_domain_update_state: AsyncMock,
    group: Group,
    user_email: str,
    pending_deletion_date: datetime,
) -> None:
    mock_groups_domain_update_state.return_value = get_mock_response(
        get_mocked_path("update_state"),
        json.dumps(
            [
                group.name,
                group.organization_id,
                user_email,
                pending_deletion_date,
            ],
            default=str,
        ),
    )
    await set_pending_deletion_date(
        group=group,
        modified_by=user_email,
        pending_deletion_date=pending_deletion_date,
    )

    assert mock_groups_domain_update_state.called is True


@pytest.mark.parametrize(
    ["group_name", "tags", "tags_to_raise_exception"],
    [
        [
            "unittesting",
            ["testtag", "this-is-ok", "th15-4l50"],
            ["same-name", "same-name", "another-one"],
        ],
        [
            "unittesting",
            ["this-tag-is-valid", "but this is not"],
            ["test-groups"],
        ],
    ],
)
@patch(MODULE_AT_TEST + "_has_repeated_tags")
async def test_validate_group_tags(
    mock__has_repeated_tags: AsyncMock,
    group_name: str,
    tags: list,
    tags_to_raise_exception: list,
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[group_name, tags]],
        mocked_objects=[mock__has_repeated_tags],
        module_at_test=MODULE_AT_TEST,
        paths_list=["_has_repeated_tags"],
    )
    loaders: Dataloaders = get_new_context()
    result = await validate_group_tags(loaders, group_name, tags)
    assert isinstance(result, list)
    assert mock__has_repeated_tags.called is True

    assert set_mocks_return_values(
        mocks_args=[[group_name, tags_to_raise_exception]],
        mocked_objects=[mock__has_repeated_tags],
        module_at_test=MODULE_AT_TEST,
        paths_list=["_has_repeated_tags"],
    )
    with pytest.raises(RepeatedValues):
        await validate_group_tags(loaders, group_name, tags_to_raise_exception)
    assert mock__has_repeated_tags.call_count == 2


@freeze_time("2019-10-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (None, Decimal("11")),
        (30, Decimal("1")),
        (90, Decimal("2")),
    ),
)
@patch(
    MODULE_AT_TEST + "Dataloaders.finding_vulnerabilities",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "get_group_findings", new_callable=AsyncMock)
async def test_get_mean_remediate_severity_low_min_days(
    mock_get_group_findings: AsyncMock,
    mock_dataloaders_finding_vulnerabilities: AsyncMock,
    min_days: int | None,
    expected_output: Decimal,
    mock_data_for_module: Callable,
) -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    min_severity = Decimal("0.1")
    max_severity = Decimal("3.9")
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_get_group_findings,
            "get_group_findings",
            [group_name],
        ),
        (
            mock_dataloaders_finding_vulnerabilities.load_many_chained,
            "Dataloaders.finding_vulnerabilities",
            [group_name, min_severity, max_severity],
        ),
    ]
    # Set up mocks' results using mock_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mock_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    mean_remediate_low_severity = await get_mean_remediate_severity(
        loaders,
        group_name,
        min_severity,
        max_severity,
        (datetime_utils.get_utc_now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert mean_remediate_low_severity == expected_output
    assert mock_get_group_findings.called is True
    assert (
        mock_dataloaders_finding_vulnerabilities.load_many_chained.called
        is True
    )


@freeze_time("2019-11-01")
@pytest.mark.parametrize(
    ("min_days", "expected_output"),
    (
        (None, Decimal("186")),
        (30, Decimal("0")),
        (90, Decimal("0")),
    ),
)
@patch(
    MODULE_AT_TEST + "Dataloaders.finding_vulnerabilities",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "get_group_findings", new_callable=AsyncMock)
async def test_get_mean_remediate_severity_medium(
    mock_get_group_findings: AsyncMock,
    mock_dataloaders_finding_vulnerabilities: AsyncMock,
    min_days: int | None,
    expected_output: Decimal,
    mock_data_for_module: Callable,
) -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    min_severity = Decimal("4.0")
    max_severity = Decimal("6.9")
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_get_group_findings,
            "get_group_findings",
            [group_name],
        ),
        (
            mock_dataloaders_finding_vulnerabilities.load_many_chained,
            "Dataloaders.finding_vulnerabilities",
            [group_name, min_severity, max_severity],
        ),
    ]
    # Set up mocks' results using mock_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mock_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    mean_remediate_medium_severity = await get_mean_remediate_severity(
        loaders,
        group_name,
        min_severity,
        max_severity,
        (datetime_utils.get_utc_now() - timedelta(days=min_days)).date()
        if min_days
        else None,
    )
    assert mean_remediate_medium_severity == expected_output
    assert mock_get_group_findings.called is True
    assert (
        mock_dataloaders_finding_vulnerabilities.load_many_chained.called
        is True
    )


@pytest.mark.parametrize(
    ["has_machine", "has_squad", "has_arm"],
    [
        [
            True,
            True,
            True,
        ],
    ],
)
def test_validate_group_services_config(
    has_machine: bool,
    has_squad: bool,
    has_arm: bool,
) -> None:
    validate_group_services_config(has_machine, has_squad, has_arm)

    with pytest.raises(
        InvalidGroupServicesConfig
    ) as invalid_group_service_asm:
        validate_group_services_config(
            has_machine=True, has_squad=True, has_arm=False
        )
    assert (
        str(invalid_group_service_asm.value)
        == "Exception - Squad is only available when ASM is too"
    )

    with pytest.raises(
        InvalidGroupServicesConfig
    ) as invalid_group_service_machine:
        validate_group_services_config(
            has_machine=False, has_squad=True, has_arm=True
        )
    assert (
        str(invalid_group_service_machine.value)
        == "Exception - Squad is only available when Machine is too"
    )


def test_validate_group_services_config_deco() -> None:
    @validate_group_services_config_deco(
        has_machine_field="has_machine",
        has_squad_field="has_squad",
        has_arm_field="has_arm",
    )
    def decorated_func(
        has_machine: bool, has_squad: bool, has_arm: bool
    ) -> str:
        return str(has_machine and has_squad and has_arm)

    assert decorated_func(has_machine=True, has_squad=True, has_arm=True)
    assert decorated_func(has_machine=False, has_squad=False, has_arm=False)
    with pytest.raises(
        InvalidGroupServicesConfig
    ) as invalid_group_service_asm:
        decorated_func(has_machine=True, has_squad=True, has_arm=False)
    assert (
        str(invalid_group_service_asm.value)
        == "Exception - Squad is only available when ASM is too"
    )
    with pytest.raises(
        InvalidGroupServicesConfig
    ) as invalid_group_service_machine:
        decorated_func(has_machine=False, has_squad=True, has_arm=True)
    assert (
        str(invalid_group_service_machine.value)
        == "Exception - Squad is only available when Machine is too"
    )
