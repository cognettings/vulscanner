from custom_exceptions import (
    DuplicateDraftFound,
    ErrorFileNameAlreadyExists,
    IncompleteSeverity,
    InvalidChar,
    InvalidCommitHash,
    InvalidField,
    InvalidFieldChange,
    InvalidMarkdown,
    InvalidMinTimeToRemediate,
    InvalidReportFilter,
    InvalidSeverityUpdateValues,
    NumberOutOfRange,
    UnsanitizedInputFound,
)
from custom_utils import (
    validations,
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
    FindingEvidence,
    FindingEvidences,
    FindingState,
)
from db_model.groups.types import (
    GroupFile,
)
from db_model.types import (
    SeverityScore,
)
from decimal import (
    Decimal,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


def test_validate_alphanumeric_field() -> None:
    assert validations.validate_alphanumeric_field("one test")
    with pytest.raises(InvalidField):
        validations.validate_alphanumeric_field("=test2@")


def test_validate_email_address() -> None:
    assert validations.validate_email_address("test@unittesting.com")
    with pytest.raises(InvalidField):
        assert validations.validate_email_address("testunittesting.com")
    with pytest.raises(InvalidField):
        assert validations.validate_email_address("test+1@unittesting.com")


@pytest.mark.parametrize(
    "fields",
    [
        ["valid", " =invalid"],
        ["=testfield", "testfield2"],
        ["testfield", "testfiel`d"],
        ["testfield", "<testfield2"],
    ],
)
def test_validate_fields(fields: list) -> None:
    validations.validate_fields(["valid%", " valid="])
    validations.validate_fields(["testfield", "testfield2"])
    with pytest.raises(InvalidChar):
        validations.validate_fields(fields)


def test_validate_file_exists() -> None:
    file_name = "test1.txt"
    validations.validate_file_exists(
        file_name,
        None,
    )
    group_files = [
        GroupFile(
            description="abc",
            file_name="test2.txt",
            modified_by="user@gmail.com",
        ),
        GroupFile(
            description="xyz",
            file_name="test3.txt",
            modified_by="user@gmail.com",
        ),
    ]
    validations.validate_file_exists(
        file_name=file_name,
        group_files=group_files,
    )
    with pytest.raises(ErrorFileNameAlreadyExists):
        validations.validate_file_exists(
            "test2.txt",
            group_files,
        )
    with pytest.raises(ErrorFileNameAlreadyExists):
        validations.validate_file_exists(
            "test3.txt",
            group_files,
        )


def test_validate_file_name() -> None:
    validations.validate_file_name("test123.py")
    with pytest.raises(InvalidChar):
        validations.validate_file_name("test.test.py")
    with pytest.raises(InvalidChar):
        validations.validate_file_name(
            "test|=$invalidname!.py",
        )


def test_validate_group_name() -> None:
    validations.validate_group_name("test")
    with pytest.raises(InvalidField):
        validations.validate_group_name("=test2@")


@pytest.mark.parametrize(
    "value, lower_bound, upper_bound, inclusive",
    [
        (10, 11, 12, True),
        (10, 11, 12, False),
    ],
)
def test_validate_int_range(
    value: int, lower_bound: int, upper_bound: int, inclusive: bool
) -> None:
    with pytest.raises(NumberOutOfRange):
        validations.validate_int_range(
            value, lower_bound, upper_bound, inclusive
        )


@pytest.mark.parametrize(
    "field",
    [
        ('"=invalidField"'),
        ("'+invalidField"),
        (",-invalidField"),
        (";@invalidField"),
        ("=invalidField"),
        ("+invalidField"),
        ("-invalidField"),
        ("@invalidField"),
        ("\\ninvalidField"),
    ],
)
def test_validate_sanitized_csv_input(field: str) -> None:
    validations.validate_sanitized_csv_input(
        "validfield@",
        "valid+field",
        "valid field",
        "http://localhost/bWAPP/sqli_1.php",
    )
    with pytest.raises(UnsanitizedInputFound):
        validations.validate_sanitized_csv_input(field)


def test_sequence_decreasing() -> None:
    assert validations.sequence_decreasing(
        "a", ord("a"), [ord("c"), ord("b")], False
    ) == [ord("c"), ord("b"), ord("a")]
    assert validations.sequence_decreasing(
        "c", ord("c"), [ord("a"), ord("b")], True
    ) == [ord("c")]
    assert validations.sequence_decreasing(
        "$", ord("$"), [ord("c"), ord("b")], False
    ) == [ord("$")]


def test_sequence_increasing() -> None:
    assert validations.sequence_increasing(
        "c", ord("c"), [ord("a"), ord("b")], True
    ) == [ord("a"), ord("b"), ord("c")]
    assert validations.sequence_increasing(
        "a", ord("a"), [ord("c"), ord("b")], False
    ) == [ord("a")]
    assert validations.sequence_increasing(
        "$", ord("$"), [ord("a"), ord("b")], True
    ) == [ord("$")]


@pytest.mark.parametrize(
    ["value", "length", "should_fail"],
    [
        ("a123b", 3, True),
        ("a123b", 4, False),
        ("a876b", 3, True),
        ("a876b", 4, False),
        ("aabcc", 3, True),
        ("aabcc", 4, False),
        ("ayxwc", 3, True),
        ("ayxwc", 4, False),
        ("aDEFc", 3, True),
        ("aDEFc", 4, False),
        ("aQPOc", 3, True),
        ("aQPOc", 4, False),
        ("a1221b", 3, False),
        ("a123321b", 4, False),
        ("a3455431b", 4, False),
        ("a1357b", 4, False),
        ("a9753b", 4, False),
        ("acdefghijklabcc", 7, True),
    ],
)
def test_has_sequence(value: str, length: int, should_fail: bool) -> None:
    assert validations.has_sequence(value, length) == should_fail


def test_validate_sequence() -> None:
    validations.validate_sequence(value="a1221b")
    validations.validate_sequence(value="no")
    with pytest.raises(InvalidReportFilter):
        validations.validate_sequence(value="aabcc")
    with pytest.raises(InvalidReportFilter):
        validations.validate_sequence(value="6543221")


@pytest.mark.parametrize(
    ["value", "should_fail"],
    [
        ("a123b", True),
        ("a'123b", False),
        ("a~876b", False),
        ("a87:6b", False),
        ("aa;bcc", False),
        ("aa<bcc", False),
        ("ayx%wc", False),
        ("ay>xwc", False),
        ("aDEFc", True),
        ("aDE=Fc", False),
        ("aQP@Oc", False),
        ("aQP-Oc", False),
        ("a12]21b", False),
        ("a123+321b", False),
        ("a34^55431b", False),
        ('a1"357b', False),
        ("a97?53b", False),
    ],
)
def test_validate_symbols(value: str, should_fail: bool) -> None:
    if should_fail:
        with pytest.raises(InvalidReportFilter):
            validations.validate_symbols(value)
    else:
        validations.validate_symbols(value)


def test_validate_finding_id() -> None:
    validations.validate_finding_id(
        finding_id="3c475384-834c-47b0-ac71-a41a022e401c"
    )

    validations.validate_finding_id(finding_id="123456781234567812345678")

    with pytest.raises(InvalidField):
        validations.validate_finding_id(
            finding_id="12345678-1234-1234-1234-1234567890a"
        )
    with pytest.raises(InvalidField):
        validations.validate_finding_id(finding_id="invalid_finding_id")


def test_validate_group_language() -> None:
    validations.validate_group_language(language="es")
    validations.validate_group_language(language="EN")
    with pytest.raises(InvalidField):
        validations.validate_group_language(language="fr")
    with pytest.raises(InvalidField):
        validations.validate_group_language(language="")


def test_validate_title_change() -> None:
    # Test valid input
    assert validations.validate_finding_title_change_policy(
        old_title="old_title",
        new_title="new_title",
        status=FindingStatus.DRAFT,
    )

    # Test invalid input
    with pytest.raises(InvalidFieldChange):
        validations.validate_finding_title_change_policy(
            old_title="old_title",
            new_title="new_title",
            status=FindingStatus.VULNERABLE,
        )
        validations.validate_finding_title_change_policy(
            old_title="old_title",
            new_title="new_title",
            status=FindingStatus.SAFE,
        )


def test_validate_commit_hash() -> None:
    validations.validate_commit_hash(
        "da39a3ee5e6b4b0d3255bfef95601890afd80709"
    )
    validations.validate_commit_hash(
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    with pytest.raises(InvalidCommitHash):
        validations.validate_commit_hash("invalid Hash")


def test_validate_start_letter() -> None:
    validations.validate_start_letter("abc123")
    with pytest.raises(InvalidReportFilter):
        validations.validate_start_letter("123abc")


def test_validate_include_number() -> None:
    validations.validate_include_number("abc123")
    with pytest.raises(InvalidReportFilter):
        validations.validate_include_number("abcdef")


def test_validate_include_lowercase() -> None:
    validations.validate_include_lowercase("abc123")
    with pytest.raises(InvalidReportFilter):
        validations.validate_include_lowercase("ABC123")


def test_validate_include_uppercase() -> None:
    validations.validate_include_uppercase("aBc123")
    with pytest.raises(InvalidReportFilter):
        validations.validate_include_uppercase("abc123")


def test_validate_markdown() -> None:
    assert validations.validate_markdown(text="<h1>Heading level\t 1</h1>")
    assert validations.validate_markdown(
        text="ftp://user:password@ftp.example.com:21/path/to/file"
    )
    with pytest.raises(InvalidMarkdown):
        validations.validate_markdown(text="<span>Example Text</span>")


def test_validate_no_duplicate_drafts() -> None:
    test_finding = (
        Finding(
            id="3c475384-834c-47b0-ac71-a41a022e401c",
            group_name="group1",
            state=FindingState(
                modified_by="test1@gmail.com",
                modified_date=datetime.fromisoformat(
                    "2017-04-08T00:45:11+00:00"
                ),
                source=Source.ASM,
                status=FindingStateStatus.CREATED,
            ),
            title="001. SQL injection - C Sharp SQL API",
            recommendation="Updated recommendation",
            description="I just have updated the description",
            hacker_email="test1@gmail.com",
            severity=CVSS31Severity(
                attack_complexity=Decimal("0.44"),
                attack_vector=Decimal("0.2"),
                availability_impact=Decimal("0.22"),
                availability_requirement=Decimal("1.5"),
                confidentiality_impact=Decimal("0.22"),
                confidentiality_requirement=Decimal("0.5"),
                exploitability=Decimal("0.94"),
                integrity_impact=Decimal("0.22"),
                integrity_requirement=Decimal("1"),
                modified_availability_impact=Decimal("0.22"),
                modified_user_interaction=Decimal("0.62"),
                modified_integrity_impact=Decimal("0"),
                modified_attack_complexity=Decimal("0.44"),
                modified_severity_scope=Decimal("0"),
                modified_privileges_required=Decimal("0.27"),
                modified_attack_vector=Decimal("0.85"),
                modified_confidentiality_impact=Decimal("0.22"),
                privileges_required=Decimal("0.62"),
                severity_scope=Decimal("1.0"),
                remediation_level=Decimal("0.95"),
                report_confidence=Decimal("1"),
                user_interaction=Decimal("0.85"),
            ),
            severity_score=SeverityScore(
                base_score=Decimal("4.5"),
                temporal_score=Decimal("4.1"),
                cvss_v3="CVSS:3.1/AV:P/AC:H/PR:L/UI:N/S:C/C:L/I:L/A:L/E:P/"
                "RL:O/CR:L/AR:H/MAV:N/MAC:H/MPR:H/MUI:R/MS:U/MC:L/MA:L",
                cvssf=Decimal("1.149"),
            ),
            requirements=(
                "REQ.0132. Passwords (phrase type) "
                "must be at least 3 words long."
            ),
            threat="Updated threat",
            attack_vector_description=("This is an updated attack vector"),
            evidences=FindingEvidences(
                evidence1=FindingEvidence(
                    description="evidence1",
                    url="group1-3c475384-834c-47b0-ac71-a41a022e401c-"
                    "evidence1",
                    modified_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                ),
                records=FindingEvidence(
                    description="records",
                    url="group1-3c475384-834c-47b0-ac71-a41a022e401c-"
                    "records",
                    modified_date=datetime.fromisoformat(
                        "2111-11-19T13:37:10+00:00"
                    ),
                ),
            ),
        ),
    )

    assert validations.validate_no_duplicate_drafts(
        new_title="New Title", drafts=(), findings=test_finding
    )
    assert validations.validate_no_duplicate_drafts(
        new_title="New Title", drafts=test_finding, findings=()
    )

    with pytest.raises(DuplicateDraftFound):
        validations.validate_no_duplicate_drafts(
            new_title="001. SQL injection - C Sharp SQL API",
            drafts=(),
            findings=test_finding,
        )
    with pytest.raises(DuplicateDraftFound):
        validations.validate_no_duplicate_drafts(
            new_title="001. SQL injection - C Sharp SQL API",
            drafts=test_finding,
            findings=(),
        )


def test_validate_missing_severity_field_names() -> None:
    fields_cvss31_severity = {
        "attack_complexity",
        "attack_vector",
        "availability_impact",
        "availability_requirement",
        "confidentiality_impact",
        "confidentiality_requirement",
        "exploitability",
        "integrity_impact",
        "integrity_requirement",
        "modified_attack_complexity",
        "modified_attack_vector",
        "modified_availability_impact",
        "modified_confidentiality_impact",
        "modified_integrity_impact",
        "modified_privileges_required",
        "modified_user_interaction",
        "modified_severity_scope",
        "privileges_required",
        "remediation_level",
        "report_confidence",
        "severity_scope",
        "user_interaction",
    }

    validations.validate_missing_severity_field_names(
        field_names=fields_cvss31_severity
    )

    fields_cvss31_severity.remove("attack_complexity")
    with pytest.raises(IncompleteSeverity):
        validations.validate_missing_severity_field_names(
            field_names=fields_cvss31_severity
        )


def test_validate_update_severity_values() -> None:
    my_dict = {"field1": 2, "field2": 6, "field3": 9}
    my_dict_fail = {"field1": 2, "field2": 12, "field3": 9}

    validations.validate_update_severity_values(dictionary=my_dict)

    with pytest.raises(InvalidSeverityUpdateValues):
        validations.validate_update_severity_values(dictionary=my_dict_fail)


def test_validate_chart_field() -> None:
    validations.validate_chart_field("content", "field")
    with pytest.raises(InvalidChar):
        validations.validate_chart_field("content!", "field")


def test_check_and_set_min_time_to_remediate() -> None:
    assert validations.check_and_set_min_time_to_remediate(None) is None
    assert validations.check_and_set_min_time_to_remediate(1) == 1
    assert validations.check_and_set_min_time_to_remediate("10") == 10
    with pytest.raises(InvalidMinTimeToRemediate):
        validations.check_and_set_min_time_to_remediate(0)
    with pytest.raises(InvalidMinTimeToRemediate):
        validations.check_and_set_min_time_to_remediate(-5)
    with pytest.raises(InvalidMinTimeToRemediate):
        validations.check_and_set_min_time_to_remediate("-5")
    with pytest.raises(InvalidMinTimeToRemediate):
        validations.check_and_set_min_time_to_remediate("abc")
