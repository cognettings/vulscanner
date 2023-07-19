from custom_exceptions import (
    InvalidCVSS3VectorString,
    InvalidSeverityCweIds,
)
from custom_utils import (
    cvss as cvss_utils,
    utils,
)
from cvss import (
    CVSS3,
)
from db_model.findings.types import (
    CVSS31Severity,
)
from decimal import (
    Decimal,
)
from dynamodb.types import (
    Item,
)
import pytest


def format_severity(severity: dict[str, float]) -> dict[str, Decimal]:
    return {
        utils.camelcase_to_snakecase(key): Decimal(value)
        for key, value in severity.items()
    }


def test_calculate_cvss3_scope_changed_base_score() -> None:
    severity_dict = {
        "confidentialityImpact": 0.22,
        "integrityImpact": 0.22,
        "availabilityImpact": 0,
        "severityScope": 1,
        "attackVector": 0.85,
        "attackComplexity": 0.77,
        "privilegesRequired": 0.68,
        "userInteraction": 0.85,
    }
    cvss_base_score_test = Decimal(6.4).quantize(Decimal("0.1"))
    severity = CVSS31Severity(**format_severity(severity_dict))
    cvss_base_score = cvss_utils.get_cvss31_base_score(severity)
    assert cvss_base_score == cvss_base_score_test


def test_calculate_cvss3_scope_unchanged_base_score() -> None:
    severity_dict = {
        "confidentialityImpact": 0.22,
        "integrityImpact": 0.22,
        "availabilityImpact": 0,
        "severityScope": 0,
        "attackVector": 0.85,
        "attackComplexity": 0.77,
        "privilegesRequired": 0.62,
        "userInteraction": 0.85,
    }
    cvss_base_score_test = Decimal(5.4).quantize(Decimal("0.1"))
    severity = CVSS31Severity(**format_severity(severity_dict))
    cvss_base_score = cvss_utils.get_cvss31_base_score(severity)
    assert cvss_base_score == cvss_base_score_test


def test_calculate_cvss3_scope_changed_temporal() -> None:
    severity_dict = {
        "confidentialityImpact": 0.22,
        "integrityImpact": 0.22,
        "availabilityImpact": 0,
        "severityScope": 1,
        "attackVector": 0.85,
        "attackComplexity": 0.77,
        "privilegesRequired": 0.68,
        "userInteraction": 0.85,
        "exploitability": 0.97,
        "remediationLevel": 0.97,
        "reportConfidence": 1,
    }
    cvss_temporal_test = Decimal(6.1).quantize(Decimal("0.1"))
    severity = CVSS31Severity(**format_severity(severity_dict))
    cvss_base_score = cvss_utils.get_cvss31_base_score(severity)
    cvss_temporal = cvss_utils.get_cvss31_temporal(severity, cvss_base_score)
    assert cvss_temporal == cvss_temporal_test


def test_calculate_cvss3_scope_unchanged_temporal() -> None:
    severity_dict = {
        "confidentialityImpact": 0.22,
        "integrityImpact": 0.22,
        "availabilityImpact": 0,
        "severityScope": 0,
        "attackVector": 0.85,
        "attackComplexity": 0.77,
        "privilegesRequired": 0.62,
        "userInteraction": 0.85,
        "exploitability": 0.97,
        "remediationLevel": 0.97,
        "reportConfidence": 1,
    }
    cvss_temporal_test = Decimal(5.1).quantize(Decimal("0.1"))
    severity = CVSS31Severity(**format_severity(severity_dict))
    cvss_base_score = cvss_utils.get_cvss31_base_score(severity)
    cvss_temporal = cvss_utils.get_cvss31_temporal(severity, cvss_base_score)
    assert cvss_temporal == cvss_temporal_test


