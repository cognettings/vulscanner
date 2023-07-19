from back.test.unit.src.utils import (
    get_module_at_test,
)
from collections.abc import (
    Iterable,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateStatus,
    VulnerabilityToolImpact,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTool,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
    VulnerabilityVerification,
)
from decimal import (
    Decimal,
)
import pytest
from schedulers.update_indicators import (
    create_data_format_chart,
    create_register_by_week,
    create_weekly_date,
    get_accepted_vulns,
    get_by_time_range,
    get_date_last_vulns,
    get_first_week_dates,
    get_status_vulns_by_time_range,
    RegisterByTime,
    update_indicators,
)
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


def test_create_data_format_chart() -> None:
    registers = {
        "Sep 24 - 30, 2018": {  # NOSONAR
            "found": Decimal(2),
            "accepted": Decimal(0),
            "closed": Decimal(0),
            "assumed_closed": Decimal(0),
            "opened": Decimal(2),
        },
    }
    test_data = create_data_format_chart(registers)
    expected_output = [
        [{"y": 2, "x": "Sep 24 - 30, 2018"}],
        [{"y": 0, "x": "Sep 24 - 30, 2018"}],
        [{"y": 0, "x": "Sep 24 - 30, 2018"}],
        [{"y": 0, "x": "Sep 24 - 30, 2018"}],
        [{"y": 2, "x": "Sep 24 - 30, 2018"}],
    ]
    assert test_data == expected_output


def test_create_weekly_date() -> None:
    first_date = datetime.fromisoformat("2019-09-19T13:23:32+00:00")
    test_data = create_weekly_date(first_date)
    expected_output = "Sep 16 - 22, 2019"
    assert test_data == expected_output


@pytest.mark.parametrize(
    ["group_name"],
    [["unittesting"]],
)
@patch(MODULE_AT_TEST + "_get_vulnerability_data", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "Dataloaders.finding_vulnerabilities_released_nzr",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "Dataloaders.group_findings",
    new_callable=AsyncMock,
)
async def test_create_register_by_week(
    mock_loaders_group_findings: AsyncMock,
    mock_dataloaders_finding_vulnerabilities_released_nzr: AsyncMock,
    mock__get_vulnerability_data: AsyncMock,
    mocked_data_for_module: Any,
    group_name: str,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_loaders_group_findings.load,
            "Dataloaders.group_findings",
            [group_name],
        ),
        (
            mock_dataloaders_finding_vulnerabilities_released_nzr.load_many_chained,  # noqa: E501 pylint: disable=line-too-long
            "Dataloaders.finding_vulnerabilities_released_nzr",
            [group_name],
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
    # Functions inside collect have to be mocked using side_effect
    mock__get_vulnerability_data.side_effect = mocked_data_for_module(
        mock_path="_get_vulnerability_data",
        mock_args=[group_name],
        module_at_test=MODULE_AT_TEST,
    )
    loaders = get_new_context()
    result = await create_register_by_week(loaders, group_name)
    assert isinstance(result, RegisterByTime)
    assert isinstance(result.vulnerabilities, list)
    for item in result.vulnerabilities:
        assert isinstance(item, list)
        assert isinstance(item[0], dict)
        assert item[0] is not None
    assert mock_loaders_group_findings.load.called is True
    assert (
        mock_dataloaders_finding_vulnerabilities_released_nzr.load_many_chained.called  # noqa: E501 pylint: disable=line-too-long
        is True
    )
    assert mock__get_vulnerability_data.call_count == 36


@pytest.mark.parametrize(
    ["historic_state", "historic_treatment", "severity", "expected_result"],
    [
        [
            [
                VulnerabilityState(
                    modified_by="unittest@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-01-03T17:46:10+00:00"
                    ),
                    source=Source.ASM,
                    specific="12",
                    status=VulnerabilityStateStatus.VULNERABLE,
                    where="test/data/lib_path/f060/csharp.cs",
                    commit=None,
                    reasons=None,
                    other_reason=None,
                    tool=VulnerabilityTool(
                        name="tool-2", impact=VulnerabilityToolImpact.INDIRECT
                    ),
                    snippet=None,
                )
            ],
            [
                VulnerabilityTreatment(
                    modified_date=datetime.fromisoformat(
                        "2020-01-03T17:46:10+00:00"
                    ),
                    status=VulnerabilityTreatmentStatus.IN_PROGRESS,
                    acceptance_status=None,
                    accepted_until=None,
                    justification="test justification",
                    assigned="integratesuser2@gmail.com",
                    modified_by="integratesuser@gmail.com",
                )
            ],
            Decimal("2.9"),
            0,
        ],
        [
            [
                VulnerabilityState(
                    modified_by="unittest@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2019-09-13T13:17:41+00:00"
                    ),
                    source=Source.ASM,
                    specific="333",
                    status=VulnerabilityStateStatus.VULNERABLE,
                    where="192.168.100.101",
                    commit=None,
                    reasons=None,
                    other_reason=None,
                    tool=VulnerabilityTool(
                        name="tool-2", impact=VulnerabilityToolImpact.INDIRECT
                    ),
                    snippet=None,
                )
            ],
            [
                VulnerabilityTreatment(
                    modified_date=datetime.fromisoformat(
                        "2019-09-13T13:17:41+00:00"
                    ),
                    status=VulnerabilityTreatmentStatus.UNTREATED,
                    acceptance_status=None,
                    accepted_until=None,
                    justification=None,
                    assigned=None,
                    modified_by=None,
                )
            ],
            Decimal("2.6"),
            0,
        ],
        [
            [
                VulnerabilityState(
                    modified_by="unittest@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2019-04-08T00:45:15+00:00"
                    ),
                    source=Source.ASM,
                    specific="8888",
                    status=VulnerabilityStateStatus.VULNERABLE,
                    where="192.168.1.19",
                    commit=None,
                    reasons=None,
                    other_reason=None,
                    tool=VulnerabilityTool(
                        name="tool-1", impact=VulnerabilityToolImpact.INDIRECT
                    ),
                    snippet=None,
                )
            ],
            [
                VulnerabilityTreatment(
                    modified_date=datetime.fromisoformat(
                        "2019-04-08T00:59:06+00:00"
                    ),
                    status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
                    acceptance_status=VulnerabilityAcceptanceStatus.SUBMITTED,
                    accepted_until=None,
                    justification="test justification permanently accepted",
                    assigned="integratesuser2@gmail.com",
                    modified_by="integratesuser@gmail.com",
                )
            ],
            Decimal("6.3"),
            1,
        ],
    ],
)
async def test_get_accepted_vulns(
    historic_state: list[VulnerabilityState],
    historic_treatment: list[VulnerabilityTreatment],
    severity: Decimal,
    expected_result: int,
) -> None:
    result = get_accepted_vulns(
        tuple(historic_state),
        tuple(historic_treatment),
        severity,
        datetime.fromisoformat("2019-06-30T23:59:59+00:00"),
    ).vulnerabilities
    assert result == expected_result


