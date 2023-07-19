from back.test.unit.src.utils import (
    get_mock_response,
    get_mocked_path,
    get_module_at_test,
)
from collections import (
    OrderedDict,
)
from custom_exceptions import (
    InvalidFileName,
    InvalidFileSize,
    InvalidFileType,
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
from db_model.findings.enums import (
    FindingSorts,
    FindingStateStatus,
    FindingStatus,
    FindingVerificationStatus,
)
from db_model.findings.types import (
    CVSS31Severity,
    Finding,
    FindingEvidence,
    FindingEvidences,
    FindingState,
    FindingTreatmentSummary,
    FindingUnreliableIndicators,
    FindingVerification,
    FindingVerificationSummary,
)
from db_model.types import (
    SeverityScore,
)
from decimal import (
    Decimal,
)
from findings.domain.evidence import (
    download_evidence_file,
    get_records_from_file,
    validate_evidence,
    validate_evidence_name,
)
import json
import os
import pytest
from starlette.datastructures import (
    UploadFile,
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


@pytest.mark.parametrize(
    [
        "group_name",
        "finding_id",
        "file_name",
    ],
    [
        [
            "unittesting",
            "422286126",
            "unittesting-422286126-evidence_route_1.png",
        ],
    ],
)
@patch(
    get_mocked_path("findings_storage.search_evidence"),
    new_callable=AsyncMock,
)
@patch(
    get_mocked_path("findings_storage.download_evidence"),
    new_callable=AsyncMock,
)
async def test_download_evidence_file(
    mock_download_evidence: AsyncMock,
    mock_search_evidence: AsyncMock,
    group_name: str,
    finding_id: str,
    file_name: str,
) -> None:
    mock_parameters = json.dumps([group_name, finding_id, file_name])
    mock_search_evidence.return_value = get_mock_response(
        get_mocked_path("findings_storage.search_evidence"), mock_parameters
    )
    mock_download_evidence.return_value = get_mock_response(
        get_mocked_path("findings_storage.download_evidence"), mock_parameters
    )
    test_data = await download_evidence_file(group_name, finding_id, file_name)

    expected_output = os.path.abspath(
        # FP: local testing
        "/tmp/unittesting-422286126-evidence_route_1.png"  # NOSONAR
    )
    assert test_data == expected_output


@pytest.mark.parametrize(
    ["group_name", "finding_id", "file_name", "expected_output"],
    [
        [
            "unittesting",
            "422286126",
            "unittesting-422286126-evidence_file.csv",
            [
                OrderedDict(
                    [
                        ("song", "a million little pieces"),
                        ("artist", "placebo"),
                        ("year", "2010"),
                    ]
                ),
                OrderedDict(
                    [
                        ("song", "heart shaped box"),
                        ("artist", "nirvana"),
                        ("year", "1992"),
                    ]
                ),
                OrderedDict(
                    [("song", "zenith"), ("artist", "ghost"), ("year", "2015")]
                ),
                OrderedDict(
                    [
                        ("song", "hysteria"),
                        ("artist", "def leppard"),
                        ("year", "1987"),
                    ]
                ),
            ],
        ],
    ],
)
@patch(get_mocked_path("download_evidence_file"), new_callable=AsyncMock)
async def test_get_records_from_file(
    mock_download_evidence_file: AsyncMock,
    group_name: str,
    finding_id: str,
    file_name: str,
    expected_output: list[dict[object, object]],
) -> None:
    mock_download_evidence_file.return_value = get_mock_response(
        get_mocked_path("download_evidence_file"),
        json.dumps([group_name, finding_id, file_name]),
    )

    test_data = await get_records_from_file(group_name, finding_id, file_name)

    assert test_data == expected_output
    assert mock_download_evidence_file.called is True


@pytest.mark.parametrize(
    ["evidence_id", "file_name", "finding", "validate_name"],
    [
        [
            "fileRecords",
            "okada-unittesting-records123.csv",
            Finding(
                hacker_email="unittest@fluidattacks.com",
                group_name="unittesting",
                id="463558592",
                state=FindingState(
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-12-17T05:00:00+00:00"
                    ),
                    source=Source.ASM,
                    status=FindingStateStatus.APPROVED,
                    rejection=None,
                    justification=StateRemovalJustification.NO_JUSTIFICATION,
                ),
                title="007. Cross-site request forgery",
                attack_vector_description="This is an attack vector",
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
                description=(
                    "La aplicación permite engañar a un usuario "
                    "autenticado por medio de links manipulados para "
                    "ejecutaracciones sobre la aplicación sin su "
                    " consentimiento."
                ),
                evidences=FindingEvidences(
                    animation=None,
                    evidence1=FindingEvidence(
                        description="test",
                        modified_date=datetime.fromisoformat(
                            "2018-12-17T05:00:00+00:00"
                        ),
                        url="unittesting-463558592-evidence_route_1.png",
                    ),
                    evidence2=FindingEvidence(
                        description="Test2",
                        modified_date=datetime.fromisoformat(
                            "2018-12-17T05:00:00+00:00"
                        ),
                        url="unittesting-463558592-evidence_route_2.jpg",
                    ),
                    evidence3=FindingEvidence(
                        description="Test3",
                        modified_date=datetime.fromisoformat(
                            "2018-12-17T05:00:00+00:00"
                        ),
                        url="unittesting-463558592-evidence_route_3.png",
                    ),
                    evidence4=FindingEvidence(
                        description="Test4",
                        modified_date=datetime.fromisoformat(
                            "2018-12-17T05:00:00+00:00"
                        ),
                        url="unittesting-463558592-evidence_route_4.png",
                    ),
                    evidence5=FindingEvidence(
                        description="Test5",
                        modified_date=datetime.fromisoformat(
                            "2018-12-17T05:00:00+00:00"
                        ),
                        url="unittesting-463558592-evidence_route_5.png",
                    ),
                    exploitation=None,
                    records=None,
                ),
                min_time_to_remediate=18,
                recommendation=(
                    "Hacer uso de tokens en los formularios para la "
                    "verificación de las peticiones realizadas por usuarios "
                    "legítimos."
                ),
                requirements=(
                    "REQ.0174. La aplicación debe garantizar que las "
                    "peticiones que ejecuten transacciones no sigan un "
                    "patrón discernible."
                ),
                severity=CVSS31Severity(
                    attack_complexity=Decimal("0.44"),
                    attack_vector=Decimal("0.62"),
                    availability_impact=Decimal("0"),
                    availability_requirement=Decimal("1"),
                    confidentiality_impact=Decimal("0.56"),
                    confidentiality_requirement=Decimal("1"),
                    exploitability=Decimal("0.91"),
                    integrity_impact=Decimal("0.22"),
                    integrity_requirement=Decimal("1.5"),
                    modified_attack_complexity=Decimal("0.44"),
                    modified_attack_vector=Decimal("0.62"),
                    modified_availability_impact=Decimal("0"),
                    modified_confidentiality_impact=Decimal("0.56"),
                    modified_integrity_impact=Decimal("0.22"),
                    modified_privileges_required=Decimal("0.62"),
                    modified_user_interaction=Decimal("0.62"),
                    modified_severity_scope=Decimal("0"),
                    privileges_required=Decimal("0.62"),
                    remediation_level=Decimal("0.95"),
                    report_confidence=Decimal("0.96"),
                    severity_scope=Decimal("0"),
                    user_interaction=Decimal("0.62"),
                ),
                severity_score=SeverityScore(
                    base_score=Decimal("5.1"),
                    temporal_score=Decimal("4.3"),
                    cvss_v3="CVSS:3.1/AV:A/AC:H/PR:L/UI:R/S:U/C:H/I:L/A:N/E:U/"
                    "RL:O/RC:R/IR:H/MAV:A/MAC:H/MPR:L/MUI:R/MS:U/MC:H/MI:L",
                    cvssf=Decimal("1.516"),
                ),
                sorts=FindingSorts.NO,
                threat="Test.",
                unfulfilled_requirements=["029", "174"],
                unreliable_indicators=FindingUnreliableIndicators(
                    unreliable_closed_vulnerabilities=1,
                    unreliable_newest_vulnerability_report_date=(
                        datetime.fromisoformat("2019-01-15T16:04:14+00:00")
                    ),
                    unreliable_oldest_open_vulnerability_report_date=(
                        datetime.fromisoformat("2019-01-15T15:43:39+00:00")
                    ),
                    unreliable_oldest_vulnerability_report_date=(
                        datetime.fromisoformat("2019-01-15T15:43:39+00:00")
                    ),
                    unreliable_open_vulnerabilities=1,
                    unreliable_status=FindingStatus.VULNERABLE,
                    unreliable_treatment_summary=FindingTreatmentSummary(
                        accepted=1,
                        accepted_undefined=0,
                        in_progress=0,
                        untreated=0,
                    ),
                    unreliable_verification_summary=FindingVerificationSummary(
                        requested=0, on_hold=0, verified=0
                    ),
                    unreliable_where="path/to/file2.ext",
                ),
                verification=FindingVerification(
                    comment_id="1558048727999",
                    modified_by="integratesuser@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2020-01-19T15:41:04+00:00"
                    ),
                    status=FindingVerificationStatus.REQUESTED,
                    vulnerability_ids={
                        "3bcdb384-5547-4170-a0b6-3b397a245465",
                        "74632c0c-db08-47c2-b013-c70e5b67c49f",
                    },
                ),
            ),
            True,
        ],
    ],
)
@patch(MODULE_AT_TEST + "validate_filename", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "files_utils.get_file_size", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "files_utils.assert_uploaded_file_mime",
    new_callable=AsyncMock,
)
async def test_validate_evidence(
    # pylint: disable=too-many-arguments, too-many-locals
    mock_files_utils_assert_uploaded_file_mime: AsyncMock,
    mock_files_utils_get_file_size: AsyncMock,
    mock_validate_filename: AsyncMock,
    evidence_id: str,
    file_name: str,
    finding: Finding,
    validate_name: bool,
    mock_data_for_module: Any,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_files_utils_assert_uploaded_file_mime,
            "files_utils.assert_uploaded_file_mime",
            [file_name, evidence_id],
        ),
        (
            mock_files_utils_get_file_size,
            "files_utils.get_file_size",
            [file_name],
        ),
        (
            mock_validate_filename,
            "validate_filename",
            [file_name, finding.id],
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
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "mock/evidences/" + file_name)
    mime_type = "text/csv"
    loaders = get_new_context()
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(file_name, test_file, mime_type)
        test_data = await validate_evidence(
            evidence_id=evidence_id,
            file=uploaded_file,
            loaders=loaders,
            finding=finding,
            validate_name=validate_name,
        )
    assert isinstance(test_data, bool)
    assert test_data
    mocks_list = [mock[0] for mock in mocks_setup_list]
    assert all(mock_object.called is True for mock_object in mocks_list)