@pytest.mark.parametrize(
    ["vector_string", "cvss31_severity"],
    [
        [
            # Privilege escalation
            "CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H/E:X/RL:X/RC:X",
            CVSS31Severity(
                attack_complexity=Decimal("0.44"),
                attack_vector=Decimal("0.85"),
                availability_impact=Decimal("0.56"),
                availability_requirement=Decimal("0.0"),
                confidentiality_impact=Decimal("0.56"),
                confidentiality_requirement=Decimal("0.0"),
                exploitability=Decimal("1.0"),
                integrity_impact=Decimal("0.56"),
                integrity_requirement=Decimal("0.0"),
                modified_attack_complexity=Decimal("0.0"),
                modified_attack_vector=Decimal("0.0"),
                modified_availability_impact=Decimal("0.0"),
                modified_confidentiality_impact=Decimal("0.0"),
                modified_integrity_impact=Decimal("0.0"),
                modified_privileges_required=Decimal("0.0"),
                modified_user_interaction=Decimal("0.0"),
                modified_severity_scope=Decimal("0.0"),
                privileges_required=Decimal("0.5"),
                remediation_level=Decimal("1.00"),
                report_confidence=Decimal("1.00"),
                severity_scope=Decimal("1.0"),
                user_interaction=Decimal("0.85"),
            ),
        ],
        [
            # Privilege escalation - Environmental modified
            "CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H"
            "/CR:L/IR:M/AR:H/MAV:N",
            CVSS31Severity(
                attack_complexity=Decimal("0.44"),
                attack_vector=Decimal("0.85"),
                availability_impact=Decimal("0.56"),
                availability_requirement=Decimal("1.5"),
                confidentiality_impact=Decimal("0.56"),
                confidentiality_requirement=Decimal("0.5"),
                exploitability=Decimal("1.0"),
                integrity_impact=Decimal("0.56"),
                integrity_requirement=Decimal("1.0"),
                modified_attack_complexity=Decimal("0.0"),
                modified_attack_vector=Decimal("0.85"),
                modified_availability_impact=Decimal("0.0"),
                modified_confidentiality_impact=Decimal("0.0"),
                modified_integrity_impact=Decimal("0.0"),
                modified_privileges_required=Decimal("0.0"),
                modified_user_interaction=Decimal("0.0"),
                modified_severity_scope=Decimal("0.0"),
                privileges_required=Decimal("0.5"),
                remediation_level=Decimal("1.00"),
                report_confidence=Decimal("1.00"),
                severity_scope=Decimal("1.0"),
                user_interaction=Decimal("0.85"),
            ),
        ],
        [
            # Improper authentication for shared folders
            "CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N/E:H/RL:U/RC:C",
            CVSS31Severity(
                attack_complexity=Decimal("0.77"),
                attack_vector=Decimal("0.62"),
                availability_impact=Decimal("0.00"),
                availability_requirement=Decimal("0.0"),
                confidentiality_impact=Decimal("0.56"),
                confidentiality_requirement=Decimal("0.0"),
                exploitability=Decimal("1.0"),
                integrity_impact=Decimal("0.00"),
                integrity_requirement=Decimal("0.0"),
                modified_attack_complexity=Decimal("0.0"),
                modified_attack_vector=Decimal("0.0"),
                modified_availability_impact=Decimal("0.0"),
                modified_confidentiality_impact=Decimal("0.0"),
                modified_integrity_impact=Decimal("0.0"),
                modified_privileges_required=Decimal("0.0"),
                modified_user_interaction=Decimal("0.0"),
                modified_severity_scope=Decimal("0.0"),
                privileges_required=Decimal("0.62"),
                remediation_level=Decimal("1.00"),
                report_confidence=Decimal("1.00"),
                severity_scope=Decimal("0.0"),
                user_interaction=Decimal("0.85"),
            ),
        ],
        [
            # Improper authentication for shared folders - Environmental
            # modified
            "CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N/E:H/RL:U/RC:C"
            "/MS:C/MPR:H",
            CVSS31Severity(
                attack_complexity=Decimal("0.77"),
                attack_vector=Decimal("0.62"),
                availability_impact=Decimal("0.00"),
                availability_requirement=Decimal("0.0"),
                confidentiality_impact=Decimal("0.56"),
                confidentiality_requirement=Decimal("0.0"),
                exploitability=Decimal("1.0"),
                integrity_impact=Decimal("0.00"),
                integrity_requirement=Decimal("0.0"),
                modified_attack_complexity=Decimal("0.0"),
                modified_attack_vector=Decimal("0.0"),
                modified_availability_impact=Decimal("0.0"),
                modified_confidentiality_impact=Decimal("0.0"),
                modified_integrity_impact=Decimal("0.0"),
                modified_privileges_required=Decimal("0.5"),
                modified_user_interaction=Decimal("0.0"),
                modified_severity_scope=Decimal("1.0"),
                privileges_required=Decimal("0.62"),
                remediation_level=Decimal("1.00"),
                report_confidence=Decimal("1.00"),
                severity_scope=Decimal("0.0"),
                user_interaction=Decimal("0.85"),
            ),
        ],
    ],
)
def test_parse_cvss31_vector_string(
    vector_string: str, cvss31_severity: CVSS31Severity
) -> None:
    assert (
        cvss_utils.parse_cvss_vector_string(vector_string) == cvss31_severity
    )
    score = cvss_utils.get_severity_score_from_cvss_vector(vector_string)
    score_legacy = cvss_utils.get_severity_score_summary(cvss31_severity)
    assert score.base_score == score_legacy.base_score
    assert score.temporal_score == score_legacy.temporal_score
    assert score.cvss_v3 == CVSS3(vector_string).clean_vector()
    assert score.cvssf == score_legacy.cvssf


