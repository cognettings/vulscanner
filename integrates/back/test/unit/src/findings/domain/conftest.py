# pylint: disable=too-many-lines
from collections.abc import (
    Callable,
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
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTechnique,
    VulnerabilityToolImpact,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    VulnerabilitiesConnection,
    Vulnerability,
    VulnerabilityEdge,
    VulnerabilityState,
    VulnerabilityTool,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
)
from decimal import (
    Decimal,
)
from dynamodb.types import (
    PageInfo,
)
import pytest
from typing import (
    Any,
)

pytestmark = [
    pytest.mark.asyncio,
]


findings: dict[str, tuple[Finding, ...]] = {
    '["463558592", "422286126"]': (
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
                "La aplicación permite engañar a un usuario            "
                " autenticado por medio de links manipulados para            "
                " ejecutaracciones sobre la aplicación sin su            "
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
                "Hacer uso de tokens en los formularios para la            "
                " verificación de las peticiones realizadas por usuarios      "
                "       legítimos."
            ),
            requirements=(
                "REQ.0174. La aplicación debe garantizar que las            "
                " peticiones que ejecuten transacciones no sigan un           "
                "  patróndiscernible."
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
            title="060. Insecure service configuration - Host verification",
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
                "The source code uses generic exceptions to handle            "
                " unexpected errors. Catching generic exceptions obscures the "
                "            problem that caused the error and promotes a"
                " generic way to             handle different categories or"
                " sources of error. This may             cause security"
                " vulnerabilities to materialize, as some special            "
                " flows go unnoticed."
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
                "Implement password politicies with the best                "
                " practicies for strong passwords."
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
                "An attacker can get passwords of users and                "
                " impersonatethem or used the credentials for practices       "
                "          maliciosus."
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
    )
}