@pytest.mark.parametrize(
    [
        "organization_name",
        "group_name",
        "filename",
        "invalid_file_name",
        "invalid_file_name_length",
    ],
    [
        [
            "okada",
            "unittesting",
            "okada-unittesting-records123.csv",
            "organization-unittesting-records123.csv",
            "okada-unittesting-records.csv",
        ],
    ],
)
def test_validate_evidence_name(
    organization_name: str,
    group_name: str,
    filename: str,
    invalid_file_name: str,
    invalid_file_name_length: str,
) -> None:
    validate_evidence_name(
        organization_name=organization_name,
        group_name=group_name,
        filename=filename,
    )
    with pytest.raises(InvalidFileName):
        validate_evidence_name(
            organization_name=organization_name,
            group_name=group_name,
            filename=invalid_file_name,
        )
    with pytest.raises(InvalidFileName):
        validate_evidence_name(
            organization_name=organization_name,
            group_name=group_name,
            filename=invalid_file_name_length,
        )


@pytest.mark.parametrize(
    ("evidence_id", "file_name", "finding"),
    (
        (
            "fileRecords",
            "test-file-records.csv",
            Finding(
                hacker_email="unittest@fluidattacks.com",
                group_name="unittesting",
                id="422286126",
                state=FindingState(
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-07-09T05:00:00+00:00"
                    ),
                    source=Source.ASM,
                    status=FindingStateStatus.APPROVED,
                    rejection=None,
                    justification=StateRemovalJustification.NO_JUSTIFICATION,
                ),
                title="060. Insecure service configuration - Host "
                "verification",
                attack_vector_description="This is an attack vector",
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
                description=(
                    "The source code uses generic exceptions to handle "
                    "unexpected errors. Catching generic exceptions obscures "
                    "the problem that caused the error and promotes a "
                    "generic way to handle different categories or sources "
                    "of error. This may cause security vulnerabilities to "
                    "materialize, as some special flows go unnoticed."
                ),
                evidences=FindingEvidences(
                    animation=FindingEvidence(
                        description="Test description",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        url="unittesting-422286126-animation.gif",
                    ),
                    evidence1=FindingEvidence(
                        description="this is a test description",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        url="unittesting-422286126-evidence_route_1.png",
                    ),
                    evidence2=FindingEvidence(
                        description="exception",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        url="unittesting-422286126-evidence_route_2.jpg",
                    ),
                    evidence3=FindingEvidence(
                        description="Description",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        url="unittesting-422286126-evidence_route_3.png",
                    ),
                    evidence4=FindingEvidence(
                        description="changed for testing purposesese",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        url="unittesting-422286126-evidence_route_4.png",
                    ),
                    evidence5=FindingEvidence(
                        description="Test description",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        url="unittesting-422286126-evidence_route_5.png",
                    ),
                    exploitation=FindingEvidence(
                        description="test",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        url="unittesting-422286126-exploitation.png",
                    ),
                    records=FindingEvidence(
                        description="test",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        url="unittesting-422286126-evidence_file.csv",
                    ),
                ),
                min_time_to_remediate=18,
                recommendation=(
                    "Implement password politicies with the best "
                    "practicies for strong passwords."
                ),
                requirements="R359. Avoid using generic exceptions.",
                severity=CVSS31Severity(
                    attack_complexity=Decimal("0.77"),
                    attack_vector=Decimal("0.62"),
                    availability_impact=Decimal("0"),
                    availability_requirement=Decimal("1"),
                    confidentiality_impact=Decimal("0"),
                    confidentiality_requirement=Decimal("1"),
                    exploitability=Decimal("0.91"),
                    integrity_impact=Decimal("0.22"),
                    integrity_requirement=Decimal("1"),
                    modified_attack_complexity=Decimal("0.77"),
                    modified_attack_vector=Decimal("0.62"),
                    modified_availability_impact=Decimal("0"),
                    modified_confidentiality_impact=Decimal("0"),
                    modified_integrity_impact=Decimal("0.22"),
                    modified_privileges_required=Decimal("0.62"),
                    modified_user_interaction=Decimal("0.85"),
                    modified_severity_scope=Decimal("0"),
                    privileges_required=Decimal("0.62"),
                    remediation_level=Decimal("0.97"),
                    report_confidence=Decimal("0.92"),
                    severity_scope=Decimal("0"),
                    user_interaction=Decimal("0.85"),
                ),
                severity_score=SeverityScore(
                    base_score=Decimal("3.5"),
                    temporal_score=Decimal("2.9"),
                    cvss_v3="CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/"
                    "RL:W/RC:U/MAV:A/MAC:L/MPR:L/MUI:N/MS:U/MI:L",
                    cvssf=Decimal("0.218"),
                ),
                sorts=FindingSorts.NO,
                threat=(
                    "An attacker can get passwords of users and "
                    "impersonatethem or used the credentials for practices "
                    "maliciosus."
                ),
                unfulfilled_requirements=["266"],
                unreliable_indicators=FindingUnreliableIndicators(
                    unreliable_closed_vulnerabilities=0,
                    unreliable_newest_vulnerability_report_date=(
                        datetime.fromisoformat("2020-01-03T17:46:10+00:00")
                    ),
                    unreliable_oldest_open_vulnerability_report_date=(
                        datetime.fromisoformat("2020-01-03T17:46:10+00:00")
                    ),
                    unreliable_oldest_vulnerability_report_date=(
                        datetime.fromisoformat("2020-01-03T17:46:10+00:00")
                    ),
                    unreliable_open_vulnerabilities=1,
                    unreliable_status=FindingStatus.VULNERABLE,
                    unreliable_treatment_summary=FindingTreatmentSummary(
                        accepted=0,
                        accepted_undefined=0,
                        in_progress=1,
                        untreated=0,
                    ),
                    unreliable_verification_summary=FindingVerificationSummary(
                        requested=0, on_hold=0, verified=0
                    ),
                    unreliable_where="test/data/lib_path/f060/csharp.cs",
                ),
                verification=None,
            ),
        ),
    ),
)
@patch(
    MODULE_AT_TEST + "files_utils.assert_uploaded_file_mime",
    new_callable=AsyncMock,
)
async def test_validate_evidence_invalid_type(
    mock_files_utils_assert_uploaded_file_mime: AsyncMock,
    evidence_id: str,
    file_name: str,
    finding: Finding,
    mock_data_for_module: Any,
) -> None:
    # Set up mock's result using mock_data_for_module fixture
    mock_files_utils_assert_uploaded_file_mime.return_value = (
        mock_data_for_module(
            mock_path="files_utils.assert_uploaded_file_mime",
            mock_args=[file_name, evidence_id],
            module_at_test=MODULE_AT_TEST,
        )
    )
    loaders = get_new_context()
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "mock/evidences/" + file_name)
    mime_type = "image/png"

    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "test-file-records.csv", test_file, mime_type
        )
        with pytest.raises(InvalidFileType):
            await validate_evidence(
                evidence_id=evidence_id,
                file=uploaded_file,
                loaders=loaders,
                finding=finding,
            )
    assert mock_files_utils_assert_uploaded_file_mime.called is True


