from back.test.unit.src.utils import (
    create_dummy_info,
    create_dummy_session,
    get_mock_response,
    get_mocked_path,
    get_module_at_test,
)
from collections.abc import (
    Callable,
    Iterable,
)
from custom_exceptions import (
    FindingNotFound,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingCommentsRequest,
)
from db_model.findings.enums import (
    FindingSorts,
    FindingStateStatus,
    FindingStatus,
)
from db_model.findings.types import (
    CVSS31Severity,
    Finding,
    FindingEvidence,
    FindingEvidences,
    FindingState,
    FindingTreatmentSummary,
    FindingUnreliableIndicators,
    FindingVerificationSummary,
)
from db_model.types import (
    SeverityScore,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    VulnerabilityState,
    VulnerabilityTreatment,
)
from decimal import (
    Decimal,
)
from findings.domain import (
    get_last_closed_vulnerability_info,
    get_max_open_severity,
    get_oldest_no_treatment,
    get_pending_verification_findings,
    get_tracking_vulnerabilities,
    get_treatment_summary,
    has_access_to_finding,
    mask_finding,
    verify_vulnerabilities,
)
from findings.types import (
    Tracking,
)
from freezegun import (
    freeze_time,
)
import json
import pytest
from pytz import (
    timezone,
)
from settings import (
    TIME_ZONE,
)
from typing import (
    Any,
)
from unittest.mock import (
    AsyncMock,
    patch,
)
from vulnerabilities.types import (
    Treatments,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@patch(
    MODULE_AT_TEST + "Dataloaders.finding_vulnerabilities_released_nzr",
    new_callable=AsyncMock,
)
@pytest.mark.parametrize(
    ["findings"],
    [
        [["463558592", "422286126"]],
    ],
)
async def test_get_last_closed_vulnerability(
    mock_dataloaders_finding_vulnerabilities_released_nzr: AsyncMock,
    findings: list,
    findings_data: dict[str, tuple[Finding, ...]],
    mock_data_for_module: Any,
) -> None:
    # Set up mock's return_value using mock_data_for_module fixture
    mock_dataloaders_finding_vulnerabilities_released_nzr.load_many_chained.return_value = mock_data_for_module(  # noqa: E501 pylint: disable=line-too-long
        mock_path="Dataloaders.finding_vulnerabilities_released_nzr",
        mock_args=[findings],
        module_at_test=MODULE_AT_TEST,
    )
    findings_as_keys = json.dumps(findings)
    findings_loader = findings_data[findings_as_keys]
    loaders = get_new_context()
    (
        vuln_closed_days,
        last_closed_vuln,
    ) = await get_last_closed_vulnerability_info(loaders, findings_loader)
    tzn = timezone(TIME_ZONE)
    actual_date = datetime.now(tz=tzn).date()
    initial_date = datetime(2019, 1, 15).date()
    assert vuln_closed_days == (actual_date - initial_date).days
    expected_id = "242f848c-148a-4028-8e36-c7d995502590"
    assert last_closed_vuln
    assert last_closed_vuln.id == expected_id
    assert last_closed_vuln.finding_id == "463558592"
    assert (
        mock_dataloaders_finding_vulnerabilities_released_nzr.load_many_chained.called  # noqa: E501 pylint: disable=line-too-long
        is True
    )


@patch(get_mocked_path("get_open_vulnerabilities_len"), new_callable=AsyncMock)
@pytest.mark.parametrize(
    ["findings"],
    [
        [["463558592", "422286126"]],
    ],
)
async def test_get_max_open_severity(
    mock_get_open_vulnerabilities_len: AsyncMock,
    findings: list,
    findings_data: dict[str, tuple[Finding, ...]],
) -> None:
    findings_as_keys = json.dumps(findings)
    findings_loader = findings_data[findings_as_keys]
    loaders = get_new_context()
    mock_get_open_vulnerabilities_len.return_value = get_mock_response(
        get_mocked_path("get_open_vulnerabilities_len"), findings_as_keys
    )
    test_data = await get_max_open_severity(loaders, findings_loader)
    assert test_data[0] == Decimal(4.3).quantize(Decimal("0.1"))
    result_finding = test_data[1]
    assert result_finding
    assert result_finding.id == "463558592"


@pytest.mark.parametrize(
    ["group_name"],
    [
        ["unittesting"],
    ],
)
@patch(
    MODULE_AT_TEST + "_is_pending_verification",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "findings_utils.get_group_findings",
    new_callable=AsyncMock,
)
async def test_get_pending_verification_findings(
    mock_findings_utils_get_group_findings: AsyncMock,
    mock__is_pending_verification: AsyncMock,
    group_name: str,
    mock_data_for_module: Any,
) -> None:
    # Set up mock's result using mocked_data_for_module fixture
    mock_findings_utils_get_group_findings.return_value = mock_data_for_module(
        mock_path="findings_utils.get_group_findings",
        mock_args=[group_name],
        module_at_test=MODULE_AT_TEST,
    )

    # Functions inside collect have to be mocked using side_effect
    # so that the iterations work
    mock__is_pending_verification.side_effect = mock_data_for_module(
        mock_path="_is_pending_verification",
        mock_args=[group_name],
        module_at_test=MODULE_AT_TEST,
    )
    loaders = get_new_context()
    findings: list[Finding] = await get_pending_verification_findings(
        loaders, group_name
    )
    assert len(findings) >= 1
    assert findings[0].title == "038. Business information leak"
    assert findings[0].id == "436992569"
    assert findings[0].group_name == "unittesting"
    assert mock_findings_utils_get_group_findings.called is True
    assert mock__is_pending_verification.call_count == 6


@pytest.mark.parametrize(
    ["vulns_state", "vulns_treatment"],
    [
        [
            [
                [
                    VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T14:58:38+00:00"
                        ),
                        source=Source.ASM,
                        specific="3636",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.105",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    )
                ],
                [
                    VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="7777",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.18",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    )
                ],
            ],
            [
                [
                    VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T14:58:38+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    )
                ],
                [
                    VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.IN_PROGRESS,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by="integratesuser@gmail.com",
                    ),
                    VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        acceptance_status=None,
                        accepted_until=datetime.fromisoformat(
                            "2021-01-16T17:46:10+00:00"
                        ),
                        justification="accepted justification",
                        assigned="integratesuser@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                ],
            ],
        ]
    ],
)
async def test_get_tracking_vulnerabilities(
    vulns_state: Iterable[Iterable[VulnerabilityState]],
    vulns_treatment: Iterable[Iterable[VulnerabilityTreatment]],
) -> None:
    test_data = get_tracking_vulnerabilities(
        vulns_state=vulns_state,
        vulns_treatment=vulns_treatment,
    )
    expected_output = [
        Tracking(
            cycle=0,
            open=1,
            closed=0,
            date="2019-09-12",
            accepted=0,
            accepted_undefined=0,
            assigned="",
            justification="",
            safe=0,
            vulnerable=1,
        ),
        Tracking(
            cycle=1,
            open=1,
            closed=0,
            date="2019-09-13",
            accepted=0,
            accepted_undefined=0,
            assigned="",
            justification="",
            safe=0,
            vulnerable=1,
        ),
        Tracking(
            cycle=2,
            open=0,
            closed=0,
            date="2019-09-13",
            accepted=1,
            accepted_undefined=0,
            assigned="integratesuser@gmail.com",
            justification="accepted justification",
            safe=0,
            vulnerable=0,
        ),
    ]
    assert test_data == expected_output