@pytest.mark.parametrize(
    ["cvss31_severity", "vector_string"],
    [
        [
            # Privilege escalation
            CVSS31Severity(
                attack_complexity=Decimal("0.44"),
                attack_vector=Decimal("0.85"),
                availability_impact=Decimal("0.56"),
                availability_requirement=Decimal("0.0"),
                confidentiality_impact=Decimal("0.56"),
                confidentiality_requirement=Decimal("0.0"),
                exploitability=Decimal("1.0"),
                integrity_impact=Decimal("0.56"),
                integrity_requirement=Decimal("0.0"),
                modified_attack_complexity=Decimal("0.0"),
                modified_attack_vector=Decimal("0.0"),
                modified_availability_impact=Decimal("0.0"),
                modified_confidentiality_impact=Decimal("0.0"),
                modified_integrity_impact=Decimal("0.0"),
                modified_privileges_required=Decimal("0.0"),
                modified_user_interaction=Decimal("0.0"),
                modified_severity_scope=Decimal("0.0"),
                privileges_required=Decimal("0.5"),
                remediation_level=Decimal("1.00"),
                report_confidence=Decimal("1.00"),
                severity_scope=Decimal("1.0"),
                user_interaction=Decimal("0.85"),
            ),
            "CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H/E:H/RL:U/RC:C",
        ],
        [
            # Privilege escalation - Environmental modified
            CVSS31Severity(
                attack_complexity=Decimal("0.44"),
                attack_vector=Decimal("0.85"),
                availability_impact=Decimal("0.56"),
                availability_requirement=Decimal("1.5"),
                confidentiality_impact=Decimal("0.56"),
                confidentiality_requirement=Decimal("0.5"),
                exploitability=Decimal("1.0"),
                integrity_impact=Decimal("0.56"),
                integrity_requirement=Decimal("1.0"),
                modified_attack_complexity=Decimal("0.0"),
                modified_attack_vector=Decimal("0.85"),
                modified_availability_impact=Decimal("0.0"),
                modified_confidentiality_impact=Decimal("0.0"),
                modified_integrity_impact=Decimal("0.0"),
                modified_privileges_required=Decimal("0.0"),
                modified_user_interaction=Decimal("0.0"),
                modified_severity_scope=Decimal("0.0"),
                privileges_required=Decimal("0.5"),
                remediation_level=Decimal("1.00"),
                report_confidence=Decimal("1.00"),
                severity_scope=Decimal("1.0"),
                user_interaction=Decimal("0.85"),
            ),
            "CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H/E:H/RL:U/RC:C"
            "/CR:L/IR:X/AR:H/MAV:N",
        ],
        [
            # Improper authentication for shared folders
            CVSS31Severity(
                attack_complexity=Decimal("0.77"),
                attack_vector=Decimal("0.62"),
                availability_impact=Decimal("0.00"),
                availability_requirement=Decimal("0.0"),
                confidentiality_impact=Decimal("0.56"),
                confidentiality_requirement=Decimal("0.0"),
                exploitability=Decimal("1.0"),
                integrity_impact=Decimal("0.00"),
                integrity_requirement=Decimal("0.0"),
                modified_attack_complexity=Decimal("0.0"),
                modified_attack_vector=Decimal("0.0"),
                modified_availability_impact=Decimal("0.0"),
                modified_confidentiality_impact=Decimal("0.0"),
                modified_integrity_impact=Decimal("0.0"),
                modified_privileges_required=Decimal("0.0"),
                modified_user_interaction=Decimal("0.0"),
                modified_severity_scope=Decimal("0.0"),
                privileges_required=Decimal("0.62"),
                remediation_level=Decimal("1.00"),
                report_confidence=Decimal("1.00"),
                severity_scope=Decimal("0.0"),
                user_interaction=Decimal("0.85"),
            ),
            "CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N/E:H/RL:U/RC:C",
        ],
        [
            # Improper authentication for shared folders - Environmental
            # modified
            CVSS31Severity(
                attack_complexity=Decimal("0.77"),
                attack_vector=Decimal("0.62"),
                availability_impact=Decimal("0.00"),
                availability_requirement=Decimal("0.0"),
                confidentiality_impact=Decimal("0.56"),
                confidentiality_requirement=Decimal("0.0"),
                exploitability=Decimal("1.0"),
                integrity_impact=Decimal("0.00"),
                integrity_requirement=Decimal("0.0"),
                modified_attack_complexity=Decimal("0.0"),
                modified_attack_vector=Decimal("0.0"),
                modified_availability_impact=Decimal("0.0"),
                modified_confidentiality_impact=Decimal("0.0"),
                modified_integrity_impact=Decimal("0.0"),
                modified_privileges_required=Decimal("0.5"),
                modified_user_interaction=Decimal("0.0"),
                modified_severity_scope=Decimal("1.0"),
                privileges_required=Decimal("0.62"),
                remediation_level=Decimal("1.00"),
                report_confidence=Decimal("1.00"),
                severity_scope=Decimal("0.0"),
                user_interaction=Decimal("0.85"),
            ),
            "CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N/E:H/RL:U/RC:C"
            "/MS:C/MPR:H",
        ],
        [
            # Improper authentication for shared folders - Temporal and
            # Environmental modified, privileges_required altered
            CVSS31Severity(
                attack_complexity=Decimal("0.77"),
                attack_vector=Decimal("0.62"),
                availability_impact=Decimal("0.00"),
                availability_requirement=Decimal("0.0"),
                confidentiality_impact=Decimal("0.56"),
                confidentiality_requirement=Decimal("0.0"),
                exploitability=Decimal("0.91"),
                integrity_impact=Decimal("0.00"),
                integrity_requirement=Decimal("0.0"),
                modified_attack_complexity=Decimal("0.0"),
                modified_attack_vector=Decimal("0.0"),
                modified_availability_impact=Decimal("0.0"),
                modified_confidentiality_impact=Decimal("0.0"),
                modified_integrity_impact=Decimal("0.0"),
                modified_privileges_required=Decimal("0.27"),
                modified_user_interaction=Decimal("0.0"),
                modified_severity_scope=Decimal("1.0"),
                privileges_required=Decimal("0.68"),
                remediation_level=Decimal("0.97"),
                report_confidence=Decimal("0.96"),
                severity_scope=Decimal("0.0"),
                user_interaction=Decimal("0.85"),
            ),
            "CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N/E:U/RL:W/RC:R"
            "/MS:C/MPR:H",
        ],
    ],
)
def test_parse_cvss31_severity_legacy(
    cvss31_severity: CVSS31Severity, vector_string: str
) -> None:
    vector_string_output = cvss_utils.parse_cvss31_severity_legacy(
        cvss31_severity
    )
    assert vector_string_output == CVSS3(vector_string).clean_vector()