@pytest.mark.parametrize(
    ("evidence_id", "file_name", "finding"),
    (
        (
            "animation",
            "test-big-image.png",
            Finding(
                hacker_email="unittest@fluidattacks.com",
                group_name="unittesting",
                id="422286126",
                state=FindingState(
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-07-09T05:00:00+00:00"
                    ),
                    source=Source.ASM,
                    status=FindingStateStatus.APPROVED,
                    rejection=None,
                    justification=StateRemovalJustification.NO_JUSTIFICATION,
                ),
                title="060. Insecure service configuration - Host "
                "verification",
                attack_vector_description="This is an attack vector",
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
                description=(
                    "The source code uses generic exceptions to handle "
                    "unexpected errors. Catching generic exceptions obscures "
                    "the problem that caused the error and promotes a "
                    "generic way to handle different categories or sources "
                    "of error. This may cause security vulnerabilities to "
                    "materialize, as some special flows go unnoticed."
                ),
                evidences=FindingEvidences(
                    animation=FindingEvidence(
                        description="Test description",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        url="unittesting-422286126-animation.gif",
                    ),
                    evidence1=FindingEvidence(
                        description="this is a test description",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        url="unittesting-422286126-evidence_route_1.png",
                    ),
                    evidence2=FindingEvidence(
                        description="exception",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        url="unittesting-422286126-evidence_route_2.jpg",
                    ),
                    evidence3=FindingEvidence(
                        description="Description",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        url="unittesting-422286126-evidence_route_3.png",
                    ),
                    evidence4=FindingEvidence(
                        description="changed for testing purposesese",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        url="unittesting-422286126-evidence_route_4.png",
                    ),
                    evidence5=FindingEvidence(
                        description="Test description",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        url="unittesting-422286126-evidence_route_5.png",
                    ),
                    exploitation=FindingEvidence(
                        description="test",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        url="unittesting-422286126-exploitation.png",
                    ),
                    records=FindingEvidence(
                        description="test",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        url="unittesting-422286126-evidence_file.csv",
                    ),
                ),
                min_time_to_remediate=18,
                recommendation=(
                    "Implement password politicies with the best "
                    "practicies for strong passwords."
                ),
                requirements="R359. Avoid using generic exceptions.",
                severity=CVSS31Severity(
                    attack_complexity=Decimal("0.77"),
                    attack_vector=Decimal("0.62"),
                    availability_impact=Decimal("0"),
                    availability_requirement=Decimal("1"),
                    confidentiality_impact=Decimal("0"),
                    confidentiality_requirement=Decimal("1"),
                    exploitability=Decimal("0.91"),
                    integrity_impact=Decimal("0.22"),
                    integrity_requirement=Decimal("1"),
                    modified_attack_complexity=Decimal("0.77"),
                    modified_attack_vector=Decimal("0.62"),
                    modified_availability_impact=Decimal("0"),
                    modified_confidentiality_impact=Decimal("0"),
                    modified_integrity_impact=Decimal("0.22"),
                    modified_privileges_required=Decimal("0.62"),
                    modified_user_interaction=Decimal("0.85"),
                    modified_severity_scope=Decimal("0"),
                    privileges_required=Decimal("0.62"),
                    remediation_level=Decimal("0.97"),
                    report_confidence=Decimal("0.92"),
                    severity_scope=Decimal("0"),
                    user_interaction=Decimal("0.85"),
                ),
                severity_score=SeverityScore(
                    base_score=Decimal("3.5"),
                    temporal_score=Decimal("2.9"),
                    cvss_v3="CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/"
                    "RL:W/RC:U/MAV:A/MAC:L/MPR:L/MUI:N/MS:U/MI:L",
                    cvssf=Decimal("0.218"),
                ),
                sorts=FindingSorts.NO,
                threat=(
                    "An attacker can get passwords of users and "
                    "impersonatethem or used the credentials for practices "
                    "maliciosus."
                ),
                unfulfilled_requirements=["266"],
                unreliable_indicators=FindingUnreliableIndicators(
                    unreliable_closed_vulnerabilities=0,
                    unreliable_newest_vulnerability_report_date=(
                        datetime.fromisoformat("2020-01-03T17:46:10+00:00")
                    ),
                    unreliable_oldest_open_vulnerability_report_date=(
                        datetime.fromisoformat("2020-01-03T17:46:10+00:00")
                    ),
                    unreliable_oldest_vulnerability_report_date=(
                        datetime.fromisoformat("2020-01-03T17:46:10+00:00")
                    ),
                    unreliable_open_vulnerabilities=1,
                    unreliable_status=FindingStatus.VULNERABLE,
                    unreliable_treatment_summary=FindingTreatmentSummary(
                        accepted=0,
                        accepted_undefined=0,
                        in_progress=1,
                        untreated=0,
                    ),
                    unreliable_verification_summary=FindingVerificationSummary(
                        requested=0, on_hold=0, verified=0
                    ),
                    unreliable_where="test/data/lib_path/f060/csharp.cs",
                ),
                verification=None,
            ),
        ),
    ),
)
@patch(MODULE_AT_TEST + "files_utils.get_file_size", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "files_utils.assert_uploaded_file_mime",
    new_callable=AsyncMock,
)
async def test_validate_evidence_invalid_size(
    # pylint: disable=too-many-arguments, too-many-locals
    mock_files_utils_assert_uploaded_file_mime: AsyncMock,
    mock_files_utils_get_file_size: AsyncMock,
    evidence_id: str,
    file_name: str,
    finding: Finding,
    mock_data_for_module: Any,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_files_utils_assert_uploaded_file_mime,
            "files_utils.assert_uploaded_file_mime",
            [file_name, evidence_id],
        ),
        (
            mock_files_utils_get_file_size,
            "files_utils.get_file_size",
            [file_name],
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
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "mock/evidences/" + file_name)
    mime_type = "image/png"
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(file_name, test_file, mime_type)
        with pytest.raises(InvalidFileSize):
            await validate_evidence(
                evidence_id=evidence_id,
                file=uploaded_file,
                loaders=loaders,
                finding=finding,
            )
    mocks_list = [mock[0] for mock in mocks_setup_list]
    assert all(mock_object.called is True for mock_object in mocks_list)
