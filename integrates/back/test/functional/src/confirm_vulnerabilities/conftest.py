# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
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
from db_model.types import (
    SeverityScore,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
)
from decimal import (
    Decimal,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("confirm_vulnerabilities")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "findings": [
            {
                "finding": Finding(
                    id="3c475384-834c-47b0-ac71-a41a022e401c",
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
                        cvss_v3="CVSS:3.1/AV:P/AC:H/PR:L/UI:N/S:C/C:L/I:L/A:L/"
                        "E:P/RL:O/CR:L/AR:H/MAV:N/MAC:H/MPR:H/MUI:R/MS:U/MC:L/"
                        "MA:L",
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
                    evidences=FindingEvidences(
                        evidence1=FindingEvidence(
                            description="evidence1",
                            url=(
                                "group1-3c475384-834c-47b0-ac71-a41a022e401c-"
                                "evidence1"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2020-11-19T13:37:10+00:00"
                            ),
                        ),
                        records=FindingEvidence(
                            description="records",
                            url=(
                                "group1-3c475384-834c-47b0-ac71-a41a022e401c-"
                                "records"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2111-11-19T13:37:10+00:00"
                            ),
                        ),
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
                        modified_by="test1@gmail.com",
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
                        status=FindingVerificationStatus.REQUESTED,
                        vulnerability_ids={
                            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
                        },
                    )
                ],
                "unreliable_indicators": FindingUnreliableIndicatorsToUpdate(
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
                    unreliable_status=FindingStatus.DRAFT,
                    unreliable_where="192.168.1.2",
                ),
            },
        ],
        "vulnerabilities": [
            {
                "vulnerability": Vulnerability(
                    created_by="hacker@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:15+00:00"
                    ),
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    organization_name="orgtest",
                    hacker_email="hacker@gmail.com",
                    id="be09edb7-cd5c-47ed-bee4-97c645acdce10",
                    state=VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.SUBMITTED,
                        where="192.168.1.20",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by="hacker@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:15+00:00"
                    ),
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    organization_name="orgtest",
                    hacker_email="hacker@gmail.com",
                    id="be09edb7-cd5c-47ed-bee4-97c645acdce11",
                    severity_score=SeverityScore(
                        base_score=Decimal("5.3"),
                        temporal_score=Decimal("4.8"),
                        cvss_v3="CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:L/I:L/A:L"
                        "/E:P/RL:O/CR:L/AR:H/MAV:N/MAC:H/MPR:H/MUI:R/MS:U/MC:L"
                        "/MA:L",
                        cvssf=Decimal("3.031"),
                    ),
                    state=VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.SUBMITTED,
                        where="192.168.1.20",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by="hacker@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:15+00:00"
                    ),
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    organization_name="orgtest",
                    hacker_email="hacker@gmail.com",
                    id="be09edb7-cd5c-47ed-bee4-97c645acdce12",
                    state=VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.SUBMITTED,
                        where="192.168.1.20",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by="hacker@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:15+00:00"
                    ),
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    organization_name="orgtest",
                    hacker_email="hacker@gmail.com",
                    id="be09edb7-cd5c-47ed-bee4-97c645acdce13",
                    state=VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.SUBMITTED,
                        where="192.168.1.20",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by="hacker@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:15+00:00"
                    ),
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    organization_name="orgtest",
                    hacker_email="hacker@gmail.com",
                    id="be09edb7-cd5c-47ed-bee4-97c645acdce14",
                    state=VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.SUBMITTED,
                        where="192.168.1.20",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                ),
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
