from collections.abc import (
    Callable,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    GitCloningStatus,
    Source,
)
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
    RootUnreliableIndicators,
)
from db_model.types import (
    SeverityScore,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateReason,
    VulnerabilityStateStatus,
    VulnerabilityToolImpact,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityZeroRiskStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTool,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
    VulnerabilityZeroRisk,
)
from decimal import (
    Decimal,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]

MOCK_VULNERABILITIES = {
    "80d6a69f-a376-46be-98cd-2fdedcffdcc0": Vulnerability(
        created_by="test@unittesting.com",
        created_date=datetime.fromisoformat("2020-09-09T21:01:26+00:00"),
        finding_id="422286126",
        group_name="unittesting",
        organization_name="okada",
        hacker_email="test@unittesting.com",
        id="80d6a69f-a376-46be-98cd-2fdedcffdcc0",
        state=VulnerabilityState(
            modified_by="test@unittesting.com",
            modified_date=datetime.fromisoformat("2020-09-09T21:01:26+00:00"),
            source=Source.ASM,
            specific="phone",
            status=VulnerabilityStateStatus.VULNERABLE,
            where="https://example.com",
            commit=None,
            reasons=None,
            other_reason=None,
            tool=VulnerabilityTool(
                name="tool-2", impact=VulnerabilityToolImpact.INDIRECT
            ),
            snippet=None,
        ),
        type=VulnerabilityType.INPUTS,
        bug_tracking_system_url=None,
        custom_severity=None,
        cwe_ids=["CWE-1035", "CWE-770", "CWE-937"],
        developer=None,
        event_id=None,
        hash=None,
        root_id=None,
        severity_score=SeverityScore(
            base_score=Decimal("5.4"),
            temporal_score=Decimal("4.9"),
            cvss_v3="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:P/RL:O/RC"
            ":C",
            cvssf=Decimal("3.482"),
        ),
        skims_method=None,
        skims_technique=None,
        stream=None,
        tags=None,
        treatment=VulnerabilityTreatment(
            modified_date=datetime.fromisoformat("2020-11-23T17:46:10+00:00"),
            status=VulnerabilityTreatmentStatus.IN_PROGRESS,
            acceptance_status=None,
            accepted_until=None,
            justification="This is a treatment justification",
            assigned="integratesuser@gmail.com",
            modified_by="integratesuser2@gmail.com",
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
                "2020-09-09T21:01:26+00:00"
            ),
            unreliable_treatment_changes=1,
        ),
        verification=None,
        zero_risk=VulnerabilityZeroRisk(
            comment_id="123456",
            modified_by="test@gmail.com",
            modified_date=datetime.fromisoformat("2020-09-09T21:01:26+00:00"),
            status=VulnerabilityZeroRiskStatus.CONFIRMED,
        ),
    )
}

