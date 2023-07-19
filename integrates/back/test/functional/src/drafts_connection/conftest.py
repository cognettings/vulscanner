# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsState,
    HttpsPatSecret,
)
from db_model.enums import (
    CredentialType,
    Source,
)
from db_model.findings.enums import (
    FindingStateStatus,
    FindingStatus,
)
from db_model.findings.types import (
    CVSS31Severity,
    Finding,
    FindingEvidence,
    FindingEvidences,
    FindingState,
    FindingUnreliableIndicatorsToUpdate,
    FindingVerificationSummary,
)
from db_model.types import (
    SeverityScore,
)
from decimal import (
    Decimal,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("drafts_connection")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "credentials": (
            Credentials(
                id="9edc56a8-2743-437e-a6a9-4847b28e1fd5",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="customer_manager@fluidattacks.com",
                state=CredentialsState(
                    modified_by="customer_manager@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-11 11:32:15+00:00"
                    ),
                    name="cred_https_token",
                    type=CredentialType.HTTPS,
                    secret=HttpsPatSecret(token="token test"),
                    is_pat=False,
                ),
            ),
        ),
        "findings": [
            {
                "finding": Finding(
                    id="475041521",
                    group_name="group1",
                    evidences=FindingEvidences(
                        evidence1=FindingEvidence(
                            description="evidence1",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c"
                            "-evidence1",
                            modified_date=datetime.fromisoformat(
                                "2020-11-19T13:37:10+00:00"
                            ),
                        ),
                    ),
                    state=FindingState(
                        modified_by="admin@fluidattacks.com",
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
                    hacker_email="admin@fluidattacks.com",
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
                "historic_state": [],
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
                    unreliable_status=FindingStatus.VULNERABLE,
                    unreliable_verification_summary=FindingVerificationSummary(
                        requested=3, on_hold=0, verified=0
                    ),
                    unreliable_where="192.168.1.2",
                ),
            },
        ],
        "policies": [
            {
                "level": "group",
                "subject": "admin@fluidattacks.com",
                "object": "group1",
                "role": "admin",
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