@pytest.mark.parametrize(
    ["vector_string"],
    [
        ["CVSS:3.1/AV:N"],
        ["CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N/E:H/RL:U/RC:C/AV:P"],
        ["CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H/E:X/RL:X/RC:T"],
        ["CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H/E:X/RL:X/RC:X/"],
        [
            "AV:L/AC:L/Au:M/C:N/I:P/A:C/E:U/RL:W/RC:ND/CDP:L/TD:H/CR:ND/"
            "IR:ND/AR:M"  # CVSS 2.0
        ],
    ],
)
def test_parse_cvss31_vector_string_fail(vector_string: str) -> None:
    with pytest.raises(InvalidCVSS3VectorString):
        cvss_utils.parse_cvss_vector_string(vector_string)


@pytest.mark.parametrize(
    ["cwe_ids", "expected_result"],
    [
        [None, None],
        [[], None],
        [
            ["CWE-1035", "CWE-770", "CWE-937"],
            ["CWE-1035", "CWE-770", "CWE-937"],
        ],
        [
            ["CWE-1035", "CWE-937", "CWE-770", "CWE-770", "CWE-770"],
            ["CWE-1035", "CWE-770", "CWE-937"],
        ],
    ],
)
def test_parse_cwe_ids(
    cwe_ids: list[str] | None, expected_result: list[str] | None
) -> None:
    assert cvss_utils.parse_cwe_ids(cwe_ids) == expected_result