MOCK_DATA = {
    "findings.domain.core.authz.has_access_to_group": {
        '["unittest@fluidattacks.com", "422286126"]': True,
    },
    "findings.domain.core.comments_domain.remove_comments": {
        '["457497316"]': None,
    },
    "findings.domain.core.Dataloaders.finding": {
        '["000000000"]': None,
        '["422286126"]': Finding(
            hacker_email="unittest@fluidattacks.com",
            group_name="unittesting",
            id="422286126",
            state=FindingState(
                modified_by="integratesmanager@gmail.com",
                modified_date=datetime.fromisoformat(
                    "2018-07-09t05:00:00+00:00"
                ),
                source=Source.ASM,
                status=FindingStateStatus.APPROVED,
                rejection=None,
                justification=StateRemovalJustification.NO_JUSTIFICATION,
            ),
            title="060. Insecure service configuration - Host verification",
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
            description="The source code uses generic exceptions to "
            "handle unexpected errors. Catching generic exceptions "
            "obscures the problem that caused the error and promotes "
            "a generic way to handle different categories or sources of "
            "error. This may cause security vulnerabilities to "
            "materialize, as some special flows go unnoticed.",
            evidences=FindingEvidences(
                animation=FindingEvidence(
                    description="",
                    modified_date=datetime.fromisoformat(
                        "2018-07-09t05:00:00+00:00"
                    ),
                    url="unittesting-422286126-animation.webm",
                ),
                evidence1=FindingEvidence(
                    description="this is a test description",
                    modified_date=datetime.fromisoformat(
                        "2018-07-09t05:00:00+00:00"
                    ),
                    url="unittesting-422286126-evidence_route_1.png",
                ),
                evidence2=FindingEvidence(
                    description="exception",
                    modified_date=datetime.fromisoformat(
                        "2018-07-09t05:00:00+00:00"
                    ),
                    url="unittesting-422286126-evidence_route_2.jpg",
                ),
                evidence3=FindingEvidence(
                    description="update testing",
                    modified_date=datetime.fromisoformat(
                        "2018-07-09t05:00:00+00:00"
                    ),
                    url="unittesting-422286126-evidence_route_3.png",
                ),
                evidence4=FindingEvidence(
                    description="changed for testing purposesese",
                    modified_date=datetime.fromisoformat(
                        "2018-07-09t05:00:00+00:00"
                    ),
                    url="unittesting-422286126-evidence_route_4.png",
                ),
                evidence5=FindingEvidence(
                    description="yes, it does.",
                    modified_date=datetime.fromisoformat(
                        "2018-07-09t05:00:00+00:00"
                    ),
                    url="unittesting-422286126-evidence_route_5.png",
                ),
                exploitation=FindingEvidence(
                    description="",
                    modified_date=datetime.fromisoformat(
                        "2018-07-09t05:00:00+00:00"
                    ),
                    url="unittesting-422286126-exploitation.png",
                ),
                records=FindingEvidence(
                    description="",
                    modified_date=datetime.fromisoformat(
                        "2018-07-09t05:00:00+00:00"
                    ),
                    url="unittesting-422286126-evidence_file.csv",
                ),
            ),
            min_time_to_remediate=18,
            recommendation="Implement password politicies with the best "
            "practicies for strong passwords.",
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
                base_score=Decimal("5.4"),
                temporal_score=Decimal("4.9"),
                cvss_v3="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:"
                "P/RL:O/RC:C",
                cvssf=Decimal("3.482"),
            ),
            sorts=FindingSorts.NO,
            threat="A attack can get passwords  of users and He can "
            "impersonate them or used the credentials for practices "
            "maliciosus.",
            unfulfilled_requirements=["266"],
            unreliable_indicators=FindingUnreliableIndicators(
                unreliable_closed_vulnerabilities=0,
                unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                    "2020-01-03t17:46:10+00:00"
                ),
                unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                    "2020-01-03t17:46:10+00:00"
                ),
                unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                    "2020-01-03t17:46:10+00:00"
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
    },
    "findings.domain.core.Dataloaders.finding_vulnerabilities_all": {
        '["457497316"]': [
            Vulnerability(
                created_by="unittest@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2018-11-27T19:54:08+00:00"
                ),
                finding_id="457497316",
                group_name="unittesting",
                organization_name="okada",
                hacker_email="unittest@fluidattacks.com",
                id="6192c72f-2e10-4259-9207-717b2d90d8d2",
                state=VulnerabilityState(
                    modified_by="unittest@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2019-09-16T14:40:37+00:00"
                    ),
                    source=Source.ASM,
                    specific="userToken",
                    status=VulnerabilityStateStatus.SAFE,
                    where="https://10.1.1.1/",
                    commit=None,
                    reasons=None,
                    other_reason=None,
                    tool=None,
                    snippet=None,
                ),
                type=VulnerabilityType.INPUTS,
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
                        "2018-11-27T19:54:08+00:00"
                    ),
                    status=VulnerabilityTreatmentStatus.UNTREATED,
                    acceptance_status=None,
                    accepted_until=None,
                    justification=None,
                    assigned=None,
                    modified_by=None,
                ),
                unreliable_indicators=VulnerabilityUnreliableIndicators(
                    unreliable_closing_date=datetime.fromisoformat(
                        "2019-09-16T14:40:37+00:00"
                    ),
                    unreliable_source=Source.ASM,
                    unreliable_efficacy=Decimal("0"),
                    unreliable_last_reattack_date=None,
                    unreliable_last_reattack_requester=None,
                    unreliable_last_requested_reattack_date=None,
                    unreliable_reattack_cycles=0,
                    unreliable_report_date=datetime.fromisoformat(
                        "2018-11-27T19:54:08+00:00"
                    ),
                    unreliable_treatment_changes=0,
                ),
                verification=None,
                zero_risk=None,
            ),
        ]
    },
    "findings.domain.core.Dataloaders.finding_vulnerabilities_released_nzr": {
        '[["457497318", "475041513"]]': [
            Vulnerability(
                created_by="unittest@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2020-09-12T13:45:48+00:00"
                ),
                finding_id="457497318",
                group_name="oneshottest",
                organization_name="okada",
                hacker_email="unittest@fluidattacks.com",
                id="afb345f6-9319-416a-b174-0201d7cd3822",
                state=VulnerabilityState(
                    modified_by="unittest@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-09-12T13:45:48+00:00"
                    ),
                    source=Source.ASM,
                    specific="6666",
                    status=VulnerabilityStateStatus.VULNERABLE,
                    where="192.168.1.9",
                    commit=None,
                    reasons=None,
                    other_reason=None,
                    tool=None,
                    snippet=None,
                ),
                type=VulnerabilityType.PORTS,
                bug_tracking_system_url=None,
                custom_severity=None,
                cwe_ids=None,
                developer=None,
                event_id=None,
                hash=None,
                root_id=None,
                severity_score=None,
                skims_method=None,
                skims_technique=None,
                stream=None,
                tags=None,
                technique=VulnerabilityTechnique.SCR,
                treatment=VulnerabilityTreatment(
                    modified_date=datetime.fromisoformat(
                        "2020-09-12T13:45:48+00:00"
                    ),
                    status=VulnerabilityTreatmentStatus.UNTREATED,
                    acceptance_status=None,
                    accepted_until=None,
                    justification=None,
                    assigned=None,
                    modified_by=None,
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
                        "2020-09-12T13:45:48+00:00"
                    ),
                    unreliable_treatment_changes=0,
                ),
                verification=None,
                zero_risk=None,
            ),
            Vulnerability(
                created_by="unittest@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2019-04-12T13:45:48+00:00"
                ),
                finding_id="475041513",
                group_name="oneshottest",
                organization_name="okada",
                hacker_email="unittest@fluidattacks.com",
                id="5c689459-64c2-4687-9fef-e5f2dd3c710c",
                state=VulnerabilityState(
                    modified_by="unittest@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2019-04-12T13:45:48+00:00"
                    ),
                    source=Source.ASM,
                    specific="123345",
                    status=VulnerabilityStateStatus.SAFE,
                    where="test/test#.config",
                    commit=None,
                    reasons=None,
                    other_reason=None,
                    tool=VulnerabilityTool(
                        name="tool-1", impact=VulnerabilityToolImpact.INDIRECT
                    ),
                    snippet=None,
                ),
                type=VulnerabilityType.LINES,
                bug_tracking_system_url=None,
                custom_severity=None,
                cwe_ids=None,
                developer=None,
                event_id=None,
                hash=None,
                root_id=None,
                severity_score=None,
                skims_method=None,
                skims_technique=None,
                stream=None,
                tags=None,
                treatment=VulnerabilityTreatment(
                    modified_date=datetime.fromisoformat(
                        "2019-04-12T13:45:48+00:00"
                    ),
                    status=VulnerabilityTreatmentStatus.UNTREATED,
                    acceptance_status=None,
                    accepted_until=None,
                    justification=None,
                    assigned=None,
                    modified_by=None,
                ),
                unreliable_indicators=VulnerabilityUnreliableIndicators(
                    unreliable_closing_date=datetime.fromisoformat(
                        "2019-04-12T13:45:48+00:00"
                    ),
                    unreliable_source=Source.ASM,
                    unreliable_efficacy=Decimal("0"),
                    unreliable_last_reattack_date=None,
                    unreliable_last_reattack_requester=None,
                    unreliable_last_requested_reattack_date=None,
                    unreliable_reattack_cycles=0,
                    unreliable_report_date=datetime.fromisoformat(
                        "2019-04-12T13:45:48+00:00"
                    ),
                    unreliable_treatment_changes=0,
                ),
                verification=None,
                zero_risk=None,
            ),
            Vulnerability(
                created_by="unittest@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2019-04-12T13:45:48+00:00"
                ),
                finding_id="475041513",
                group_name="oneshottest",
                organization_name="okada",
                hacker_email="unittest@fluidattacks.com",
                id="a8c0ff07-bb21-4cd5-bb9f-4d716fc69320",
                state=VulnerabilityState(
                    modified_by="unittest@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2019-04-12T13:45:48+00:00"
                    ),
                    source=Source.ASM,
                    specific="564",
                    status=VulnerabilityStateStatus.VULNERABLE,
                    where="path/to/file4.ext",
                    commit=None,
                    reasons=None,
                    other_reason=None,
                    tool=None,
                    snippet=None,
                ),
                type=VulnerabilityType.LINES,
                bug_tracking_system_url=None,
                custom_severity=None,
                cwe_ids=None,
                developer=None,
                event_id=None,
                hash=None,
                root_id=None,
                severity_score=None,
                skims_method=None,
                skims_technique=None,
                stream=None,
                tags=None,
                treatment=VulnerabilityTreatment(
                    modified_date=datetime.fromisoformat(
                        "2019-04-12T13:45:48+00:00"
                    ),
                    status=VulnerabilityTreatmentStatus.UNTREATED,
                    acceptance_status=None,
                    accepted_until=None,
                    justification=None,
                    assigned=None,
                    modified_by=None,
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
                        "2019-04-12T13:45:48+00:00"
                    ),
                    unreliable_treatment_changes=0,
                ),
                verification=None,
                zero_risk=None,
            ),
        ],
        '[["463558592", "422286126"]]': [
            Vulnerability(
                created_by="unittest@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2019-01-15T15:43:39+00:00"
                ),
                finding_id="463558592",
                group_name="unittesting",
                organization_name="okada",
                hacker_email="unittest@fluidattacks.com",
                id="0a848781-b6a4-422e-95fa-692151e6a98e",
                state=VulnerabilityState(
                    modified_by="unittest@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2019-01-15T15:43:39+00:00"
                    ),
                    source=Source.ASM,
                    specific="12",
                    status=VulnerabilityStateStatus.VULNERABLE,
                    where="path/to/file2.exe",
                    commit=None,
                    reasons=None,
                    tool=None,
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
                        "2019-01-15T15:43:39+00:00"
                    ),
                    status=VulnerabilityTreatmentStatus.ACCEPTED,
                    acceptance_status=None,
                    accepted_until=datetime.fromisoformat(
                        "2021-01-16T17:46:10+00:00"
                    ),
                    justification="This is a treatment justification test",
                    assigned="integratesuser@gmail.comm",
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
                        "2019-01-15T15:43:39+00:00"
                    ),
                    unreliable_treatment_changes=1,
                ),
                verification=None,
                zero_risk=None,
            ),
            Vulnerability(
                created_by="unittest@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2019-01-15T16:04:14+00:00"
                ),
                finding_id="463558592",
                group_name="unittesting",
                organization_name="okada",
                hacker_email="unittest@fluidattacks.com",
                id="242f848c-148a-4028-8e36-c7d995502590",
                state=VulnerabilityState(
                    modified_by="unittest@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2019-01-15T20:59:16+00:00"
                    ),
                    source=Source.ASM,
                    specific="123456",
                    status=VulnerabilityStateStatus.SAFE,
                    where="path/to/file2.ext",
                    commit=None,
                    reasons=None,
                    tool=None,
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
                        "2019-01-15T15:43:39+00:00"
                    ),
                    status=VulnerabilityTreatmentStatus.UNTREATED,
                    acceptance_status=None,
                    accepted_until=None,
                    justification=None,
                    assigned=None,
                    modified_by=None,
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
                        "2019-01-15T16:04:14+00:00"
                    ),
                    unreliable_treatment_changes=0,
                ),
                verification=None,
                zero_risk=None,
            ),
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
                    commit=None,
                    reasons=None,
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
    },
    "findings.domain.core.Dataloaders.finding_vulnerabilities_released_nzr_c": {  # noqa: E501 pylint: disable=line-too-long
        '["475041513"]': VulnerabilitiesConnection(
            edges=(
                VulnerabilityEdge(
                    node=Vulnerability(
                        created_by="unittest@fluidattacks.com",
                        created_date=datetime.fromisoformat(
                            "2019-04-12T13:45:48+00:00"
                        ),
                        finding_id="475041513",
                        group_name="oneshottest",
                        organization_name="okada",
                        hacker_email="unittest@fluidattacks.com",
                        id="a8c0ff07-bb21-4cd5-bb9f-4d716fc69320",
                        state=VulnerabilityState(
                            modified_by="unittest@fluidattacks.com",
                            modified_date=datetime.fromisoformat(
                                "2019-04-12T13:45:48+00:00"
                            ),
                            source=Source.ASM,
                            specific="564",
                            status=VulnerabilityStateStatus.VULNERABLE,
                            where="path/to/file4.ext",
                            commit=None,
                            reasons=None,
                            other_reason=None,
                            tool=None,
                            snippet=None,
                        ),
                        type=VulnerabilityType.LINES,
                        bug_tracking_system_url=None,
                        custom_severity=None,
                        cwe_ids=None,
                        developer=None,
                        event_id=None,
                        hash=None,
                        root_id=None,
                        severity_score=None,
                        skims_method=None,
                        skims_technique=None,
                        stream=None,
                        tags=None,
                        treatment=VulnerabilityTreatment(
                            modified_date=datetime.fromisoformat(
                                "2019-04-12T13:45:48+00:00"
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
                            unreliable_last_reattack_date=None,
                            unreliable_last_reattack_requester=None,
                            unreliable_last_requested_reattack_date=None,
                            unreliable_reattack_cycles=0,
                            unreliable_report_date=datetime.fromisoformat(
                                "2019-04-12T13:45:48+00:00"
                            ),
                            unreliable_treatment_changes=0,
                        ),
                        verification=None,
                        zero_risk=None,
                    ),
                    cursor="eyJway",
                ),
            ),
            page_info=PageInfo(has_next_page=False, end_cursor="bnVsbA=="),
            total=None,
        )
    },
    "findings.domain.core.findings_model.remove": {
        '["unittesting", "457497316"]': None,
    },
    "findings.domain.core.findings_utils.get_group_findings": {
        '["unittesting"]': [
            Finding(
                hacker_email="unittest@fluidattacks.com",
                group_name="unittesting",
                id="422286126",
                state=FindingState(
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-07-09t05:00:00+00:00"
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
                description="The source code uses generic exceptions to "
                "handle unexpected errors. Catching generic exceptions "
                "obscures the problem that caused the error and promotes "
                "a generic way to handle different categories or sources of "
                "error. This may cause security vulnerabilities to "
                "materialize, as some special flows go unnoticed.",
                evidences=FindingEvidences(
                    animation=FindingEvidence(
                        description="",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09t05:00:00+00:00"
                        ),
                        url="unittesting-422286126-animation.webm",
                    ),
                    evidence1=FindingEvidence(
                        description="this is a test description",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09t05:00:00+00:00"
                        ),
                        url="unittesting-422286126-evidence_route_1.png",
                    ),
                    evidence2=FindingEvidence(
                        description="exception",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09t05:00:00+00:00"
                        ),
                        url="unittesting-422286126-evidence_route_2.jpg",
                    ),
                    evidence3=FindingEvidence(
                        description="update testing",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09t05:00:00+00:00"
                        ),
                        url="unittesting-422286126-evidence_route_3.png",
                    ),
                    evidence4=FindingEvidence(
                        description="changed for testing purposesese",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09t05:00:00+00:00"
                        ),
                        url="unittesting-422286126-evidence_route_4.png",
                    ),
                    evidence5=FindingEvidence(
                        description="yes, it does.",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09t05:00:00+00:00"
                        ),
                        url="unittesting-422286126-evidence_route_5.png",
                    ),
                    exploitation=FindingEvidence(
                        description="",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09t05:00:00+00:00"
                        ),
                        url="unittesting-422286126-exploitation.png",
                    ),
                    records=FindingEvidence(
                        description="",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09t05:00:00+00:00"
                        ),
                        url="unittesting-422286126-evidence_file.csv",
                    ),
                ),
                min_time_to_remediate=18,
                recommendation="Implement password politicies with the best "
                "practicies for strong passwords.",
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
                    base_score=Decimal("5.4"),
                    temporal_score=Decimal("4.9"),
                    cvss_v3="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:"
                    "P/RL:O/RC:C",
                    cvssf=Decimal("3.482"),
                ),
                sorts=FindingSorts.NO,
                threat="A attack can get passwords  of users and He can "
                "impersonate them or used the credentials for practices "
                "maliciosus.",
                unfulfilled_requirements=["266"],
                unreliable_indicators=FindingUnreliableIndicators(
                    unreliable_closed_vulnerabilities=0,
                    unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2020-01-03t17:46:10+00:00"
                    ),
                    unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2020-01-03t17:46:10+00:00"
                    ),
                    unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2020-01-03t17:46:10+00:00"
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
            Finding(
                hacker_email="unittest@fluidattacks.com",
                group_name="unittesting",
                id="436992569",
                state=FindingState(
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2019-04-08T00:00:00+00:00"
                    ),
                    source=Source.ASM,
                    status=FindingStateStatus.APPROVED,
                    rejection=None,
                    justification=StateRemovalJustification.NO_JUSTIFICATION,
                ),
                title="038. Business information leak",
                attack_vector_description="- Atack vector",
                creation=FindingState(
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2019-04-08T00:18:00+00:00"
                    ),
                    source=Source.ASM,
                    status=FindingStateStatus.CREATED,
                    rejection=None,
                    justification=StateRemovalJustification.NO_JUSTIFICATION,
                ),
                description="Se obtiene información de negocio, como:\r\n- "
                "Lista de usuarios\r\n- Información estratégica\r\n- "
                "Información de empleados\r\n- Información de clientes\r\n- "
                "Información de proveedores",
                evidences=FindingEvidences(
                    animation=FindingEvidence(
                        description="",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08t05:00:00+00:00"
                        ),
                        url="unittesting-436992569-animation.webm",
                    ),
                    evidence1=FindingEvidence(
                        description="Comm1",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08t05:00:00+00:00"
                        ),
                        url="unittesting-436992569-evidence_route_1.png",
                    ),
                    evidence2=FindingEvidence(
                        description="Comm2",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08t05:00:00+00:00"
                        ),
                        url="unittesting-436992569-evidence_route_2.jpg",
                    ),
                    evidence3=FindingEvidence(
                        description="Comm3",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08t05:00:00+00:00"
                        ),
                        url="unittesting-436992569-evidence_route_3.png",
                    ),
                    evidence4=FindingEvidence(
                        description="Comm4",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08t05:00:00+00:00"
                        ),
                        url="unittesting-436992569-evidence_route_4.png",
                    ),
                    evidence5=FindingEvidence(
                        description="Comm5",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08t05:00:00+00:00"
                        ),
                        url="unittesting-436992569-evidence_route_5.png",
                    ),
                    exploitation=FindingEvidence(
                        description="",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08t05:00:00+00:00"
                        ),
                        url="unittesting-436992569-exploitation.png",
                    ),
                    records=None,
                ),
                min_time_to_remediate=18,
                recommendation="De acuerdo a la clasificación de la "
                "información encontrada, establecer los controles necesarios "
                "para que la información sea accesible sólo a las personas "
                "indicadas.",
                requirements="REQ.0176. El sistema debe restringir el acceso "
                "a objetos del sistema que tengan contenido sensible. Sólo "
                "permitirá su acceso a usuarios autorizados.",
                severity=CVSS31Severity(
                    attack_complexity=Decimal("0.44"),
                    attack_vector=Decimal("0.62"),
                    availability_impact=Decimal("0.22"),
                    availability_requirement=Decimal("1.5"),
                    confidentiality_impact=Decimal("0"),
                    confidentiality_requirement=Decimal("1.5"),
                    exploitability=Decimal("0.97"),
                    integrity_impact=Decimal("0"),
                    integrity_requirement=Decimal("0.5"),
                    modified_attack_complexity=Decimal("0.77"),
                    modified_attack_vector=Decimal("0.85"),
                    modified_availability_impact=Decimal("0"),
                    modified_confidentiality_impact=Decimal("0"),
                    modified_integrity_impact=Decimal("0"),
                    modified_privileges_required=Decimal("0.85"),
                    modified_user_interaction=Decimal("0.85"),
                    modified_severity_scope=Decimal("0"),
                    privileges_required=Decimal("0.85"),
                    remediation_level=Decimal("0.97"),
                    report_confidence=Decimal("0.96"),
                    severity_scope=Decimal("1"),
                    user_interaction=Decimal("0.62"),
                ),
                severity_score=SeverityScore(
                    base_score=Decimal("2.9"),
                    temporal_score=Decimal("2.7"),
                    cvss_v3="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:C/C:N/I:N/A:L/E:F/"
                    "RL:W/RC:R/CR:H/IR:L/AR:H/MAV:N/MAC:L/MPR:N/MUI:N/MS:U",
                    cvssf=Decimal("0.165"),
                ),
                sorts=FindingSorts.NO,
                threat="Risk.",
                unfulfilled_requirements=["176", "177", "261", "300"],
                unreliable_indicators=FindingUnreliableIndicators(
                    unreliable_closed_vulnerabilities=4,
                    unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2019-09-16t21:01:24+00:00"
                    ),
                    unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2019-08-30t14:30:13+00:00"
                    ),
                    unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2019-08-30t14:30:13+00:00"
                    ),
                    unreliable_open_vulnerabilities=24,
                    unreliable_status=FindingStatus.VULNERABLE,
                    unreliable_treatment_summary=FindingTreatmentSummary(
                        accepted=0,
                        accepted_undefined=0,
                        in_progress=0,
                        untreated=24,
                    ),
                    unreliable_verification_summary=FindingVerificationSummary(
                        requested=1, on_hold=2, verified=1
                    ),
                    unreliable_where="192.168.1.10, 192.168.1.12, "
                    "192.168.1.13, 192.168.1.14, 192.168.1.15, "
                    "192.168.1.16, 192.168.1.17, 192.168.1.2, 192.168.1.3, "
                    "192.168.1.4, 192.168.1.5, 192.168.1.6, 192.168.1.7, "
                    "192.168.1.8, 192.168.1.9, 192.168.100.101, "
                    "192.168.100.104, 192.168.100.105, 192.168.100.108, "
                    "192.168.100.111",
                ),
                verification=FindingVerification(
                    comment_id="1558048727111",
                    modified_by="integrateshacker@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-02-21t15:41:04+00:00"
                    ),
                    status=FindingVerificationStatus.VERIFIED,
                    vulnerability_ids={"15375781-31f2-4953-ac77-f31134225747"},
                ),
            ),
            Finding(
                hacker_email="unittest@fluidattacks.com",
                group_name="unittesting",
                id="457497316",
                state=FindingState(
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-11-27t05:00:00+00:00"
                    ),
                    source=Source.ASM,
                    status=FindingStateStatus.APPROVED,
                    rejection=None,
                    justification=StateRemovalJustification.NO_JUSTIFICATION,
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
                    justification=StateRemovalJustification.NO_JUSTIFICATION,
                ),
                description="Descripción de fuga de información técnica",
                evidences=FindingEvidences(
                    animation=None,
                    evidence1=None,
                    evidence2=FindingEvidence(
                        description="test",
                        modified_date=datetime.fromisoformat(
                            "2018-11-27t05:00:00+00:00"
                        ),
                        url="unittesting-457497316-evidence_route_2.jpg",
                    ),
                    evidence3=FindingEvidence(
                        description="Comentario",
                        modified_date=datetime.fromisoformat(
                            "2018-11-27t05:00:00+00:00"
                        ),
                        url="unittesting-457497316-evidence_route_3.png",
                    ),
                    evidence4=None,
                    evidence5=None,
                    exploitation=None,
                    records=None,
                ),
                min_time_to_remediate=18,
                recommendation="Eliminar el banner de los servicios con fuga "
                "de información, Verificar que los encabezados HTTP no "
                "expongan ningún nombre o versión.",
                requirements="REQ.0077. La aplicación no debe revelar "
                "detalles del sistema interno como stack traces, fragmentos "
                "de sentencias SQL y nombres de base de datos o tablas."
                "\r\nREQ.0176. El sistema debe restringir el acceso a "
                "objetos del sistema que tengan contenido sensible. Sólo "
                "permitirá su acceso a usuarios autorizados.",
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
                unfulfilled_requirements=["077", "176"],
                unreliable_indicators=FindingUnreliableIndicators(
                    unreliable_closed_vulnerabilities=1,
                    unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2018-11-27t19:54:08+00:00"
                    ),
                    unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2018-11-27t19:54:08+00:00"
                    ),
                    unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2018-11-27t19:54:08+00:00"
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
            Finding(
                hacker_email="unittest@fluidattacks.com",
                group_name="unittesting",
                id="463461507",
                state=FindingState(
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2019-01-10t05:00:00+00:00"
                    ),
                    source=Source.ASM,
                    status=FindingStateStatus.APPROVED,
                    rejection=None,
                    justification=StateRemovalJustification.NO_JUSTIFICATION,
                ),
                title="083. XML injection (XXE)",
                attack_vector_description="Test attack vector.",
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
                description="La aplicaciofectada permite la inyeccio de coo "
                "XML que es ejecutado de forma remota y permite la "
                "exfiltracio de archivos o ejecucioemota de comandos en el "
                "servidor.",
                evidences=FindingEvidences(
                    animation=FindingEvidence(
                        description="Animation test",
                        modified_date=datetime.fromisoformat(
                            "2019-01-10t05:00:00+00:00"
                        ),
                        url="unittesting-463461507-animation.webm",
                    ),
                    evidence1=None,
                    evidence2=FindingEvidence(
                        description="A2 test",
                        modified_date=datetime.fromisoformat(
                            "2019-01-10t05:00:00+00:00"
                        ),
                        url="unittesting-463461507-evidence_route_2.jpg",
                    ),
                    evidence3=FindingEvidence(
                        description="123A",
                        modified_date=datetime.fromisoformat(
                            "2019-01-10t05:00:00+00:00"
                        ),
                        url="unittesting-463461507-evidence_route_3.png",
                    ),
                    evidence4=FindingEvidence(
                        description="AAA1",
                        modified_date=datetime.fromisoformat(
                            "2019-01-10t05:00:00+00:00"
                        ),
                        url="unittesting-463461507-evidence_route_4.png",
                    ),
                    evidence5=FindingEvidence(
                        description="sdasdasda",
                        modified_date=datetime.fromisoformat(
                            "2019-01-10t05:00:00+00:00"
                        ),
                        url="unittesting-463461507-evidence_route_5.png",
                    ),
                    exploitation=None,
                    records=None,
                ),
                min_time_to_remediate=18,
                recommendation="Filtrar la informacioue recibe y envia la "
                "aplicacioor medio de listas blancas",
                requirements="REQ.0173. El sistema debe descartar toda la "
                "informacion potencialmente insegura que sea recibida por "
                "entradas de datos.",
                severity=CVSS31Severity(
                    attack_complexity=Decimal("0.44"),
                    attack_vector=Decimal("0.62"),
                    availability_impact=Decimal("0.22"),
                    availability_requirement=Decimal("1"),
                    confidentiality_impact=Decimal("0.22"),
                    confidentiality_requirement=Decimal("1.5"),
                    exploitability=Decimal("0.94"),
                    integrity_impact=Decimal("0"),
                    integrity_requirement=Decimal("1"),
                    modified_attack_complexity=Decimal("0.44"),
                    modified_attack_vector=Decimal("0.62"),
                    modified_availability_impact=Decimal("0.22"),
                    modified_confidentiality_impact=Decimal("0.22"),
                    modified_integrity_impact=Decimal("0"),
                    modified_privileges_required=Decimal("0.85"),
                    modified_user_interaction=Decimal("0.62"),
                    modified_severity_scope=Decimal("0"),
                    privileges_required=Decimal("0.85"),
                    remediation_level=Decimal("0.95"),
                    report_confidence=Decimal("0.96"),
                    severity_scope=Decimal("0"),
                    user_interaction=Decimal("0.62"),
                ),
                severity_score=SeverityScore(
                    base_score=Decimal("3.7"),
                    temporal_score=Decimal("3.2"),
                    cvss_v3="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:L/E:P/"
                    "RL:O/RC:R/CR:H/MAV:A/MAC:H/MPR:N/MUI:R/MS:U/MC:L/MA:L",
                    cvssf=Decimal("0.330"),
                ),
                sorts=FindingSorts.NO,
                threat="<i>test</i>",
                unfulfilled_requirements=["173"],
                unreliable_indicators=FindingUnreliableIndicators(
                    unreliable_closed_vulnerabilities=0,
                    unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2019-09-13t14:58:38+00:00"
                    ),
                    unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2019-09-12t13:45:48+00:00"
                    ),
                    unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2019-09-12t13:45:48+00:00"
                    ),
                    unreliable_open_vulnerabilities=2,
                    unreliable_status=FindingStatus.VULNERABLE,
                    unreliable_treatment_summary=FindingTreatmentSummary(
                        accepted=1,
                        accepted_undefined=0,
                        in_progress=0,
                        untreated=1,
                    ),
                    unreliable_verification_summary=FindingVerificationSummary(
                        requested=0, on_hold=0, verified=0
                    ),
                    unreliable_where="192.168.1.18, 192.168.100.105",
                ),
                verification=None,
            ),
            Finding(
                hacker_email="unittest@fluidattacks.com",
                group_name="unittesting",
                id="463558592",
                state=FindingState(
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-12-17t05:00:00+00:00"
                    ),
                    source=Source.ASM,
                    status=FindingStateStatus.APPROVED,
                    rejection=None,
                    justification=StateRemovalJustification.NO_JUSTIFICATION,
                ),
                title="007. Cross-site request forgery",
                attack_vector_description="test",
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
                description="La aplicación permite engañar a un usuario "
                "autenticado por medio de links manipulados para ejecutar "
                "acciones sobre la aplicación sin su consentimiento..",
                evidences=FindingEvidences(
                    animation=None,
                    evidence1=FindingEvidence(
                        description="test",
                        modified_date=datetime.fromisoformat(
                            "2018-12-17t05:00:00+00:00"
                        ),
                        url="unittesting-463558592-evidence_route_1.png",
                    ),
                    evidence2=FindingEvidence(
                        description="Test2",
                        modified_date=datetime.fromisoformat(
                            "2018-12-17t05:00:00+00:00"
                        ),
                        url="unittesting-463558592-evidence_route_2.jpg",
                    ),
                    evidence3=FindingEvidence(
                        description="Test3",
                        modified_date=datetime.fromisoformat(
                            "2018-12-17t05:00:00+00:00"
                        ),
                        url="unittesting-463558592-evidence_route_3.png",
                    ),
                    evidence4=FindingEvidence(
                        description="An error",
                        modified_date=datetime.fromisoformat(
                            "2018-12-17t05:00:00+00:00"
                        ),
                        url="unittesting-463558592-evidence_route_4.png",
                    ),
                    evidence5=FindingEvidence(
                        description="4",
                        modified_date=datetime.fromisoformat(
                            "2018-12-17t05:00:00+00:00"
                        ),
                        url="unittesting-463558592-evidence_route_5.png",
                    ),
                    exploitation=None,
                    records=None,
                ),
                min_time_to_remediate=18,
                recommendation="Hacer uso de tokens en los formularios para "
                "la verificación de las peticiones realizadas por usuarios "
                "legítimos.\r\n",
                requirements="REQ.0174. La aplicación debe garantizar que las "
                "peticiones que ejecuten transacciones no sigan un patrón "
                "discernible.",
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
                    unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2019-01-15T16:04:14+00:00"
                    ),
                    unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2019-01-15t15:43:39+00:00"
                    ),
                    unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2019-01-15t15:43:39+00:00"
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
                        "2020-01-19t15:41:04+00:00"
                    ),
                    status=FindingVerificationStatus.REQUESTED,
                    vulnerability_ids={
                        "3bcdb384-5547-4170-a0b6-3b397a245465",
                        "74632c0c-db08-47c2-b013-c70e5b67c49f",
                    },
                ),
            ),
            Finding(
                hacker_email="integratesmanager@gmail.com",
                group_name="unittesting",
                id="988493279",
                state=FindingState(
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2019-04-08T00:15:00+00:00"
                    ),
                    source=Source.ASM,
                    status=FindingStateStatus.APPROVED,
                    rejection=None,
                    justification=StateRemovalJustification.NO_JUSTIFICATION,
                ),
                title="014. Insecure functionality",
                attack_vector_description="",
                creation=FindingState(
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2019-04-08T00:18:00+00:00"
                    ),
                    source=Source.ASM,
                    status=FindingStateStatus.CREATED,
                    rejection=None,
                    justification=StateRemovalJustification.NO_JUSTIFICATION,
                ),
                description="Funcionalidad insegura description",
                evidences=FindingEvidences(
                    animation=None,
                    evidence1=None,
                    evidence2=None,
                    evidence3=None,
                    evidence4=None,
                    evidence5=None,
                    exploitation=FindingEvidence(
                        description="",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T00:15:00+00:00"
                        ),
                        url="unittesting-988493279-exploitation.png",
                    ),
                    records=None,
                ),
                min_time_to_remediate=20,
                recommendation="-",
                requirements="REQ.0266. La organización debe deshabilitar "
                "las funciones inseguras de un sistema. (hardening de "
                "sistemas)",
                severity=CVSS31Severity(
                    attack_complexity=Decimal("0.77"),
                    attack_vector=Decimal("0.85"),
                    availability_impact=Decimal("0.22"),
                    availability_requirement=Decimal("0.5"),
                    confidentiality_impact=Decimal("0.22"),
                    confidentiality_requirement=Decimal("1.5"),
                    exploitability=Decimal("0.94"),
                    integrity_impact=Decimal("0.22"),
                    integrity_requirement=Decimal("1"),
                    modified_attack_complexity=Decimal("0.77"),
                    modified_attack_vector=Decimal("0.55"),
                    modified_availability_impact=Decimal("0"),
                    modified_confidentiality_impact=Decimal("0"),
                    modified_integrity_impact=Decimal("0"),
                    modified_privileges_required=Decimal("0.62"),
                    modified_user_interaction=Decimal("0.85"),
                    modified_severity_scope=Decimal("0"),
                    privileges_required=Decimal("0.85"),
                    remediation_level=Decimal("0.95"),
                    report_confidence=Decimal("0.96"),
                    severity_scope=Decimal("0"),
                    user_interaction=Decimal("0.85"),
                ),
                severity_score=SeverityScore(
                    base_score=Decimal("7.3"),
                    temporal_score=Decimal("6.3"),
                    cvss_v3="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L/E:P/"
                    "RL:O/RC:R/CR:H/AR:L/MAV:L/MAC:L/MPR:L/MUI:N/MS:U",
                    cvssf=Decimal("24.251"),
                ),
                sorts=FindingSorts.NO,
                threat="",
                unfulfilled_requirements=["266"],
                unreliable_indicators=FindingUnreliableIndicators(
                    unreliable_closed_vulnerabilities=1,
                    unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2019-04-08T00:15:00+00:00"
                    ),
                    unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2019-04-08T00:15:00+00:00"
                    ),
                    unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                        "2019-04-08T00:15:00+00:00"
                    ),
                    unreliable_open_vulnerabilities=1,
                    unreliable_status=FindingStatus.VULNERABLE,
                    unreliable_treatment_summary=FindingTreatmentSummary(
                        accepted=0,
                        accepted_undefined=1,
                        in_progress=0,
                        untreated=0,
                    ),
                    unreliable_verification_summary=FindingVerificationSummary(
                        requested=0, on_hold=0, verified=0
                    ),
                    unreliable_where="192.168.1.19",
                ),
                verification=None,
            ),
        ],
    },
    "findings.domain.core.remove_all_evidences": {
        '["457497316", "unittesting"]': None,
    },
    "findings.domain.core.vulns_domain.mask_vulnerability": {
        '["unittest@fluidattacks.com", "457497316"]': None,
    },
    "findings.domain.core._is_pending_verification": {
        '["unittesting"]': [False, True, False, False, False, False]
    },
    "findings.domain.evidence.files_utils.assert_uploaded_file_mime": {
        '["okada-unittesting-records123.csv", "fileRecords"]': True,
        '["test-big-image.png", "animation"]': True,
        '["test-file-records.csv", "fileRecords"]': False,
    },
    "findings.domain.evidence.files_utils.get_file_size": {
        '["okada-unittesting-records123.csv"]': 68,
        '["test-big-image.png"]': 45380085,
    },
    "findings.domain.evidence.validate_filename": {
        '["okada-unittesting-records123.csv", "463558592"]': None,
    },
}


@pytest.fixture(scope="function")
def findings_data() -> dict[str, tuple[Finding, ...]]:
    return findings


@pytest.fixture
def mock_data_for_module(
    *,
    resolve_mock_data: Any,
) -> Any:
    def _mock_data_for_module(
        mock_path: str, mock_args: list[Any], module_at_test: str
    ) -> Callable[[str, list[Any], str], Any]:
        return resolve_mock_data(
            mock_data=MOCK_DATA,
            mock_path=mock_path,
            mock_args=mock_args,
            module_at_test=module_at_test,
        )

    return _mock_data_for_module
