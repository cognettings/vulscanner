from collections.abc import (
    Iterable,
)
from custom_exceptions import (
    InvalidCVSS3VectorString,
    InvalidSeverityCweIds,
    InvalidSeverityUpdateValues,
)
from cvss import (
    CVSS3,
    CVSS3Error,
)
from db_model.findings.enums import (
    AttackComplexity,
    AttackVector,
    AvailabilityImpact,
    AvailabilityRequirement,
    ConfidentialityImpact,
    ConfidentialityRequirement,
    Exploitability,
    IntegrityImpact,
    IntegrityRequirement,
    PrivilegesRequiredScopeChanged,
    PrivilegesRequiredScopeUnchanged,
    RemediationLevel,
    ReportConfidence,
    SeverityScope,
    UserInteraction,
)
from db_model.findings.types import (
    CVSS31Severity,
    CVSS31SeverityParameters,
    Finding,
)
from db_model.types import (
    SeverityScore,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from dynamodb.types import (
    Item,
)
import math
import re

DEFAULT_CVSS_31_PARAMETERS = CVSS31SeverityParameters(
    base_score_factor=Decimal("1.08"),
    exploitability_factor_1=Decimal("8.22"),
    impact_factor_1=Decimal("6.42"),
    impact_factor_2=Decimal("7.52"),
    impact_factor_3=Decimal("0.029"),
    impact_factor_4=Decimal("3.25"),
    impact_factor_5=Decimal("0.02"),
    impact_factor_6=Decimal("15"),
    mod_impact_factor_1=Decimal("0.915"),
    mod_impact_factor_2=Decimal("6.42"),
    mod_impact_factor_3=Decimal("7.52"),
    mod_impact_factor_4=Decimal("0.029"),
    mod_impact_factor_5=Decimal("3.25"),
    mod_impact_factor_6=Decimal("0.02"),
    mod_impact_factor_7=Decimal("13"),
    mod_impact_factor_8=Decimal("0.9731"),
)
NOT_DEFINED = "X"


def get_f_impact(impact: Decimal) -> Decimal:
    if impact:
        f_impact_factor = Decimal("1.176")
    else:
        f_impact_factor = Decimal("0.0")

    return f_impact_factor


def get_cvss31_base_score(
    severity: CVSS31Severity,
    parameters: CVSS31SeverityParameters = DEFAULT_CVSS_31_PARAMETERS,
) -> Decimal:
    """
    Calculate cvss 3.1 base score attribute. Adjustment for Privileges Required
    metric is done according to the CVSS 3.1 spec.
    """
    severity = adjust_privileges_required(severity)
    iss = 1 - (
        (1 - severity.confidentiality_impact)
        * (1 - severity.integrity_impact)
        * (1 - severity.availability_impact)
    )
    if severity.severity_scope:
        impact = (
            parameters.impact_factor_2 * (iss - parameters.impact_factor_3)
        ) - (
            parameters.impact_factor_4
            * (iss - parameters.impact_factor_5) ** parameters.impact_factor_6
        )
    else:
        impact = parameters.impact_factor_1 * iss
    exploitability = (
        parameters.exploitability_factor_1
        * severity.attack_vector
        * severity.attack_complexity
        * severity.privileges_required
        * severity.user_interaction
    )
    if impact <= 0:
        base_score = Decimal(0)
    else:
        if severity.severity_scope:
            base_score = Decimal(
                math.ceil(
                    min(
                        float(
                            parameters.base_score_factor
                            * (impact + exploitability)
                        ),
                        10,
                    )
                    * 10
                )
                / 10
            )
        else:
            base_score = Decimal(
                math.ceil(min(float(impact + exploitability), 10) * 10) / 10
            )

    return base_score.quantize(Decimal("0.1"))


def get_cvss31_temporal(
    severity: CVSS31Severity, base_score: Decimal
) -> Decimal:
    """Calculate cvss 3.1 temporal attribute."""
    temporal = Decimal(
        math.ceil(
            base_score
            * severity.exploitability
            * severity.remediation_level
            * severity.report_confidence
            * 10
        )
        / 10
    )

    return temporal.quantize(Decimal("0.1"))


def _calculate_privileges(privileges: Decimal, scope: Decimal) -> Decimal:
    """
    Calculate Privileges Required metric according to
    https://www.first.org/cvss/specification-document#7-4-Metric-Values.
    """
    if scope:  # Changed
        if privileges == Decimal("0.62"):
            privileges = Decimal("0.68")
        elif privileges == Decimal("0.27"):
            privileges = Decimal("0.5")
    else:  # Unchanged
        if privileges == Decimal("0.68"):
            privileges = Decimal("0.62")
        elif privileges == Decimal("0.5"):
            privileges = Decimal("0.27")

    return Decimal(privileges).quantize(Decimal("0.01"))


def adjust_privileges_required(severity: CVSS31Severity) -> CVSS31Severity:
    """
    Adjusment made to the metric in accordance to official documentation
    https://www.first.org/cvss/specification-document#7-4-Metric-Values.
    """
    return severity._replace(
        privileges_required=_calculate_privileges(
            severity.privileges_required,
            severity.severity_scope,
        ),
        modified_privileges_required=_calculate_privileges(
            severity.modified_privileges_required,
            severity.modified_severity_scope,
        ),
    )


def get_severity_score(severity: CVSS31Severity) -> Decimal:
    base_score = get_cvss31_base_score(severity)
    return get_cvss31_temporal(severity, base_score)


def get_severity_level(severity: Decimal) -> str:
    """
    Qualitative severity rating scale as defined in
    https://www.first.org/cvss/v3.1/specification-document section 5.
    """
    if severity < 4:
        return "low"
    if 4 <= severity < 7:
        return "medium"
    if 7 <= severity < 9:
        return "high"

    return "critical"


def get_cvssf_score(temporal_score: Decimal) -> Decimal:
    return Decimal(
        pow(Decimal("4.0"), temporal_score - Decimal("4.0"))
    ).quantize(Decimal("0.001"))


def get_vulnerabilities_score(
    finding: Finding,
    vulnerabilities: Iterable[Vulnerability],
    status: VulnerabilityStateStatus = VulnerabilityStateStatus.VULNERABLE,
) -> Decimal:
    finding_score = (
        finding.severity_score.temporal_score
        if finding.severity_score
        else Decimal(0)
    )
    return max(
        (
            vulnerability.severity_score.temporal_score
            if vulnerability.severity_score
            else finding_score
            for vulnerability in vulnerabilities
            if vulnerability.state.status == status
        ),
        default=finding_score,
    )


def validate_cvss_vector(vector_string: str) -> None:
    try:
        CVSS3(vector_string)
    except CVSS3Error as ex:
        raise InvalidCVSS3VectorString.new() from ex


def parse_cvss_vector_string(  # NOSONAR
    vector_string: str,
) -> CVSS31Severity:
    try:
        cvss3 = CVSS3(vector_string)
        vector_string = cvss3.clean_vector()
    except CVSS3Error as ex:
        raise InvalidCVSS3VectorString() from ex

    cvss_vector = {
        metric.split(":")[0]: metric.split(":")[1]
        for metric in vector_string.split("/")
        if metric not in {"CVSS:3.1"}
    }

    try:
        if cvss_vector["S"] == "C":
            privileges_required = PrivilegesRequiredScopeChanged[
                cvss_vector["PR"]
            ].value
        else:
            privileges_required = PrivilegesRequiredScopeUnchanged[
                cvss_vector["PR"]
            ].value
        modified_privileges_required = Decimal("0.0")
        if cvss_vector.get("MPR"):
            if cvss_vector.get("MS") and cvss_vector["MS"] == "C":
                modified_privileges_required = PrivilegesRequiredScopeChanged[
                    cvss_vector["MPR"]
                ].value
            else:
                modified_privileges_required = (
                    PrivilegesRequiredScopeUnchanged[cvss_vector["MPR"]].value
                )

        return CVSS31Severity(
            # Base. Mandatory: YES
            attack_vector=AttackVector[cvss_vector["AV"]].value,
            attack_complexity=AttackComplexity[cvss_vector["AC"]].value,
            privileges_required=privileges_required,
            user_interaction=UserInteraction[cvss_vector["UI"]].value,
            severity_scope=SeverityScope[cvss_vector["S"]].value,
            confidentiality_impact=ConfidentialityImpact[
                cvss_vector["C"]
            ].value,
            integrity_impact=IntegrityImpact[cvss_vector["I"]].value,
            availability_impact=AvailabilityImpact[cvss_vector["A"]].value,
            # Temporal. Mandatory: NO
            exploitability=Exploitability[cvss_vector["E"]].value
            if cvss_vector.get("E")
            else Exploitability.X.value,
            remediation_level=RemediationLevel[cvss_vector["RL"]].value
            if cvss_vector.get("RL")
            else RemediationLevel.X.value,
            report_confidence=ReportConfidence[cvss_vector["RC"]].value
            if cvss_vector.get("RC")
            else ReportConfidence.X.value,
            # Environmantal. Mandatory: NO
            confidentiality_requirement=ConfidentialityRequirement[
                cvss_vector["CR"]
            ].value
            if cvss_vector.get("CR")
            else Decimal("0.0"),
            integrity_requirement=IntegrityRequirement[cvss_vector["IR"]].value
            if cvss_vector.get("IR")
            else Decimal("0.0"),
            availability_requirement=AvailabilityRequirement[
                cvss_vector["AR"]
            ].value
            if cvss_vector.get("AR")
            else Decimal("0.0"),
            modified_attack_vector=AttackVector[cvss_vector["MAV"]].value
            if cvss_vector.get("MAV")
            else Decimal("0.0"),
            modified_attack_complexity=AttackComplexity[
                cvss_vector["MAC"]
            ].value
            if cvss_vector.get("MAC")
            else Decimal("0.0"),
            modified_privileges_required=modified_privileges_required,
            modified_user_interaction=UserInteraction[cvss_vector["MUI"]].value
            if cvss_vector.get("MUI")
            else Decimal("0.0"),
            modified_severity_scope=SeverityScope[cvss_vector["MS"]].value
            if cvss_vector.get("MS")
            else Decimal("0.0"),
            modified_confidentiality_impact=ConfidentialityImpact[
                cvss_vector["MC"]
            ].value
            if cvss_vector.get("MC")
            else Decimal("0.0"),
            modified_integrity_impact=IntegrityImpact[cvss_vector["MI"]].value
            if cvss_vector.get("MI")
            else Decimal("0.0"),
            modified_availability_impact=AvailabilityImpact[
                cvss_vector["MA"]
            ].value
            if cvss_vector.get("MA")
            else Decimal("0.0"),
        )
    except KeyError as ex:
        raise InvalidCVSS3VectorString() from ex


def parse_cvss31_severity_legacy(severity: CVSS31Severity) -> str:  # NOSONAR
    try:
        privileges_required = (
            PrivilegesRequiredScopeChanged(severity.privileges_required).name
            if severity.privileges_required
            in [item.value for item in PrivilegesRequiredScopeChanged]
            else PrivilegesRequiredScopeUnchanged(
                severity.privileges_required
            ).name
        )
        modified_privileges_required = NOT_DEFINED
        if severity.modified_privileges_required:
            modified_privileges_required = (
                PrivilegesRequiredScopeChanged(
                    severity.modified_privileges_required
                ).name
                if severity.modified_privileges_required
                in [item.value for item in PrivilegesRequiredScopeChanged]
                else PrivilegesRequiredScopeUnchanged(
                    severity.modified_privileges_required
                ).name
            )
        modified_severity_scope = NOT_DEFINED
        if severity.modified_privileges_required:
            modified_severity_scope = SeverityScope(
                severity.modified_severity_scope
            ).name
        vector_translated = {
            # Base. Mandatory: YES
            "AV": AttackVector(severity.attack_vector).name,
            "AC": AttackComplexity(severity.attack_complexity).name,
            "PR": privileges_required,
            "UI": UserInteraction(severity.user_interaction).name,
            "S": SeverityScope(severity.severity_scope).name,
            "C": ConfidentialityImpact(severity.confidentiality_impact).name,
            "I": IntegrityImpact(severity.integrity_impact).name,
            "A": AvailabilityImpact(severity.availability_impact).name,
            # Temporal. Mandatory: NO
            "E": Exploitability(severity.exploitability).name
            if severity.exploitability
            else NOT_DEFINED,
            "RL": RemediationLevel(severity.remediation_level).name
            if severity.remediation_level
            else NOT_DEFINED,
            "RC": ReportConfidence(severity.report_confidence).name
            if severity.report_confidence
            else NOT_DEFINED,
            # Environmantal. Mandatory: NO
            "CR": ConfidentialityRequirement(
                severity.confidentiality_requirement
            ).name
            if severity.confidentiality_requirement
            else NOT_DEFINED,
            "IR": IntegrityRequirement(severity.integrity_requirement).name
            if severity.integrity_requirement
            else NOT_DEFINED,
            "AR": AvailabilityRequirement(
                severity.availability_requirement
            ).name
            if severity.availability_requirement
            else NOT_DEFINED,
            "MAV": AttackVector(severity.modified_attack_vector).name
            if severity.modified_attack_vector
            else NOT_DEFINED,
            "MAC": AttackComplexity(severity.modified_attack_complexity).name
            if severity.modified_attack_complexity
            else NOT_DEFINED,
            "MPR": modified_privileges_required,
            "MUI": UserInteraction(severity.modified_user_interaction).name
            if severity.modified_user_interaction
            else NOT_DEFINED,
            "MS": modified_severity_scope,
            "MC": ConfidentialityImpact(
                severity.modified_confidentiality_impact
            ).name
            if severity.modified_confidentiality_impact
            else NOT_DEFINED,
            "MI": IntegrityImpact(severity.modified_integrity_impact).name
            if severity.modified_integrity_impact
            else NOT_DEFINED,
            "MA": AvailabilityImpact(
                severity.modified_availability_impact
            ).name
            if severity.modified_availability_impact
            else NOT_DEFINED,
        }
    except ValueError as ex:
        raise InvalidSeverityUpdateValues() from ex

    vector_string = "CVSS:3.1"
    for key, value in vector_translated.items():
        vector_string += f"/{key}:{value}"

    try:
        cvss3 = CVSS3(vector_string)
        return cvss3.clean_vector()
    except CVSS3Error as ex:
        raise InvalidCVSS3VectorString() from ex


def parse_cwe_ids(raw_list: Iterable[str] | None) -> list[str] | None:
    if not raw_list:
        return None

    pattern = r"^CWE-\d{1,4}$"
    if not all(re.match(pattern, id) for id in raw_list):
        raise InvalidSeverityCweIds()

    return sorted(list(set(raw_list)))


def get_severity_score_summary(severity: CVSS31Severity) -> SeverityScore:
    base_score = get_cvss31_base_score(severity)
    temporal_score = get_cvss31_temporal(severity, base_score)

    return SeverityScore(
        base_score=base_score,
        temporal_score=temporal_score,
        cvssf=get_cvssf_score(temporal_score),
    )


def get_severity_score_from_cvss_vector(vector: str) -> SeverityScore:
    try:
        cvss3 = CVSS3(vector)
        base_score = cvss3.base_score
        temporal_score = cvss3.temporal_score

        return SeverityScore(
            base_score=base_score,
            temporal_score=temporal_score,
            cvss_v3=cvss3.clean_vector(),
            cvssf=get_cvssf_score(temporal_score),
        )
    except CVSS3Error as ex:
        raise InvalidCVSS3VectorString() from ex


def get_criteria_cvss_vector(criteria_vulnerability: Item) -> str:
    base = criteria_vulnerability["score"]["base"]
    temporal = criteria_vulnerability["score"]["temporal"]
    vector_string = (
        f'CVSS:3.1/AV:{base["attack_vector"]}'
        f'/AC:{base["attack_complexity"]}'
        f'/PR:{base["privileges_required"]}'
        f'/UI:{base["user_interaction"]}'
        f'/S:{base["scope"]}'
        f'/C:{base["confidentiality"]}'
        f'/I:{base["integrity"]}'
        f'/A:{base["availability"]}'
        f'/E:{temporal["exploit_code_maturity"]}'
        f'/RL:{temporal["remediation_level"]}'
        f'/RC:{temporal["report_confidence"]}'
    )
    try:
        cvss3 = CVSS3(vector_string)
    except CVSS3Error as ex:
        raise InvalidCVSS3VectorString() from ex

    return cvss3.clean_vector()
