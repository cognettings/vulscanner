from enum import (
    Enum,
)
from model.core import (
    LocalesEnum,
)
from typing import (
    Any,
    NamedTuple,
)
from zone import (
    t,
)


class AttackComplexity(Enum):
    L: float = 0.77
    H: float = 0.44


class AttackVector(Enum):
    P: float = 0.20
    L: float = 0.55
    A: float = 0.62
    N: float = 0.85


class AvailabilityImpact(Enum):
    N: float = 0.00
    L: float = 0.22
    H: float = 0.56


class ConfidentialityImpact(Enum):
    N: float = 0.00
    L: float = 0.22
    H: float = 0.56


class Exploitability(Enum):
    U: float = 0.91
    P: float = 0.94
    X: float = 0.94
    F: float = 0.97
    H: float = 1.0


class IntegrityImpact(Enum):
    N: float = 0.00
    L: float = 0.22
    H: float = 0.56


class PrivilegesRequired(Enum):
    N: float = 0.85
    L: float = 0.62
    H: float = 0.27


class RemediationLevel(Enum):
    O: float = 0.95
    T: float = 0.96
    W: float = 0.97
    U: float = 1.00
    X: float = 1.00


class ReportConfidence(Enum):
    U: float = 0.92
    R: float = 0.96
    C: float = 1.00
    X: float = 1.00


class SeverityScope(Enum):
    U: float = 0.0
    C: float = 1.0


class UserInteraction(Enum):
    R: float = 0.62
    N: float = 0.85


class Score(NamedTuple):
    attack_complexity: AttackComplexity
    attack_vector: AttackVector
    availability_impact: AvailabilityImpact
    confidentiality_impact: ConfidentialityImpact
    exploitability: Exploitability
    integrity_impact: IntegrityImpact
    privileges_required: PrivilegesRequired
    remediation_level: RemediationLevel
    report_confidence: ReportConfidence
    severity_scope: SeverityScope
    user_interaction: UserInteraction

    def as_dict(self) -> dict[str, Any]:
        return dict(
            attackComplexity=str(self.attack_complexity.value),
            attackVector=str(self.attack_vector.value),
            availabilityImpact=str(self.availability_impact.value),
            confidentialityImpact=str(self.confidentiality_impact.value),
            exploitability=str(self.exploitability.value),
            integrityImpact=str(self.integrity_impact.value),
            privilegesRequired=str(self.privileges_required.value),
            remediationLevel=str(self.remediation_level.value),
            reportConfidence=str(self.report_confidence.value),
            severityScope=str(self.severity_scope.value),
            userInteraction=str(self.user_interaction.value),
            # Values below are not shown on Integrates
            # Let's copy them from the temporal scoring
            availabilityRequirement=str(0.0),
            confidentialityRequirement=str(0.0),
            integrityRequirement=str(0.0),
            modifiedAttackComplexity=str(self.attack_complexity.value),
            modifiedAttackVector=str(self.attack_vector.value),
            modifiedAvailabilityImpact=str(self.availability_impact.value),
            modifiedConfidentialityImpact=str(
                self.confidentiality_impact.value
            ),
            modifiedIntegrityImpact=str(self.integrity_impact.value),
            modifiedPrivilegesRequired=str(self.privileges_required.value),
            modifiedUserInteraction=str(self.user_interaction.value),
            modifiedSeverityScope=str(self.severity_scope.value),
        )

    def score_to_vector_string(self) -> str:
        attack_vector = self.attack_vector.name
        attack_complexity = self.attack_complexity.name
        privileges_required = self.privileges_required.name
        user_interaction = self.user_interaction.name
        severity = self.severity_scope.name
        confidentiality = self.confidentiality_impact.name
        integrity = self.integrity_impact.name
        availability = self.availability_impact.name
        exploitability = self.exploitability.name
        remediation_level = self.remediation_level.name
        report_confidence = self.report_confidence.name
        return (
            f"CVSS:3.1/AV:{attack_vector}/AC:{attack_complexity}"
            f"/PR:{privileges_required}/UI:{user_interaction}"
            f"/S:{severity}/C:{confidentiality}/I:{integrity}"
            f"/A:{availability}/E:{exploitability}/RL:{remediation_level}"
            f"/RC:{report_confidence}"
        )


def find_score_data(code: str) -> Score:
    return Score(
        attack_complexity=AttackComplexity[
            t(
                f"criteria.vulns.{code}.attack_complexity",
                locale=LocalesEnum.EN,
            )
        ],
        attack_vector=AttackVector[
            t(
                f"criteria.vulns.{code}.attack_vector",
                locale=LocalesEnum.EN,
            )
        ],
        availability_impact=AvailabilityImpact[
            t(
                f"criteria.vulns.{code}.availability",
                locale=LocalesEnum.EN,
            )
        ],
        confidentiality_impact=ConfidentialityImpact[
            t(
                f"criteria.vulns.{code}.confidentiality",
                locale=LocalesEnum.EN,
            )
        ],
        exploitability=Exploitability[
            t(
                f"criteria.vulns.{code}.exploit_code_maturity",
                locale=LocalesEnum.EN,
            )
        ],
        integrity_impact=IntegrityImpact[
            t(
                f"criteria.vulns.{code}.integrity",
                locale=LocalesEnum.EN,
            )
        ],
        privileges_required=PrivilegesRequired[
            t(
                f"criteria.vulns.{code}.privileges_required",
                locale=LocalesEnum.EN,
            )
        ],
        remediation_level=RemediationLevel[
            t(
                f"criteria.vulns.{code}.remediation_level",
                locale=LocalesEnum.EN,
            )
        ],
        report_confidence=ReportConfidence[
            t(
                f"criteria.vulns.{code}.report_confidence",
                locale=LocalesEnum.EN,
            )
        ],
        severity_scope=SeverityScope[
            t(
                f"criteria.vulns.{code}.scope",
                locale=LocalesEnum.EN,
            )
        ],
        user_interaction=UserInteraction[
            t(
                f"criteria.vulns.{code}.user_interaction",
                locale=LocalesEnum.EN,
            )
        ],
    )