@patch(
    MODULE_AT_TEST + "authz.has_access_to_group",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "Dataloaders.finding",
    new_callable=AsyncMock,
)
@pytest.mark.parametrize(
    ["email", "finding_id"], [["unittest@fluidattacks.com", "422286126"]]
)
async def test_has_access_to_finding(
    mock_dataloaders_finding: AsyncMock,
    mock_authz_has_access_to_group: AsyncMock,
    email: str,
    finding_id: str,
    mock_data_for_module: Callable,
) -> None:
    loaders = get_new_context()
    mock_dataloaders_finding.load.return_value = mock_data_for_module(
        mock_path="Dataloaders.finding",
        mock_args=[finding_id],
        module_at_test=MODULE_AT_TEST,
    )
    mock_authz_has_access_to_group.return_value = mock_data_for_module(
        mock_path="authz.has_access_to_group",
        mock_args=[email, finding_id],
        module_at_test=MODULE_AT_TEST,
    )
    assert await has_access_to_finding(loaders, email, finding_id)
    assert mock_dataloaders_finding.load.called is True
    assert mock_authz_has_access_to_group.called is True


@patch(
    MODULE_AT_TEST + "Dataloaders.finding",
    new_callable=AsyncMock,
)
@pytest.mark.parametrize(
    ["email", "finding_id"], [["unittest@fluidattacks.com", "000000000"]]
)
async def test_has_access_to_finding_exception(
    mock_dataloaders_finding: AsyncMock,
    email: str,
    finding_id: str,
    mock_data_for_module: Callable,
) -> None:
    loaders = get_new_context()
    mock_dataloaders_finding.load.return_value = mock_data_for_module(
        mock_path="Dataloaders.finding",
        mock_args=[finding_id],
        module_at_test=MODULE_AT_TEST,
    )
    with pytest.raises(FindingNotFound):
        await has_access_to_finding(loaders, email, finding_id)
    assert mock_dataloaders_finding.load.called is True


