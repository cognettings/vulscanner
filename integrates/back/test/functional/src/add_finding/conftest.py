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
)
from db_model.findings.types import (
    CVSS31Severity,
    Finding,
    FindingState,
    FindingUnreliableIndicatorsToUpdate,
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


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "organizations": generic_data["db_data"]["organizations"],
        "organization_access": generic_data["db_data"]["organization_access"],
        "groups": generic_data["db_data"]["groups"],
        "policies": generic_data["db_data"]["policies"],
        "stakeholders": generic_data["db_data"]["stakeholders"],
        "findings": [
            {
                "finding": Finding(
                    id="3c475384-834c-47b0-ac71-a41a022e402c",
                    group_name="group1",
                    state=FindingState(
                        modified_by="hacker@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="001. SQL injection - C Sharp SQL API",
                    recommendation="Updated recommendation",
                    description="I just have updated the description",
                    hacker_email="hacker@fluidattacks.com",
                    severity=CVSS31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.85"),
                        availability_impact=Decimal("0.22"),
                        confidentiality_impact=Decimal("0.22"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0.22"),
                        privileges_required=Decimal("0.62"),
                        severity_scope=Decimal("0"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("1"),
                        user_interaction=Decimal("0.85"),
                    ),
                    severity_score=SeverityScore(
                        base_score=Decimal("5.0"),
                        temporal_score=Decimal("4.5"),
                        cvss_v3="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:L/"
                        "E:P/RL:O",
                        cvssf=Decimal("2.000"),
                    ),
                    requirements=(
                        "REQ.0132. Passwords (phrase type) "
                        "must be at least 3 words long."
                    ),
                    threat="Updated threat",
                    attack_vector_description="This is an updated attack",
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
                ],
                "historic_verification": [],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
                    unreliable_closed_vulnerabilities=0,
                    unreliable_open_vulnerabilities=1,
                ),
            },
        ],
    }

    return await db.populate(data)