@pytest.mark.parametrize(
    ["cwe_ids"],
    [
        [["CWE-1035", "CWE-770", "CWE-93700"]],
        [["CWE-1035", "CWE-770", "CWE-937x"]],
        [["CWE-1035", "CWE-770", "cwe-937"]],
    ],
)
def test_parse_cwe_ids_fail(cwe_ids: list[str] | None) -> None:
    with pytest.raises(InvalidSeverityCweIds):
        cvss_utils.parse_cwe_ids(cwe_ids)


@pytest.mark.parametrize(
    ["criteria_vulnerability", "vector_string"],
    [
        [
            {  # F001 - SQL injection - C Sharp SQL API
                "score": {
                    "base": {
                        "attack_vector": "N",
                        "attack_complexity": "L",
                        "privileges_required": "L",
                        "user_interaction": "N",
                        "scope": "U",
                        "confidentiality": "N",
                        "integrity": "L",
                        "availability": "N",
                    },
                    "temporal": {
                        "exploit_code_maturity": "U",
                        "remediation_level": "O",
                        "report_confidence": "R",
                    },
                },
            },
            "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:R",
        ],
        [
            {  # F005 - Privilege escalation
                "score": {
                    "base": {
                        "attack_vector": "N",
                        "attack_complexity": "H",
                        "privileges_required": "H",
                        "user_interaction": "N",
                        "scope": "C",
                        "confidentiality": "H",
                        "integrity": "H",
                        "availability": "H",
                    },
                    "temporal": {
                        "exploit_code_maturity": "X",
                        "remediation_level": "X",
                        "report_confidence": "X",
                    },
                },
            },
            "CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H",
        ],
        [
            {  # F011 - Use of software with known vulnerabilities
                "score": {
                    "base": {
                        "attack_vector": "N",
                        "attack_complexity": "H",
                        "privileges_required": "L",
                        "user_interaction": "N",
                        "scope": "U",
                        "confidentiality": "L",
                        "integrity": "L",
                        "availability": "L",
                    },
                    "temporal": {
                        "exploit_code_maturity": "P",
                        "remediation_level": "O",
                        "report_confidence": "C",
                    },
                },
            },
            "CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:L/E:P/RL:O/RC:C",
        ],
    ],
)
def test_get_criteria_cvss_vector(
    criteria_vulnerability: Item, vector_string: str
) -> None:
    assert (
        cvss_utils.get_criteria_cvss_vector(criteria_vulnerability)
        == vector_string
    )