@pytest.mark.parametrize(
    ["historic_state", "status", "severity", "last_day"],
    [
        [
            tuple(
                [
                    VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T13:17:41+00:00"
                        ),
                        source=Source.ASM,
                        specific="333",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.101",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-2",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    )
                ]
            ),
            VulnerabilityStateStatus.VULNERABLE,
            Decimal("2.6"),
            datetime.fromisoformat("2020-09-09T23:59:59+00:00"),
        ]
    ],
)
async def test_get_by_time_range(
    historic_state: tuple[VulnerabilityState, ...],
    status: VulnerabilityStateStatus,
    severity: Decimal,
    last_day: datetime,
) -> None:
    test_data = get_by_time_range(
        historic_state,
        status,
        severity,
        last_day,
    )
    expected_output = (1, Decimal("0.144"))
    assert test_data == expected_output


@pytest.mark.parametrize(
    ["vulns"],
    [
        [
            [
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2020-01-03T17:46:10+00:00"
                    ),
                    finding_id="422286126",
                    group_name="unittesting",
                    organization_name="okada",
                    hacker_email="unittest@fluidattacks.com",
                    id="0a848781-b6a4-422e-95fa-692151e6a98z",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-01-03T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        specific="12",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="test/data/lib_path/f060/csharp.cs",
                        commit="ea871eee64cfd5ce293411efaf4d3b446d04eb4a",
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-2",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-01-03T17:46:10+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.IN_PROGRESS,
                        acceptance_status=None,
                        accepted_until=None,
                        justification="test justification",
                        assigned="integratesuser2@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_report_date=datetime.fromisoformat(
                            "2020-01-03T17:46:10+00:00"
                        ),
                        unreliable_treatment_changes=1,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
            ],
        ]
    ],
)
async def test_get_date_last_vulns(
    vulns: Iterable[Vulnerability],
) -> None:
    result = get_date_last_vulns(vulns)
    expected_output = datetime.fromisoformat("2019-12-30T17:46:10+00:00")
    assert result == expected_output