MOCK_VULNERABILITIES_FINDING_DATA = {
    "422286126": [
        Vulnerability(
            created_by="integrateshacker@fluidattacks.com",
            created_date=datetime.fromisoformat("2023-04-17T16:44:44+00:00"),
            finding_id="422286126",
            group_name="unittesting",
            organization_name="okada",
            hacker_email="integrateshacker@fluidattacks.com",
            id="08717ec8-53a4-409c-aeb3-883b8c0a2d82",
            state=VulnerabilityState(
                modified_by="integrateshacker@fluidattacks.com",
                modified_date=datetime.fromisoformat(
                    "2023-04-17T16:44:44+00:00"
                ),
                source=Source.ANALYST,
                specific="345",
                status=VulnerabilityStateStatus.SUBMITTED,
                where="universe/path/to/file3.ext",
                commit="e17059d1e17059d1e17059d1e17059d1e17059d1",
                reasons=None,
                other_reason=None,
                tool=VulnerabilityTool(
                    name="tool-1", impact=VulnerabilityToolImpact.DIRECT
                ),
                snippet=None,
            ),
            type=VulnerabilityType.LINES,
            bug_tracking_system_url=None,
            custom_severity=None,
            cwe_ids=None,
            developer=None,
            event_id="EVENT",
            hash=None,
            root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
            severity_score=None,
            skims_method=None,
            skims_technique=None,
            stream=None,
            tags=None,
            treatment=VulnerabilityTreatment(
                modified_date=datetime.fromisoformat(
                    "2023-04-17T16:44:44+00:00"
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
                unreliable_source=Source.ANALYST,
                unreliable_efficacy=Decimal("0"),
                unreliable_last_reattack_date=None,
                unreliable_last_reattack_requester=None,
                unreliable_last_requested_reattack_date=None,
                unreliable_reattack_cycles=None,
                unreliable_report_date=None,
                unreliable_treatment_changes=0,
            ),
            verification=None,
            zero_risk=None,
        ),
        Vulnerability(
            created_by="unittest@fluidattacks.com",
            created_date=datetime.fromisoformat("2020-01-03T17:46:10+00:00"),
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
                    name="tool-2", impact=VulnerabilityToolImpact.INDIRECT
                ),
                snippet=None,
            ),
            type=VulnerabilityType.LINES,
            bug_tracking_system_url=None,
            custom_severity=None,
            cwe_ids=["CWE-1035", "CWE-770", "CWE-937"],
            developer=None,
            event_id=None,
            hash=None,
            root_id=None,
            severity_score=SeverityScore(
                base_score=Decimal("5.4"),
                temporal_score=Decimal("4.9"),
                cvss_v3="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:P/RL:"
                "O/RC:C",
                cvssf=Decimal("3.482"),
            ),
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
        Vulnerability(
            created_by="test@unittesting.com",
            created_date=datetime.fromisoformat("2020-09-09T21:01:26+00:00"),
            finding_id="422286126",
            group_name="unittesting",
            organization_name="okada",
            hacker_email="test@unittesting.com",
            id="80d6a69f-a376-46be-98cd-2fdedcffdcc0",
            state=VulnerabilityState(
                modified_by="test@unittesting.com",
                modified_date=datetime.fromisoformat(
                    "2020-09-09T21:01:26+00:00"
                ),
                source=Source.ASM,
                specific="phone",
                status=VulnerabilityStateStatus.VULNERABLE,
                where="https://example.com",
                commit=None,
                reasons=None,
                other_reason=None,
                tool=VulnerabilityTool(
                    name="tool-2", impact=VulnerabilityToolImpact.INDIRECT
                ),
                snippet=None,
            ),
            type=VulnerabilityType.INPUTS,
            bug_tracking_system_url=None,
            custom_severity=None,
            cwe_ids=["CWE-1035", "CWE-770", "CWE-937"],
            developer=None,
            event_id=None,
            hash=None,
            root_id=None,
            severity_score=SeverityScore(
                base_score=Decimal("5.4"),
                temporal_score=Decimal("4.9"),
                cvss_v3="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:P/RL:"
                "O/RC:C",
                cvssf=Decimal("3.482"),
            ),
            skims_method=None,
            skims_technique=None,
            stream=None,
            tags=None,
            treatment=VulnerabilityTreatment(
                modified_date=datetime.fromisoformat(
                    "2020-09-09T21:01:26+00:00"
                ),
                status=VulnerabilityTreatmentStatus.IN_PROGRESS,
                acceptance_status=None,
                accepted_until=None,
                justification="This is a treatment justification",
                assigned="integratesuser@gmail.com",
                modified_by="integratesuser2@gmail.com",
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
                    "2020-09-09T21:01:26+00:00"
                ),
                unreliable_treatment_changes=1,
            ),
            verification=None,
            zero_risk=VulnerabilityZeroRisk(
                comment_id="123456",
                modified_by="test@gmail.com",
                modified_date=datetime.fromisoformat(
                    "2020-09-09T21:01:26+00:00"
                ),
                status=VulnerabilityZeroRiskStatus.CONFIRMED,
            ),
        ),
        Vulnerability(
            created_by="integrateshacker@fluidattacks.com",
            created_date=datetime.fromisoformat("2023-04-17T16:45:51+00:00"),
            finding_id="422286126",
            group_name="unittesting",
            organization_name="okada",
            hacker_email="integrateshacker@fluidattacks.com",
            id="d65e21fb-f399-46bb-b390-90781079a0e7",
            state=VulnerabilityState(
                modified_by="integrateshacker@fluidattacks.com",
                modified_date=datetime.fromisoformat(
                    "2023-04-17T16:46:15+00:00"
                ),
                source=Source.ANALYST,
                specific="347",
                status=VulnerabilityStateStatus.REJECTED,
                where="universe/path/to/file3.ext",
                commit="e17059d1e17059d1e17059d1e17059d1e17059d1",
                reasons=[VulnerabilityStateReason.NAMING],
                other_reason=None,
                tool=VulnerabilityTool(
                    name="tool-1", impact=VulnerabilityToolImpact.DIRECT
                ),
                snippet=None,
            ),
            type=VulnerabilityType.LINES,
            bug_tracking_system_url=None,
            custom_severity=None,
            cwe_ids=None,
            developer=None,
            event_id="EVENT",
            hash=None,
            root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
            severity_score=None,
            skims_method=None,
            skims_technique=None,
            stream=None,
            tags=None,
            treatment=VulnerabilityTreatment(
                modified_date=datetime.fromisoformat(
                    "2023-04-17T16:45:51+00:00"
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
                unreliable_source=Source.ANALYST,
                unreliable_efficacy=Decimal("0"),
                unreliable_last_reattack_date=None,
                unreliable_last_reattack_requester=None,
                unreliable_last_requested_reattack_date=None,
                unreliable_reattack_cycles=None,
                unreliable_report_date=None,
                unreliable_treatment_changes=0,
            ),
            verification=None,
            zero_risk=None,
        ),
    ]
}

