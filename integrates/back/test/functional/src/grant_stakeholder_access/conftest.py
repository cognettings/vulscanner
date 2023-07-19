# pylint: disable=import-error
from back.test import (
    db,
)
from collections import (
    defaultdict,
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
)
from db_model.findings.types import (
    CVSS31Severity,
    Finding,
    FindingState,
    FindingUnreliableIndicatorsToUpdate,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupManaged,
    GroupService,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupState,
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


@pytest.mark.resolver_test_group("grant_stakeholder_access")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "groups": [
            {
                "group": Group(
                    created_by="unknown",
                    created_date=datetime.fromisoformat(
                        "2020-05-20T22:00:00+00:00"
                    ),
                    description="-",
                    language=GroupLanguage.EN,
                    name="group13",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="unknown",
                        modified_date=datetime.fromisoformat(
                            "2020-05-20T23:00:00+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    sprint_start_date=datetime.fromisoformat(
                        "2022-06-06T00:00:00+00:00"
                    ),
                ),
            },
        ],
        "findings": [
            {
                "finding": Finding(
                    id="087e80d6-692a-4a03-82d8-bf78fcdd4174",
                    group_name="group13",
                    state=FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="007. Cross-site request forgery",
                    recommendation="Hacer uso de tokens en los formularios "
                    "para la verificación de las peticiones realizadas por "
                    "usuarios legítimos.",
                    requirements="REQ.0174. La aplicación debe garantizar que "
                    "las peticiones que ejecuten transacciones no sigan un "
                    "patrón discernible.",
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
                        cvss_v3="CVSS:3.1/AV:A/AC:H/PR:L/UI:R/S:U/C:H/I:L/A:N/"
                        "E:U/RL:O/RC:R/IR:H/MAV:A/MAC:H/MPR:L/MUI:R/MS:U/MC:H/"
                        "MI:L",
                        cvssf=Decimal("1.516"),
                    ),
                    description="I just have updated the description",
                    hacker_email="test1@gmail.com",
                    threat="Updated threat",
                    attack_vector_description=(
                        "This is an updated attack vector"
                    ),
                ),
                "historic_state": [
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-04-08T00:45:12+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2021-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                    ),
                ],
                "historic_verification": [],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
                    unreliable_closed_vulnerabilities=0,
                    unreliable_open_vulnerabilities=1,
                    unreliable_newest_vulnerability_report_date=(
                        datetime.fromisoformat("2019-12-26T05:45:00+00:00")
                    ),
                    unreliable_oldest_open_vulnerability_report_date=(
                        datetime.fromisoformat("2019-02-24T05:45:00+00:00")
                    ),
                    unreliable_oldest_vulnerability_report_date=(
                        datetime.fromisoformat("2019-04-01T05:45:00+00:00")
                    ),
                    unreliable_status=FindingStatus.VULNERABLE,
                    unreliable_where="192.168.1.21",
                ),
            },
        ],
        "vulnerabilities": [
            {
                "vulnerability": Vulnerability(
                    created_by=generic_data["global_vars"]["hacker_email"],
                    created_date=datetime.fromisoformat(
                        "2021-04-08T00:45:14+00:00"
                    ),
                    finding_id="087e80d6-692a-4a03-82d8-bf78fcdd4174",
                    group_name="group13",
                    organization_name="orgtest",
                    hacker_email=generic_data["global_vars"]["hacker_email"],
                    id="be09edb7-cd5c-47ed-bee4-97c645acdce8",
                    state=VulnerabilityState(
                        modified_by=generic_data["global_vars"][
                            "hacker_email"
                        ],
                        modified_date=datetime.fromisoformat(
                            "2021-04-08T00:45:14+00:00"
                        ),
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.SAFE,
                        where="192.168.1.20",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2021-04-08T00:45:15+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                )
            },
        ],
    }

    merge_dict = defaultdict(list)
    for dict_data in (generic_data["db_data"], data):
        for key, value in dict_data.items():
            if key == "groups":
                merge_dict[key] = value
            else:
                merge_dict[key].extend(value)

    return await db.populate(merge_dict)
