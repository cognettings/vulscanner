from model import (
    cvss3,
)
import pytest


@pytest.mark.skims_test_group("unittesting")
def test_find_score_data() -> None:
    score_data_001 = cvss3.find_score_data("001")
    assert score_data_001 == cvss3.Score(
        attack_complexity=cvss3.AttackComplexity.L,
        attack_vector=cvss3.AttackVector.N,
        availability_impact=cvss3.AvailabilityImpact.N,
        confidentiality_impact=cvss3.ConfidentialityImpact.N,
        exploitability=cvss3.Exploitability.U,
        integrity_impact=cvss3.IntegrityImpact.L,
        privileges_required=cvss3.PrivilegesRequired.L,
        remediation_level=cvss3.RemediationLevel.O,
        report_confidence=cvss3.ReportConfidence.C,
        severity_scope=cvss3.SeverityScope.U,
        user_interaction=cvss3.UserInteraction.N,
    )

    score_data_172 = cvss3.find_score_data("172")
    assert score_data_172 == cvss3.Score(
        attack_complexity=cvss3.AttackComplexity.H,
        attack_vector=cvss3.AttackVector.L,
        availability_impact=cvss3.AvailabilityImpact.N,
        confidentiality_impact=cvss3.ConfidentialityImpact.L,
        exploitability=cvss3.Exploitability.X,
        integrity_impact=cvss3.IntegrityImpact.N,
        privileges_required=cvss3.PrivilegesRequired.N,
        remediation_level=cvss3.RemediationLevel.O,
        report_confidence=cvss3.ReportConfidence.X,
        severity_scope=cvss3.SeverityScope.U,
        user_interaction=cvss3.UserInteraction.N,
    )

    score_data_402 = cvss3.find_score_data("402")
    assert score_data_402 == cvss3.Score(
        attack_complexity=cvss3.AttackComplexity.H,
        attack_vector=cvss3.AttackVector.N,
        availability_impact=cvss3.AvailabilityImpact.N,
        confidentiality_impact=cvss3.ConfidentialityImpact.N,
        exploitability=cvss3.Exploitability.U,
        integrity_impact=cvss3.IntegrityImpact.L,
        privileges_required=cvss3.PrivilegesRequired.L,
        remediation_level=cvss3.RemediationLevel.O,
        report_confidence=cvss3.ReportConfidence.R,
        severity_scope=cvss3.SeverityScope.U,
        user_interaction=cvss3.UserInteraction.N,
    )