@pytest.mark.parametrize(
    ("email", "finding"),
    (
        (
            "unittest@fluidattacks.com",
            Finding(
                hacker_email="unittest@fluidattacks.com",
                group_name="unittesting",
                id="457497316",
                state=FindingState(
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-11-27T05:00:00+00:00"
                    ),
                    source=Source.ASM,
                    status=FindingStateStatus.APPROVED,
                    rejection=None,
                    justification=StateRemovalJustification.NO_JUSTIFICATION,
                ),
                title="037. Technical information leak",
                attack_vector_description="Test description",
                creation=FindingState(
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-04-08T00:43:18+00:00"
                    ),
                    source=Source.ASM,
                    status=FindingStateStatus.CREATED,
                    rejection=None,
                    justification=StateRemovalJustification.NO_JUSTIFICATION,
                ),
                description="Descripción de fuga de información técnica",
                evidences=FindingEvidences(
                    animation=None,
                    evidence1=None,
                    evidence2=FindingEvidence(
                        description="Test description",
                        modified_date=datetime.fromisoformat(
                            "2018-11-27T05:00:00+00:00"
                        ),
                        url="unittesting-457497316-evidence_route_2.jpg",
                    ),
                    evidence3=FindingEvidence(
                        description="Comentario",
                        modified_date=datetime.fromisoformat(
                            "2018-11-27T05:00:00+00:00"
                        ),
                        url="unittesting-457497316-evidence_route_3.png",
                    ),
                    evidence4=None,
                    evidence5=None,
                    exploitation=None,
                    records=None,
                ),
                min_time_to_remediate=18,
                recommendation=(
                    "Eliminar el banner de los servicios con "
                    "fuga de información, Verificar que los encabezados HTTP "
                    "no expongan ningún nombre o versión."
                ),
                requirements=(
                    "REQ.0077. La aplicación no debe revelar "
                    "detalles del sistema interno como stack traces, "
                    "fragmentos de sentencias SQL y nombres de base de datos "
                    "o tablas. REQ.0176. El sistema debe restringir el acceso "
                    "a objetos del sistema que tengan contenido sensible. "
                    "Sólo permitirá su acceso a usuarios autorizados."
                ),
                severity=CVSS31Severity(
                    attack_complexity=Decimal("0.44"),
                    attack_vector=Decimal("0.62"),
                    availability_impact=Decimal("0.22"),
                    availability_requirement=Decimal("1"),
                    confidentiality_impact=Decimal("0.22"),
                    confidentiality_requirement=Decimal("1"),
                    exploitability=Decimal("0.94"),
                    integrity_impact=Decimal("0.22"),
                    integrity_requirement=Decimal("1"),
                    modified_attack_complexity=Decimal("0.44"),
                    modified_attack_vector=Decimal("0.62"),
                    modified_availability_impact=Decimal("0.22"),
                    modified_confidentiality_impact=Decimal("0.22"),
                    modified_integrity_impact=Decimal("0.22"),
                    modified_privileges_required=Decimal("0.62"),
                    modified_user_interaction=Decimal("0.85"),
                    modified_severity_scope=Decimal("0"),
                    privileges_required=Decimal("0.62"),
                    remediation_level=Decimal("0.96"),
                    report_confidence=Decimal("0.92"),
                    severity_scope=Decimal("0"),
                    user_interaction=Decimal("0.85"),
                ),
                severity_score=SeverityScore(
                    base_score=Decimal("4.6"),
                    temporal_score=Decimal("3.9"),
                    cvss_v3="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:L/E:P/"
                    "RL:T/RC:U/MAV:A/MAC:H/MPR:L/MUI:N/MS:U/MC:L/MI:L/MA:L",
                    cvssf=Decimal("0.871"),
                ),
                sorts=FindingSorts.NO,
                threat="Amenaza.",
                unreliable_indicators=FindingUnreliableIndicators(
                    unreliable_closed_vulnerabilities=1,
                    unreliable_newest_vulnerability_report_date=(
                        datetime.fromisoformat("2018-11-27T19:54:08+00:00")
                    ),
                    unreliable_oldest_open_vulnerability_report_date=(
                        datetime.fromisoformat("2018-11-27T19:54:08+00:00")
                    ),
                    unreliable_oldest_vulnerability_report_date=(
                        datetime.fromisoformat("2018-11-27T19:54:08+00:00")
                    ),
                    unreliable_open_vulnerabilities=0,
                    unreliable_status=FindingStatus.SAFE,
                    unreliable_treatment_summary=FindingTreatmentSummary(
                        accepted=0,
                        accepted_undefined=0,
                        in_progress=0,
                        untreated=0,
                    ),
                    unreliable_verification_summary=FindingVerificationSummary(
                        requested=0, on_hold=0, verified=0
                    ),
                    unreliable_where="",
                ),
                verification=None,
            ),
        ),
    ),
)
@patch(MODULE_AT_TEST + "findings_model.remove", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "vulns_domain.mask_vulnerability", new_callable=AsyncMock
)
@patch(
    MODULE_AT_TEST + "Dataloaders.finding_vulnerabilities_all",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "remove_all_evidences", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "comments_domain.remove_comments", new_callable=AsyncMock
)
async def test_mask_finding(  # pylint: disable=too-many-arguments
    mock_comments_domain_remove_comments: AsyncMock,
    mock_remove_all_evidences: AsyncMock,
    mock_dataloaders_finding_vulnerabilities_all: AsyncMock,
    mock_vulns_domain_mask_vulnerability: AsyncMock,
    mock_findings_model_remove: AsyncMock,
    email: str,
    finding: Finding,
    mock_data_for_module: Callable,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_comments_domain_remove_comments,
            "comments_domain.remove_comments",
            [finding.id],
        ),
        (
            mock_remove_all_evidences,
            "remove_all_evidences",
            [finding.id, finding.group_name],
        ),
        (
            mock_dataloaders_finding_vulnerabilities_all.load,
            "Dataloaders.finding_vulnerabilities_all",
            [finding.id],
        ),
        (
            mock_vulns_domain_mask_vulnerability,
            "vulns_domain.mask_vulnerability",
            [email, finding.id],
        ),
        (
            mock_findings_model_remove,
            "findings_model.remove",
            [finding.group_name, finding.id],
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
    await mask_finding(loaders, finding, email)
    assert mock_comments_domain_remove_comments.called is True
    assert mock_remove_all_evidences.called is True
    assert mock_dataloaders_finding_vulnerabilities_all.load.called is True
    assert mock_vulns_domain_mask_vulnerability.called is True
    assert mock_findings_model_remove.called is True


@pytest.mark.parametrize(
    ["findings"],
    [
        [
            (
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="oneshottest",
                    id="457497318",
                    state=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-11-29T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="037. Technical information leak",
                    attack_vector_description="Descripción",
                    creation=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:43:18+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="This is a description",
                    evidences=FindingEvidences(
                        animation=None,
                        evidence1=FindingEvidence(
                            description="Comentario",
                            modified_date=datetime.fromisoformat(
                                "2018-11-29T05:00:00+00:00"
                            ),
                            url="oneshottest-457497318-evidence_route_1",
                        ),
                        evidence2=FindingEvidence(
                            description="test",
                            modified_date=datetime.fromisoformat(
                                "2018-11-29T05:00:00+00:00"
                            ),
                            url="oneshottest-457497318-evidence_route_2",
                        ),
                        evidence3=FindingEvidence(
                            description="1",
                            modified_date=datetime.fromisoformat(
                                "2018-11-29T05:00:00+00:00"
                            ),
                            url="oneshottest-457497318-evidence_route_3",
                        ),
                        evidence4=None,
                        evidence5=None,
                        exploitation=None,
                        records=None,
                    ),
                    min_time_to_remediate=18,
                    recommendation="This is a recomendation.",
                    requirements="REQ.0077.",
                    severity=CVSS31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.62"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("1"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("1"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_attack_vector=Decimal("0.62"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        modified_integrity_impact=Decimal("0.22"),
                        modified_privileges_required=Decimal("0.62"),
                        modified_user_interaction=Decimal("0.85"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.62"),
                        remediation_level=Decimal("0.96"),
                        report_confidence=Decimal("0.92"),
                        severity_scope=Decimal("0"),
                        user_interaction=Decimal("0.85"),
                    ),
                    severity_score=SeverityScore(
                        base_score=Decimal("4.6"),
                        temporal_score=Decimal("3.9"),
                        cvss_v3="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:L/"
                        "E:P/RL:T/RC:U/MAV:A/MAC:H/MPR:L/MUI:N/MS:U/MC:L/MI:L/"
                        "MA:L",
                        cvssf=Decimal("0.871"),
                    ),
                    sorts=FindingSorts.NO,
                    threat="Amenaza.",
                    unfulfilled_requirements=["077", "176"],
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=0,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-09-12T13:45:48+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-09-12T13:45:48+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-09-12T13:45:48+00:00"
                        ),
                        unreliable_open_vulnerabilities=1,
                        unreliable_status=FindingStatus.VULNERABLE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=0,
                            accepted_undefined=0,
                            in_progress=0,
                            untreated=1,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=0, on_hold=0, verified=0
                        ),
                        unreliable_where="192.168.1.9",
                    ),
                    verification=None,
                ),
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="oneshottest",
                    id="475041513",
                    state=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="081. Lack of multi-factor authentication",
                    attack_vector_description="This is an attack vector.",
                    creation=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:43:18+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="This is a description.",
                    evidences=FindingEvidences(
                        animation=None,
                        evidence1=FindingEvidence(
                            description="Evidencia",
                            modified_date=datetime.fromisoformat(
                                "2018-04-08T00:43:18+00:00"
                            ),
                            url="continuoustesting-475041513-evidence_route_1",
                        ),
                        evidence2=FindingEvidence(
                            description="Test",
                            modified_date=datetime.fromisoformat(
                                "2018-04-08T00:43:18+00:00"
                            ),
                            url="continuoustesting-475041513-evidence_route_2",
                        ),
                        evidence3=None,
                        evidence4=None,
                        evidence5=None,
                        exploitation=None,
                        records=None,
                    ),
                    min_time_to_remediate=18,
                    recommendation="This is a recomendation.",
                    requirements="REQ.0229.",
                    severity=CVSS31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.2"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("0.5"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("0.5"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_attack_vector=Decimal("0.85"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        modified_integrity_impact=Decimal("0"),
                        modified_privileges_required=Decimal("0.27"),
                        modified_user_interaction=Decimal("0.62"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.62"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("1"),
                        severity_scope=Decimal("0"),
                        user_interaction=Decimal("0.85"),
                    ),
                    severity_score=SeverityScore(
                        base_score=Decimal("3.8"),
                        temporal_score=Decimal("3.4"),
                        cvss_v3="CVSS:3.1/AV:P/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:L/"
                        "E:P/RL:O/CR:L/AR:L/MAV:N/MAC:H/MPR:H/MUI:R/MS:U/MC:L/"
                        "MA:L",
                        cvssf=Decimal("0.435"),
                    ),
                    sorts=FindingSorts.NO,
                    threat="This is a threat.",
                    unfulfilled_requirements=[
                        "229",
                        "231",
                        "264",
                        "319",
                        "328",
                    ],
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=1,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-04-12T13:45:48+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-04-12T13:45:48+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-04-12T13:45:48+00:00"
                        ),
                        unreliable_open_vulnerabilities=1,
                        unreliable_status=FindingStatus.VULNERABLE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=0,
                            accepted_undefined=0,
                            in_progress=0,
                            untreated=1,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=0, on_hold=0, verified=0
                        ),
                        unreliable_where="path/to/file4.ext",
                    ),
                    verification=None,
                ),
            )
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "Dataloaders.finding_vulnerabilities_released_nzr",
    new_callable=AsyncMock,
)
@freeze_time("2021-05-27")
async def test_get_oldest_no_treatment(
    mock_dataloaders_finding_vulnerabilities_released_nzr: AsyncMock,
    findings: Iterable[Finding],
    mock_data_for_module: Any,
) -> None:
    findings_ids = [finding.id for finding in findings]
    # Set up mock's return_value using mock_data_for_module fixture
    mock_dataloaders_finding_vulnerabilities_released_nzr.load_many_chained.return_value = mock_data_for_module(  # noqa: E501 pylint: disable=line-too-long
        mock_path="Dataloaders.finding_vulnerabilities_released_nzr",
        mock_args=[findings_ids],
        module_at_test=MODULE_AT_TEST,
    )
    loaders = get_new_context()
    oldest_findings = await get_oldest_no_treatment(loaders, findings)
    expected_output = {
        "oldest_age": 775,
        "oldest_name": "081. Lack of multi-factor authentication",
    }
    assert expected_output == oldest_findings
    mock_dataloaders_finding_vulnerabilities_released_nzr.load_many_chained.assert_called_with(  # noqa: E501 pylint: disable=line-too-long
        findings_ids
    )


