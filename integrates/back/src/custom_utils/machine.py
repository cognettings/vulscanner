from custom_utils import (
    cvss as cvss_utils,
)
from db_model.findings.types import (
    Finding,
)
from typing import (
    Any,
)


def has_machine_description(
    finding: Finding, criteria_vulnerability: dict[str, Any], language: str
) -> bool:
    return all(
        (
            finding.description.strip()
            == criteria_vulnerability[language]["description"].strip(),
            finding.threat.strip()
            == criteria_vulnerability[language]["threat"].strip(),
            finding.severity_score.cvss_v3
            == cvss_utils.get_criteria_cvss_vector(criteria_vulnerability),
        )
    )