@pytest.mark.parametrize(
    ["vulns"],
    [
        [
            [
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2020-01-03T17:46:10+00:00"
                    ),
                    finding_id="422286126",
                    group_name="unittesting",
                    organization_name="okada",
                    hacker_email="unittest@fluidattacks.com",
                    id="0a848781-b6a4-422e-95fa-692151e6a98z",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-01-03T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        specific="12",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="test/data/lib_path/f060/csharp.cs",
                        commit="ea871eee64cfd5ce293411efaf4d3b446d04eb4a",
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-2",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-01-03T17:46:10+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.IN_PROGRESS,
                        acceptance_status=None,
                        accepted_until=None,
                        justification="test justification",
                        assigned="integratesuser2@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_report_date=datetime.fromisoformat(
                            "2020-01-03T17:46:10+00:00"
                        ),
                        unreliable_treatment_changes=1,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
            ],
        ]
    ],
)
async def test_get_first_week_dates(
    vulns: Iterable[Vulnerability],
) -> None:
    test_data = get_first_week_dates(vulns)
    expected_output = (
        datetime.fromisoformat("2019-12-30T00:00:00+00:00"),
        datetime.fromisoformat("2020-01-05T23:59:59+00:00"),
    )
    assert test_data == expected_output


@pytest.mark.parametrize(
    [
        "vulnerabilities",
        "vulnerabilities_severity",
        "vulnerabilities_historic_states",
        "vulnerabilities_historic_treatments",
        "first_day",
        "last_day",
    ],
    [
        [
            tuple(
                [
                    Vulnerability(
                        created_by="unittest@fluidattacks.com",
                        created_date=datetime.fromisoformat(
                            "2020-01-03T17:46:10+00:00"
                        ),
                        finding_id="422286126",
                        group_name="unittesting",
                        organization_name="okada",
                        hacker_email="unittest@fluidattacks.com",
                        id="0a848781-b6a4-422e-95fa-692151e6a98z",
                        state=VulnerabilityState(
                            modified_by="unittest@fluidattacks.com",
                            modified_date=datetime.fromisoformat(
                                "2020-01-03T17:46:10+00:00"
                            ),
                            source=Source.ASM,
                            specific="12",
                            status=VulnerabilityStateStatus.VULNERABLE,
                            where="test/data/lib_path/f060/csharp.cs",
                            commit="ea871eee64cfd5ce293411efaf4d3b446d04eb4a",
                            reasons=None,
                            other_reason=None,
                            tool=VulnerabilityTool(
                                name="tool-2",
                                impact=VulnerabilityToolImpact.INDIRECT,
                            ),
                            snippet=None,
                        ),
                        type=VulnerabilityType.LINES,
                        bug_tracking_system_url=None,
                        custom_severity=None,
                        developer=None,
                        event_id=None,
                        hash=None,
                        root_id=None,
                        skims_method=None,
                        skims_technique=None,
                        stream=None,
                        tags=None,
                        treatment=VulnerabilityTreatment(
                            modified_date=datetime.fromisoformat(
                                "2020-01-03T17:46:10+00:00"
                            ),
                            status=VulnerabilityTreatmentStatus.IN_PROGRESS,
                            acceptance_status=None,
                            accepted_until=None,
                            justification="test justification",
                            assigned="integratesuser2@gmail.com",
                            modified_by="integratesuser@gmail.com",
                        ),
                        unreliable_indicators=VulnerabilityUnreliableIndicators(  # noqa: E501 pylint: disable=line-too-long
                            unreliable_closing_date=None,
                            unreliable_source=Source.ASM,
                            unreliable_efficacy=Decimal("0"),
                            unreliable_last_reattack_date=None,
                            unreliable_last_reattack_requester=None,
                            unreliable_last_requested_reattack_date=None,
                            unreliable_reattack_cycles=0,
                            unreliable_report_date=datetime.fromisoformat(
                                "2020-01-03T17:46:10+00:00"
                            ),
                            unreliable_treatment_changes=1,
                        ),
                        verification=None,
                        zero_risk=None,
                    ),
                    Vulnerability(
                        created_by="unittest@fluidattacks.com",
                        created_date=datetime.fromisoformat(
                            "2019-09-13T13:17:41+00:00"
                        ),
                        finding_id="436992569",
                        group_name="unittesting",
                        organization_name="okada",
                        hacker_email="unittest@fluidattacks.com",
                        id="15375781-31f2-4953-ac77-f31134225747",
                        state=VulnerabilityState(
                            modified_by="unittest@fluidattacks.com",
                            modified_date=datetime.fromisoformat(
                                "2019-09-13T13:17:41+00:00"
                            ),
                            source=Source.ASM,
                            specific="333",
                            status=VulnerabilityStateStatus.VULNERABLE,
                            where="192.168.100.101",
                            commit=None,
                            reasons=None,
                            other_reason=None,
                            tool=VulnerabilityTool(
                                name="tool-2",
                                impact=VulnerabilityToolImpact.INDIRECT,
                            ),
                            snippet=None,
                        ),
                        type=VulnerabilityType.PORTS,
                        bug_tracking_system_url=None,
                        custom_severity=None,
                        developer=None,
                        event_id=None,
                        hash=None,
                        root_id=None,
                        skims_method=None,
                        skims_technique=None,
                        stream=None,
                        tags=None,
                        treatment=VulnerabilityTreatment(
                            modified_date=datetime.fromisoformat(
                                "2019-09-13T13:17:41+00:00"
                            ),
                            status=VulnerabilityTreatmentStatus.UNTREATED,
                            acceptance_status=None,
                            accepted_until=None,
                            justification=None,
                            assigned=None,
                            modified_by=None,
                        ),
                        unreliable_indicators=VulnerabilityUnreliableIndicators(  # noqa: E501 pylint: disable=line-too-long
                            unreliable_closing_date=None,
                            unreliable_source=Source.ASM,
                            unreliable_efficacy=Decimal("0"),
                            unreliable_last_reattack_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                                "2020-02-19T15:41:04+00:00"
                            ),
                            unreliable_last_reattack_requester="integratesuser@gmail.com",  # noqa: E501 pylint: disable=line-too-long
                            unreliable_last_requested_reattack_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                                "2020-02-18T15:41:04+00:00"
                            ),
                            unreliable_reattack_cycles=1,
                            unreliable_report_date=datetime.fromisoformat(
                                "2019-09-13T13:17:41+00:00"
                            ),
                            unreliable_treatment_changes=0,
                        ),
                        verification=VulnerabilityVerification(
                            modified_date=datetime.fromisoformat(
                                "2020-02-19T15:41:04+00:00"
                            ),
                            status=VulnerabilityVerificationStatus.VERIFIED,
                            event_id=None,
                        ),
                        zero_risk=None,
                    ),
                    Vulnerability(
                        created_by="unittest@fluidattacks.com",
                        created_date=datetime.fromisoformat(
                            "2019-04-08T00:45:15+00:00"
                        ),
                        finding_id="988493279",
                        group_name="unittesting",
                        organization_name="okada",
                        hacker_email="unittest@fluidattacks.com",
                        id="47ce0fb0-4108-49b0-93cc-160dce8168a6",
                        state=VulnerabilityState(
                            modified_by="unittest@fluidattacks.com",
                            modified_date=datetime.fromisoformat(
                                "2019-04-08T00:45:15+00:00"
                            ),
                            source=Source.ASM,
                            specific="8888",
                            status=VulnerabilityStateStatus.VULNERABLE,
                            where="192.168.1.19",
                            commit=None,
                            reasons=None,
                            other_reason=None,
                            tool=VulnerabilityTool(
                                name="tool-1",
                                impact=VulnerabilityToolImpact.INDIRECT,
                            ),
                            snippet=None,
                        ),
                        type=VulnerabilityType.PORTS,
                        bug_tracking_system_url=None,
                        custom_severity=None,
                        developer=None,
                        event_id=None,
                        hash=None,
                        root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                        skims_method=None,
                        skims_technique=None,
                        stream=None,
                        tags=None,
                        treatment=VulnerabilityTreatment(
                            modified_date=datetime.fromisoformat(
                                "2020-10-08T00:59:06+00:00"
                            ),
                            status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,  # noqa: E501 pylint: disable=line-too-long
                            acceptance_status=VulnerabilityAcceptanceStatus.APPROVED,  # noqa: E501 pylint: disable=line-too-long
                            accepted_until=None,
                            justification="Observations about permanently accepted",  # noqa: E501 pylint: disable=line-too-long
                            assigned="integratesuser@gmail.com",
                            modified_by="integratesuser@gmail.com",
                        ),
                        unreliable_indicators=VulnerabilityUnreliableIndicators(  # noqa: E501 pylint: disable=line-too-long
                            unreliable_closing_date=None,
                            unreliable_source=Source.ASM,
                            unreliable_efficacy=Decimal("0"),
                            unreliable_last_reattack_date=None,
                            unreliable_last_reattack_requester=None,
                            unreliable_last_requested_reattack_date=None,
                            unreliable_reattack_cycles=0,
                            unreliable_report_date=datetime.fromisoformat(
                                "2019-04-08T00:45:15+00:00"
                            ),
                            unreliable_treatment_changes=2,
                        ),
                        verification=None,
                        zero_risk=None,
                    ),
                ]
            ),
            [Decimal("2.9"), Decimal("2.6"), Decimal("6.3")],
            (
                (
                    VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-01-03T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        specific="12",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="test/data/lib_path/f060/csharp.cs",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-2",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                ),
                (
                    VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T13:17:41+00:00"
                        ),
                        source=Source.ASM,
                        specific="333",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.101",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-2",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                ),
                (
                    VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        specific="8888",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.19",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-1",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                ),
            ),
            (
                (
                    VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-01-03T17:46:10+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.IN_PROGRESS,
                        acceptance_status=None,
                        accepted_until=None,
                        justification="test justification",
                        assigned="integratesuser2@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                ),
                (
                    VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T13:17:41+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                ),
                (
                    VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T00:59:06+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
                        acceptance_status=VulnerabilityAcceptanceStatus.SUBMITTED,  # noqa: E501 pylint: disable=line-too-long
                        accepted_until=None,
                        justification="test justification permanently accepted",  # noqa: E501 pylint: disable=line-too-long
                        assigned="integratesuser2@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                ),
            ),
            datetime.fromisoformat("2019-06-01T12:00:00+00:00"),
            datetime.fromisoformat("2020-02-28T23:59:59+00:00"),
        ]
    ],
)
async def test_get_status_vulns_by_time_range(
    # pylint: disable=too-many-arguments
    vulnerabilities: tuple[Vulnerability, ...],
    vulnerabilities_severity: list[Decimal],
    vulnerabilities_historic_states: tuple[
        tuple[VulnerabilityState, ...], ...
    ],
    vulnerabilities_historic_treatments: tuple[
        tuple[VulnerabilityTreatment, ...], ...
    ],
    first_day: datetime,
    last_day: datetime,
) -> None:
    test_data = get_status_vulns_by_time_range(
        vulnerabilities=vulnerabilities,
        vulnerabilities_severity=vulnerabilities_severity,
        vulnerabilities_historic_states=vulnerabilities_historic_states,
        vulnerabilities_historic_treatments=vulnerabilities_historic_treatments,  # noqa: E501 pylint: disable=line-too-long
        first_day=first_day,
        last_day=last_day,
    )

    expected_output = {"found": 2, "accepted": 1, "closed": 0, "opened": 2}
    output = {
        "found": test_data.found_vulnerabilities,
        "accepted": test_data.accepted_vulnerabilities,
        "closed": test_data.closed_vulnerabilities,
        "opened": test_data.open_vulnerabilities,
    }
    expected_output_cvssf = {
        "found": Decimal("0.362"),
        "accepted": Decimal("24.251"),
        "closed": Decimal("0"),
        "opened": Decimal("0.362"),
    }
    output_cvssf = {
        "found": test_data.found_cvssf,
        "accepted": test_data.accepted_cvssf,
        "closed": test_data.closed_cvssf,
        "opened": test_data.open_cvssf,
    }
    assert sorted(output.items()) == sorted(expected_output.items())
    assert sorted(output_cvssf.items()) == sorted(
        expected_output_cvssf.items()
    )


@patch(MODULE_AT_TEST + "update_group_indicators", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "orgs_domain.get_all_active_groups",
    new_callable=AsyncMock,
)
async def test_update_group_indicators(
    mock_orgs_domain_get_all_active_groups: AsyncMock,
    mock_update_group_indicators: AsyncMock,
    mocked_data_for_module: Any,
) -> None:
    # Set up mocks' results using mocked_data_for_module fixture
    mock_orgs_domain_get_all_active_groups.return_value = (
        mocked_data_for_module(
            mock_path="orgs_domain.get_all_active_groups",
            mock_args=[],
            module_at_test=MODULE_AT_TEST,
        )
    )
    # Functions inside collect have to be mocked using side_effect
    # so that the iterations work
    mock_update_group_indicators.side_effect = mocked_data_for_module(
        mock_path="update_group_indicators",
        mock_args=[],
        module_at_test=MODULE_AT_TEST,
    )
    await update_indicators()
    assert mock_orgs_domain_get_all_active_groups.called is True
    assert mock_update_group_indicators.call_count == 13
