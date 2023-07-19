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
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("request_vulnerabilities_verification")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    vulnerabilities = [
        {
            "vulnerability": Vulnerability(
                created_by="test1@gmail.com",
                created_date=datetime.fromisoformat(
                    "2018-04-08T00:45:15+00:00"
                ),
                finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                group_name="group1",
                organization_name="orgtest",
                hacker_email="test1@gmail.com",
                id="be09edb7-cd5c-47ed-bee4-97c645acdce8",
                state=VulnerabilityState(
                    modified_by="test1@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-04-08T00:45:15+00:00"
                    ),
                    source=Source.ASM,
                    specific="9999",
                    status=VulnerabilityStateStatus.VULNERABLE,
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
                created_by="test1@gmail.com",
                created_date=datetime.fromisoformat(
                    "2018-04-08T00:45:15+00:00"
                ),
                finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                group_name="group1",
                organization_name="orgtest",
                hacker_email="test1@gmail.com",
                id="be09edb7-cd5c-47ed-bee4-97c645acdce9",
                state=VulnerabilityState(
                    modified_by="test1@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-04-08T00:45:15+00:00"
                    ),
                    source=Source.ASM,
                    specific="9999",
                    status=VulnerabilityStateStatus.VULNERABLE,
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
                created_by="test1@gmail.com",
                created_date=datetime.fromisoformat(
                    "2018-04-08T00:45:15+00:00"
                ),
                finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                group_name="group1",
                organization_name="orgtest",
                hacker_email="test1@gmail.com",
                id="be09edb7-cd5c-47ed-bee4-97c645acdce15",
                state=VulnerabilityState(
                    modified_by="test1@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-04-08T00:45:15+00:00"
                    ),
                    source=Source.ASM,
                    specific="9999",
                    status=VulnerabilityStateStatus.VULNERABLE,
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
                created_by="test1@gmail.com",
                created_date=datetime.fromisoformat(
                    "2018-04-08T00:45:15+00:00"
                ),
                finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                group_name="group1",
                organization_name="orgtest",
                hacker_email="test1@gmail.com",
                id="be09edb7-cd5c-47ed-bee4-97c645acdce16",
                state=VulnerabilityState(
                    modified_by="test1@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-04-08T00:45:15+00:00"
                    ),
                    source=Source.ASM,
                    specific="9999",
                    status=VulnerabilityStateStatus.VULNERABLE,
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
    ]
    vulnerabilities.extend(generic_data["db_data"]["vulnerabilities"])
    return await db.populate(
        {**generic_data["db_data"], "vulnerabilities": vulnerabilities}
    )
