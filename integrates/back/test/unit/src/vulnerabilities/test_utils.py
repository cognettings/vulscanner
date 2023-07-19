from dataloaders import (
    Dataloaders,
    get_new_context,
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
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from db_model.vulnerabilities.types import (
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from db_model.vulnerabilities.utils import (
    get_group_index_key,
    get_new_group_index_key,
)
from dynamodb.types import (
    PrimaryKey,
)
import pytest


@pytest.mark.asyncio
async def test_group_index_utils() -> None:
    loaders: Dataloaders = get_new_context()

    current_value = await loaders.vulnerability.load(
        "15375781-31f2-4953-ac77-f31134225747"
    )
    assert current_value
    assert get_group_index_key(current_value) == PrimaryKey(
        partition_key="GROUP#unittesting",
        sort_key="VULN#ZR#false#STATE#vulnerable#TREAT#false",
    )

    new_state = VulnerabilityState(
        modified_by="test@unittesting.com",
        modified_date=datetime.fromisoformat("2023-03-14T00:45:15+00:00"),
        source=Source.ASM,
        specific="2321",
        status=VulnerabilityStateStatus.SAFE,
        where="192.168.1.2",
    )
    assert get_new_group_index_key(current_value, new_state) == PrimaryKey(
        partition_key="GROUP#unittesting",
        sort_key="VULN#ZR#false#STATE#safe#TREAT#false",
    )

    new_accepted_treatment = VulnerabilityTreatment(
        modified_date=datetime.fromisoformat("2023-03-14T00:45:15+00:00"),
        status=VulnerabilityTreatmentStatus.ACCEPTED,
    )
    assert get_new_group_index_key(
        current_value, new_accepted_treatment
    ) == PrimaryKey(
        partition_key="GROUP#unittesting",
        sort_key="VULN#ZR#false#STATE#vulnerable#TREAT#true",
    )

    new_permanent_treatment = VulnerabilityTreatment(
        modified_date=datetime.fromisoformat("2023-03-14T00:45:15+00:00"),
        status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
    )
    assert get_new_group_index_key(
        current_value, new_permanent_treatment
    ) == PrimaryKey(
        partition_key="GROUP#unittesting",
        sort_key="VULN#ZR#false#STATE#vulnerable#TREAT#true",
    )

    new_verification = VulnerabilityVerification(
        modified_date=datetime.fromisoformat("2023-03-14T00:45:15+00:00"),
        status=VulnerabilityVerificationStatus.VERIFIED,
        event_id=None,
    )
    assert get_new_group_index_key(current_value, new_verification) is None

    new_requested_zero_risk = VulnerabilityZeroRisk(
        comment_id="123456",
        modified_by="test@gmail.com",
        modified_date=datetime.fromisoformat("2023-03-14T00:45:15+00:00"),
        status=VulnerabilityZeroRiskStatus.REQUESTED,
    )
    assert get_new_group_index_key(
        current_value, new_requested_zero_risk
    ) == PrimaryKey(
        partition_key="GROUP#unittesting",
        sort_key="VULN#ZR#true#STATE#vulnerable#TREAT#false",
    )

    new_confirmed_zero_risk = VulnerabilityZeroRisk(
        comment_id="123456",
        modified_by="test@gmail.com",
        modified_date=datetime.fromisoformat("2023-03-14T00:45:15+00:00"),
        status=VulnerabilityZeroRiskStatus.CONFIRMED,
    )
    assert get_new_group_index_key(
        current_value, new_confirmed_zero_risk
    ) == PrimaryKey(
        partition_key="GROUP#unittesting",
        sort_key="VULN#ZR#true#STATE#vulnerable#TREAT#false",
    )