MOCK_VULNERABILITIE_ROOT_DATA = {
    "4039d098-ffc5-4984-8ed3-eb17bca98e19": GitRoot(
        cloning=GitRootCloning(
            modified_date=datetime.fromisoformat("2020-11-19T13:39:10+00:00"),
            reason="root OK",
            status=GitCloningStatus.OK,
            commit="5b5c92105b5c92105b5c92105b5c92105b5c9210",
            commit_date=datetime.fromisoformat(
                "2022-02-15T18:45:06.493253+00:00"
            ),
        ),
        created_by="jdoe@fluidattacks.com",
        created_date=datetime.fromisoformat("2020-11-19T13:37:10+00:00"),
        group_name="unittesting",
        id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
        organization_name="okada",
        state=GitRootState(
            branch="master",
            environment="production",
            includes_health_check=True,
            modified_by="jdoe@fluidattacks.com",
            modified_date=datetime.fromisoformat("2020-11-19T13:37:10+00:00"),
            nickname="universe",
            status=RootStatus.ACTIVE,
            url="https://gitlab.com/fluidattacks/universe",
            credential_id=None,
            gitignore=["bower_components/*", "node_modules/*"],
            other=None,
            reason=None,
            use_vpn=False,
        ),
        type=RootType.GIT,
        unreliable_indicators=RootUnreliableIndicators(
            unreliable_code_languages=[],
            unreliable_last_status_update=datetime.fromisoformat(
                "2020-11-19T13:37:10+00:00"
            ),
        ),
    )
}


@pytest.fixture(scope="function")
def mock_vulnerability() -> Callable[[str], Vulnerability]:
    def _mock_vulnerability(
        vulnerability_id: str,
    ) -> Vulnerability:
        return MOCK_VULNERABILITIES[vulnerability_id]

    return _mock_vulnerability


@pytest.fixture(scope="function")
def mock_vulnerabilities_finding() -> Callable[[str], list[Vulnerability]]:
    def _mock_vulnerabilities_finding(
        finding_id: str,
    ) -> list[Vulnerability]:
        return MOCK_VULNERABILITIES_FINDING_DATA[finding_id]

    return _mock_vulnerabilities_finding


@pytest.fixture(scope="function")
def mock_vulnerabilitie_roots() -> Callable[[str], GitRoot]:
    def _mock_vulnerabilitie_roots(
        finding_id: str,
    ) -> GitRoot:
        return MOCK_VULNERABILITIE_ROOT_DATA[finding_id]

    return _mock_vulnerabilitie_roots
