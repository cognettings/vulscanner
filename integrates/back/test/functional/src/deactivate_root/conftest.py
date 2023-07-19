# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    GitCloningStatus,
    Source,
)
from db_model.events.enums import (
    EventStateStatus,
    EventType,
)
from db_model.events.types import (
    Event,
    EventEvidence,
    EventEvidences,
    EventState,
)
from db_model.findings.enums import (
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
    FindingUnreliableIndicatorsToUpdate,
    FindingVerification,
)
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
    IPRoot,
    IPRootState,
    URLRoot,
    URLRootState,
)
from db_model.types import (
    SeverityScore,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
    VulnerabilityVerification,
)
from decimal import (
    Decimal,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("deactivate_root")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    test_email = "admin@gmail.com"
    test_status = RootStatus.ACTIVE
    data: dict[str, Any] = {
        "roots": [
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        reason="root creation",
                        status=GitCloningStatus("UNKNOWN"),
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group1",
                    id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        gitignore=["bower_components/*", "node_modules/*"],
                        includes_health_check=True,
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="nickname",
                        other=None,
                        reason=None,
                        status=test_status,
                        url="https://gitlab.com/fluidattacks/universe",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": IPRoot(
                    created_by=test_email,
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group2",
                    id="83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
                    organization_name="orgtest",
                    state=IPRootState(
                        address="192.168.1.1",
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="deactivate_ip_1",
                        other=None,
                        reason=None,
                        status=test_status,
                    ),
                    type=RootType.IP,
                ),
                "historic_state": [],
            },
            {
                "root": URLRoot(
                    created_by=test_email,
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group2",
                    id="eee8b331-98b9-4e32-a3c7-ec22bd244ae8",
                    organization_name="orgtest",
                    state=URLRootState(
                        host="app.fluidattacks.com",
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="deactivate_url_1",
                        other=None,
                        path="/",
                        port="8080",
                        protocol="HTTPS",
                        reason=None,
                        status=test_status,
                    ),
                    type=RootType.URL,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        reason="root creation",
                        status=GitCloningStatus("UNKNOWN"),
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group2",
                    id="702b81b3-d741-4699-9173-ecbc30bfb0cb",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        gitignore=["bower_components/*", "node_modules/*"],
                        includes_health_check=True,
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="nickname",
                        other=None,
                        reason=None,
                        status=test_status,
                        url="https://gitlab.com/fluidattacks/repo",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": IPRoot(
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group1",
                    id="44db9bee-c97d-4161-98c6-f124d7dc9a41",
                    organization_name="orgtest",
                    state=IPRootState(
                        # FP: local testing
                        address="192.168.1.2",  # NOSONAR
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="deactivate_ip_2",
                        other=None,
                        reason=None,
                        status=test_status,
                    ),
                    type=RootType.IP,
                ),
                "historic_state": [],
            },
            {
                "root": URLRoot(
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group1",
                    id="bd4e5e66-da26-4274-87ed-17de7c3bc2f1",
                    organization_name="orgtest",
                    state=URLRootState(
                        host="test.fluidattacks.com",
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="deactivate_url_2",
                        other=None,
                        path="/",
                        port="8080",
                        protocol="HTTPS",
                        reason=None,
                        status=test_status,
                    ),
                    type=RootType.URL,
                ),
                "historic_state": [],
            },
        ],
        "findings": [
            {
                "finding": Finding(
                    id="475041521",
                    group_name="group1",
                    state=FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title=(
                        "060. Insecure service configuration - "
                        "Host verification"
                    ),
                    recommendation="Updated recommendation",
                    description="I just have updated the description",
                    hacker_email=generic_data["global_vars"]["admin_email"],
                    severity=CVSS31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.2"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("1.5"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("0.5"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_user_interaction=Decimal("0.62"),
                        modified_integrity_impact=Decimal("0"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_severity_scope=Decimal("0"),
                        modified_privileges_required=Decimal("0.27"),
                        modified_attack_vector=Decimal("0.85"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        privileges_required=Decimal("0.62"),
                        severity_scope=Decimal("1.0"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("1"),
                        user_interaction=Decimal("0.85"),
                    ),
                    severity_score=SeverityScore(
                        base_score=Decimal("4.5"),
                        temporal_score=Decimal("4.1"),
                        cvss_v3="CVSS:3.1/AV:P/AC:H/PR:L/UI:N/S:C/C:L/I:L/A:L/"
                        "E:P/RL:O/CR:L/AR:H/MAV:N/MAC:H/MPR:H/MUI:R/MS:U/MC:L/"
                        "MA:L",
                        cvssf=Decimal("1.149"),
                    ),
                    requirements="R359. Avoid using generic exceptions.",
                    threat="Autenticated attacker from the Internet.",
                    attack_vector_description=(
                        "This is an updated attack vector"
                    ),
                ),
                "historic_state": [
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:12+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:13+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.REJECTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:14+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                    ),
                ],
                "historic_verification": [
                    FindingVerification(
                        comment_id="42343434",
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-01-01T00:45:12+00:00"
                        ),
                        status=FindingVerificationStatus.ON_HOLD,
                        vulnerability_ids={
                            "6401bc87-8633-4a4a-8d8e-7dae0ca57e6b",
                        },
                    )
                ],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
                    unreliable_closed_vulnerabilities=3,
                    unreliable_open_vulnerabilities=5,
                    unreliable_newest_vulnerability_report_date=(
                        datetime.fromisoformat("2020-12-26T05:45:00+00:00")
                    ),
                    unreliable_oldest_open_vulnerability_report_date=(
                        datetime.fromisoformat("2020-02-24T05:45:00+00:00")
                    ),
                    unreliable_oldest_vulnerability_report_date=(
                        datetime.fromisoformat("2018-04-01T05:45:00+00:00")
                    ),
                    unreliable_status=FindingStatus.VULNERABLE,
                    unreliable_where="192.168.1.2",
                ),
            },
            {
                "finding": Finding(
                    id="575041531",
                    group_name="group1",
                    state=FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="001. SQL injection - C Sharp SQL API",
                    recommendation="Updated recommendation",
                    description="I just have updated the description",
                    hacker_email="test1@gmail.com",
                    severity=CVSS31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.2"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("1.5"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("0.5"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_user_interaction=Decimal("0.62"),
                        modified_integrity_impact=Decimal("0"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_severity_scope=Decimal("0"),
                        modified_privileges_required=Decimal("0.27"),
                        modified_attack_vector=Decimal("0.85"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        privileges_required=Decimal("0.62"),
                        severity_scope=Decimal("1.0"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("1"),
                        user_interaction=Decimal("0.85"),
                    ),
                    severity_score=SeverityScore(
                        base_score=Decimal("4.5"),
                        temporal_score=Decimal("4.1"),
                        cvss_v3="CVSS:3.1/AV:P/AC:H/PR:L/UI:N/S:C/C:L/I:L/"
                        "A:L/E:P/RL:O/CR:L/AR:H/MAV:N/MAC:H/MPR:H/MUI:R/MS:U/"
                        "MC:L/MA:L",
                        cvssf=Decimal("1.149"),
                    ),
                    requirements=(
                        "REQ.0132. Passwords (phrase type) "
                        "must be at least 3 words long."
                    ),
                    threat="Updated threat",
                    attack_vector_description=(
                        "This is an updated attack vector"
                    ),
                ),
                "historic_state": [
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:12+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:13+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.REJECTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:14+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                    ),
                ],
                "historic_verification": [],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
                    unreliable_closed_vulnerabilities=3,
                    unreliable_open_vulnerabilities=5,
                    unreliable_newest_vulnerability_report_date=(
                        datetime.fromisoformat("2020-12-26T05:45:00+00:00")
                    ),
                    unreliable_oldest_open_vulnerability_report_date=(
                        datetime.fromisoformat("2020-02-24T05:45:00+00:00")
                    ),
                    unreliable_oldest_vulnerability_report_date=(
                        datetime.fromisoformat("2018-04-01T05:45:00+00:00")
                    ),
                    unreliable_status=FindingStatus.VULNERABLE,
                    unreliable_where="192.168.1.2",
                ),
            },
            {
                "finding": Finding(
                    id="475041531",
                    group_name="group1",
                    evidences=FindingEvidences(
                        evidence1=FindingEvidence(
                            description="evidence1",
                            url=(
                                "group1-3c475384-834c-47b0-ac71-a41a022e401c"
                                "-evidence1"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2020-11-19T13:37:10+00:00"
                            ),
                        ),
                        evidence2=FindingEvidence(
                            description="evidence2",
                            url=(
                                "group1-3c475384-834c-47b0-ac71-a41a022e401c"
                                "-evidence2"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2020-11-19T13:37:10+00:00"
                            ),
                        ),
                        evidence3=FindingEvidence(
                            description="evidence3",
                            url=(
                                "group1-3c475384-834c-47b0-ac71-a41a022e401c"
                                "-evidence3"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2020-11-19T13:37:10+00:00"
                            ),
                        ),
                        evidence4=FindingEvidence(
                            description="evidence4",
                            url=(
                                "group1-3c475384-834c-47b0-ac71-a41a022e401c"
                                "-evidence4"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2020-11-19T13:37:10+00:00"
                            ),
                        ),
                        evidence5=FindingEvidence(
                            description="evidence5",
                            url=(
                                "group1-3c475384-834c-47b0-ac71-a41a022e401c"
                                "-evidence5"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2020-11-19T13:37:10+00:00"
                            ),
                        ),
                        exploitation=FindingEvidence(
                            description="exploitation",
                            url=(
                                "group1-3c475384-834c-47b0-ac71-a41a022e401c"
                                "-exploitation"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2010-11-19T13:37:10+00:00"
                            ),
                        ),
                        animation=FindingEvidence(
                            description="animation",
                            url=(
                                "group1-3c475384-834c-47b0-ac71-a41a022e401c"
                                "-animation"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2020-11-19T13:37:10+00:00"
                            ),
                        ),
                    ),
                    state=FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="001. SQL injection - C Sharp SQL API",
                    recommendation="Updated recommendation",
                    description="I just have updated the description",
                    hacker_email="test1@gmail.com",
                    severity=CVSS31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.2"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("1.5"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("0.5"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_user_interaction=Decimal("0.62"),
                        modified_integrity_impact=Decimal("0"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_severity_scope=Decimal("0"),
                        modified_privileges_required=Decimal("0.27"),
                        modified_attack_vector=Decimal("0.85"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        privileges_required=Decimal("0.62"),
                        severity_scope=Decimal("1.0"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("1"),
                        user_interaction=Decimal("0.85"),
                    ),
                    severity_score=SeverityScore(
                        base_score=Decimal("4.5"),
                        temporal_score=Decimal("4.1"),
                        cvss_v3="CVSS:3.1/AV:P/AC:H/PR:L/UI:N/S:C/C:L/I:L/A:L"
                        "/E:P/RL:O/CR:L/AR:H/MAV:N/MAC:H/MPR:H/MUI:R/MS:U/MC:L"
                        "/MA:L",
                        cvssf=Decimal("1.149"),
                    ),
                    requirements=(
                        "REQ.0132. Passwords (phrase type) "
                        "must be at least 3 words long."
                    ),
                    threat="Updated threat",
                    attack_vector_description=(
                        "This is an updated attack vector"
                    ),
                ),
                "historic_state": [],
                "historic_verification": [
                    FindingVerification(
                        comment_id="42343434",
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-01-01T00:45:12+00:00"
                        ),
                        status=FindingVerificationStatus.REQUESTED,
                        vulnerability_ids={
                            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
                            "uuid2",
                        },
                    )
                ],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
                    unreliable_closed_vulnerabilities=3,
                    unreliable_open_vulnerabilities=5,
                    unreliable_newest_vulnerability_report_date=(
                        datetime.fromisoformat("2020-12-26T05:45:00+00:00")
                    ),
                    unreliable_oldest_open_vulnerability_report_date=(
                        datetime.fromisoformat("2020-02-24T05:45:00+00:00")
                    ),
                    unreliable_oldest_vulnerability_report_date=(
                        datetime.fromisoformat("2018-04-01T05:45:00+00:00")
                    ),
                    unreliable_status=FindingStatus.VULNERABLE,
                    unreliable_where="192.168.1.2",
                ),
            },
        ],
        "events": [
            {
                "event": Event(
                    id="418900971",
                    group_name="group1",
                    hacker="unittest@fluidattacks.com",
                    client="Fluid",
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2018-06-27T12:00:00+00:00"
                    ),
                    description="ARM unit test",
                    type=EventType.OTHER,
                    event_date=datetime.fromisoformat(
                        "2018-06-27T12:00:00+00:00"
                    ),
                    evidences=EventEvidences(
                        image_1=EventEvidence(
                            file_name=(
                                "unittesting_418900971_evidence_image_1.png"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2019-03-11T15:57:45+00:00"
                            ),
                        ),
                        file_1=EventEvidence(
                            file_name=(
                                "unittesting_418900971_evidence_file_1.csv"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2019-03-11T15:57:45+00:00"
                            ),
                        ),
                    ),
                    state=EventState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2018-06-27T12:00:00+00:00"
                        ),
                        status=EventStateStatus.OPEN,
                    ),
                ),
                "historic_state": [
                    EventState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2018-06-27T19:40:05+00:00"
                        ),
                        status=EventStateStatus.CREATED,
                    ),
                ],
            },
        ],
        "vulnerabilities": [
            {
                "vulnerability": Vulnerability(
                    created_by=generic_data["global_vars"]["admin_email"],
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:13+00:00"
                    ),
                    finding_id="475041521",
                    group_name="group1",
                    organization_name="orgtest",
                    hacker_email=generic_data["global_vars"]["admin_email"],
                    id="be09edb7-cd5c-47ed-bee4-97c645acdce8",
                    state=VulnerabilityState(
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:13+00:00"
                        ),
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.20",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:14+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                    root_id="83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by=generic_data["global_vars"]["admin_email"],
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:15+00:00"
                    ),
                    finding_id="475041521",
                    group_name="group1",
                    organization_name="orgtest",
                    hacker_email=generic_data["global_vars"]["admin_email"],
                    id="6401bc87-8633-4a4a-8d8e-7dae0ca57e6a",
                    state=VulnerabilityState(
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        specific="2320",
                        status=VulnerabilityStateStatus.SAFE,
                        where="192.168.1.1",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        accepted_until=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        justification="justification",
                        assigned=generic_data["global_vars"]["user_email"],
                        modified_by=generic_data["global_vars"][
                            "user_manager_email"
                        ],
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=1,
                    ),
                    root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by=generic_data["global_vars"]["admin_email"],
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:15+00:00"
                    ),
                    finding_id="475041521",
                    group_name="group1",
                    organization_name="orgtest",
                    hacker_email=generic_data["global_vars"]["admin_email"],
                    id="6401bc87-8633-4a4a-8d8e-7dae0ca57e6b",
                    state=VulnerabilityState(
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        specific="2321",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.2",
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2022-09-01T00:45:11+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.ON_HOLD,
                        event_id="418900971",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        accepted_until=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        justification="justification",
                        assigned=generic_data["global_vars"]["user_email"],
                        modified_by=generic_data["global_vars"][
                            "user_manager_email"
                        ],
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=1,
                    ),
                    root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                ),
                "historic_verification": [
                    VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T01:45:11+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                    VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2022-09-01T00:45:11+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.ON_HOLD,
                        event_id="418900971",
                    ),
                ],
            },
            {
                "vulnerability": Vulnerability(
                    created_by=generic_data["global_vars"]["admin_email"],
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:16+00:00"
                    ),
                    finding_id="475041521",
                    group_name="group1",
                    organization_name="orgtest",
                    hacker_email=generic_data["global_vars"]["admin_email"],
                    id="baabb2c1-00bc-47ae-9d5f-c9c2e2e88e70",
                    state=VulnerabilityState(
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:16+00:00"
                        ),
                        source=Source.ASM,
                        specific="2322",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.3",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        accepted_until=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        justification="justification",
                        assigned=generic_data["global_vars"][
                            "user_manager_email"
                        ],
                        modified_by=generic_data["global_vars"][
                            "user_manager_email"
                        ],
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=1,
                    ),
                    root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                ),
            },
        ],
    }

    return await db.populate({**generic_data["db_data"], **data})