@pytest.mark.parametrize(
    ["finding_id"],
    [
        ["475041513"],
    ],
)
@patch(
    MODULE_AT_TEST + "Dataloaders.finding_vulnerabilities_released_nzr_c",
    new_callable=AsyncMock,
)
@freeze_time("2021-05-27")
async def test_get_treatment_summary(
    mock_dataloaders_finding_vulnerabilities_released_nzr_c: AsyncMock,
    finding_id: str,
    mock_data_for_module: Any,
) -> None:
    # Set up mock's return_value using mock_data_for_module fixture
    mock_dataloaders_finding_vulnerabilities_released_nzr_c.load.return_value = mock_data_for_module(  # noqa: E501 pylint: disable=line-too-long
        mock_path="Dataloaders.finding_vulnerabilities_released_nzr_c",
        mock_args=[finding_id],
        module_at_test=MODULE_AT_TEST,
    )
    loaders = get_new_context()
    oldest_findings = await get_treatment_summary(loaders, finding_id)
    expected_output = Treatments(
        accepted=0,
        accepted_undefined=0,
        in_progress=0,
        untreated=1,
    )
    assert expected_output == oldest_findings
    assert (
        mock_dataloaders_finding_vulnerabilities_released_nzr_c.load.called
        is True
    )


@pytest.mark.changes_db
async def test_verify_vulnerabilities() -> None:
    finding_id = "436992569"
    request = await create_dummy_session("unittest@fluidattacks.com")
    info = create_dummy_info(request)
    user_info = {
        "first_name": "Miguel",
        "last_name": "de Orellana",
        "user_email": "unittest@fluidattacks.com",
    }
    justification = "Vuln verified"
    open_vulns_ids = ["587c40de-09a0-4d85-a9f9-eaa46aa895d7"]
    closed_vulns_ids: list[str] = []
    await verify_vulnerabilities(
        context=info.context,
        finding_id=finding_id,
        user_info=user_info,
        justification=justification,
        open_vulns_ids=open_vulns_ids,
        closed_vulns_ids=closed_vulns_ids,
        vulns_to_close_from_file=[],
        loaders=info.context.loaders,
    )
    loaders = get_new_context()
    finding_comments = await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.COMMENT, finding_id=finding_id
        )
    ) + await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.VERIFICATION, finding_id=finding_id
        )
    )
    assert finding_comments[-1].finding_id == finding_id
    assert finding_comments[-1].full_name == "Miguel de Orellana"
    assert finding_comments[-1].comment_type == CommentType.VERIFICATION
    assert finding_comments[-1].content[-13:] == "Vuln verified"
