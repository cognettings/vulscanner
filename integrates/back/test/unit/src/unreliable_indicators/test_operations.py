from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    FindingStatus,
)
from db_model.findings.types import (
    FindingTreatmentSummary,
    FindingUnreliableIndicators,
)
from db_model.vulnerabilities.types import (
    VulnerabilityUnreliableIndicators,
)
from decimal import (
    Decimal,
)
from freezegun.api import (
    freeze_time,
)
import pytest
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@freeze_time("2020-12-01")
async def test_update_unreliable_indicators_by_deps() -> None:
    loaders = get_new_context()
    finding_id = "422286126"
    vulnerability_id = "15375781-31f2-4953-ac77-f31134225747"
    await update_unreliable_indicators_by_deps(
        EntityDependency.upload_file,
        finding_ids=[finding_id],
        vulnerability_ids=[vulnerability_id],
    )
    expected_finding_output = FindingUnreliableIndicators(
        unreliable_closed_vulnerabilities=0,
        unreliable_max_open_severity_score=Decimal("4.9"),
        unreliable_open_vulnerabilities=1,
        unreliable_newest_vulnerability_report_date=(
            datetime.fromisoformat("2020-01-03T17:46:10+00:00")
        ),
        unreliable_oldest_open_vulnerability_report_date=(
            datetime.fromisoformat("2020-01-03T17:46:10+00:00")
        ),
        unreliable_oldest_vulnerability_report_date=(
            datetime.fromisoformat("2020-01-03T17:46:10+00:00")
        ),
        unreliable_rejected_vulnerabilities=1,
        unreliable_status=FindingStatus.VULNERABLE,
        unreliable_submitted_vulnerabilities=1,
        unreliable_total_open_cvssf=Decimal("3.482"),
        unreliable_treatment_summary=FindingTreatmentSummary(
            accepted=0,
            accepted_undefined=0,
            in_progress=1,
            untreated=0,
        ),
        unreliable_where="test/data/lib_path/f060/csharp.cs",
        open_vulnerabilities=1,
        closed_vulnerabilities=0,
        submitted_vulnerabilities=1,
        rejected_vulnerabilities=1,
        max_open_severity_score=Decimal("4.9"),
        newest_vulnerability_report_date=(
            datetime.fromisoformat("2020-01-03T17:46:10+00:00")
        ),
        oldest_vulnerability_report_date=(
            datetime.fromisoformat("2020-01-03T17:46:10+00:00")
        ),
        treatment_summary=FindingTreatmentSummary(
            accepted=0,
            accepted_undefined=0,
            in_progress=1,
            untreated=0,
        ),
    )
    finding = await loaders.finding.load(finding_id)
    assert finding
    assert finding.unreliable_indicators == expected_finding_output
    vulnerability = await loaders.vulnerability.load(vulnerability_id)
    assert vulnerability
    expected_vulnerability_output = VulnerabilityUnreliableIndicators(
        unreliable_efficacy=Decimal("0"),
        unreliable_last_reattack_date=datetime.fromisoformat(
            "2020-02-19T15:41:04+00:00"
        ),
        unreliable_last_reattack_requester="integratesuser@gmail.com",
        unreliable_last_requested_reattack_date=datetime.fromisoformat(
            "2020-02-18T15:41:04+00:00"
        ),
        unreliable_report_date=datetime.fromisoformat(
            "2019-09-13T13:17:41+00:00"
        ),
        unreliable_reattack_cycles=1,
        unreliable_source=Source.ASM,
        unreliable_treatment_changes=0,
    )
    assert vulnerability.unreliable_indicators == expected_vulnerability_output
