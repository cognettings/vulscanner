from custom_exceptions import (
    DuplicateDraftFound,
    ErrorFileNameAlreadyExists,
    IncompleteSeverity,
    InvalidChar,
    InvalidCommitHash,
    InvalidField,
    InvalidFieldLength,
    InvalidMarkdown,
    InvalidParameter,
    InvalidReportFilter,
    InvalidSeverity,
    InvalidSeverityUpdateValues,
    InvalidSpacesField,
    NumberOutOfRange,
    UnsanitizedInputFound,
)
from custom_utils import (
    validations_deco,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    FindingStateStatus,
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
from typing import (
    Any,
    NamedTuple,
)

pytestmark = [
    pytest.mark.asyncio,
]


def test_validate_alphanumeric_field_deco() -> None:
    @validations_deco.validate_alphanumeric_field_deco("field")
    def decorated_func(field: str) -> str:
        return field

    assert decorated_func(field="one test")
    with pytest.raises(InvalidField):
        decorated_func(field="=test2@")

    class TestClass(NamedTuple):
        field: str

    @validations_deco.validate_alphanumeric_field_deco("test_obj.field")
    def decorated_func_obj(test_obj: TestClass) -> TestClass:
        return test_obj

    test_obj = TestClass(field="one test")
    test_obj_fail = TestClass(field="=test2@")
    assert decorated_func_obj(test_obj=test_obj)

    with pytest.raises(InvalidField):
        decorated_func_obj(test_obj=test_obj_fail)


def test_validate_email_address_deco() -> None:
    @validations_deco.validate_email_address_deco("email")
    def decorated_func(email: str) -> str:
        return email

    assert decorated_func(email="test@unittesting.com")

    class Email(NamedTuple):
        address: str

    @validations_deco.validate_email_address_deco("email_test.address")
    def decorated_func_obj(email_test: Email) -> Email:
        return email_test

    email = Email(address="test@unittesting.com")
    assert decorated_func_obj(email_test=email)
    with pytest.raises(InvalidField):
        decorated_func(email="testunittesting.com")
    with pytest.raises(InvalidField):
        decorated_func(email="test+1@unittesting.com")


def test_validate_length_deco() -> None:
    @validations_deco.validate_length_deco(
        "test_string", min_length=2, max_length=12
    )
    def test_2_and_12(test_string: str) -> str:
        return test_string

    assert test_2_and_12(test_string="testlength")
    with pytest.raises(InvalidFieldLength):
        test_2_and_12(test_string="t")
    with pytest.raises(InvalidFieldLength):
        test_2_and_12(test_string="testlengthtoolong")
    with pytest.raises(InvalidFieldLength):
        test_2_and_12(test_string="")

    @validations_deco.validate_length_deco("test_string", max_length=10)
    def test_max_12(test_string: str) -> str:
        return test_string

    assert test_max_12(test_string="t")
    assert test_max_12(test_string="") == ""
    assert test_max_12(test_string="testlength")
    with pytest.raises(InvalidFieldLength):
        test_max_12(test_string="testlengthtoolong")

    @validations_deco.validate_length_deco("test_string", min_length=3)
    def test_min_3(test_string: str) -> str:
        return test_string

    assert test_min_3(test_string="ttt")
    assert test_min_3(test_string="testlengthtootootoolong")
    with pytest.raises(InvalidFieldLength):
        test_min_3(test_string="a")
    with pytest.raises(InvalidFieldLength):
        test_min_3(test_string="")

    class TestClass(NamedTuple):
        test_string: str | None = None
        a_none_field: str | None = None

    @validations_deco.validate_length_deco(
        "test_obj.test_string", max_length=12
    )
    @validations_deco.validate_length_deco(
        "test_obj.a_none_field", min_length=12
    )
    def get_obj(test_obj: TestClass) -> TestClass:
        return test_obj

    test_obj = TestClass(test_string="test_string")
    test_obj_fail = TestClass(test_string="test_string_too_long")
    assert get_obj(test_obj=test_obj)
    with pytest.raises(InvalidFieldLength):
        get_obj(test_obj=test_obj_fail)


def test_validate_all_fields_length_deco() -> None:
    @validations_deco.validate_all_fields_length_deco(max_length=5)
    def decorated_func(**kwargs: Any) -> str:
        return f"{kwargs}"

    assert decorated_func(field1="abcd", field2="abc")
    with pytest.raises(InvalidFieldLength):
        decorated_func(field1="abcdefg", field2="abcdefg")


def test_validate_fields_deco() -> None:
    class TestClass(NamedTuple):
        field1: str
        field2: str

    test_object = TestClass(field1="valid", field2=" valid=")

    @validations_deco.validate_fields_deco(["obj"])
    def decorated_func_full_obj(obj: TestClass) -> TestClass:
        return obj

    assert decorated_func_full_obj(obj=test_object)

    test_list = ["test", "valid", "valid%"]

    @validations_deco.validate_fields_deco(["test_list"])
    def decorated_func_full_list(test_list: list) -> list:
        return test_list

    assert decorated_func_full_list(test_list=test_list)

    @validations_deco.validate_fields_deco(
        ["test_object.field1", "test_object.field2"]
    )
    def decorated_func_obj(test_object: TestClass) -> TestClass:
        return test_object

    assert decorated_func_obj(test_object=test_object)

    @validations_deco.validate_fields_deco(["field1", "field2"])
    def decorated_func(field1: str, field2: str) -> str:
        return field1 + field2

    assert decorated_func(field1="valid%", field2=" valid=")
    assert decorated_func(field1="testfield", field2="testfield2")
    with pytest.raises(InvalidChar):
        decorated_func(field1="valid", field2=" =invalid")
    with pytest.raises(InvalidChar):
        decorated_func(field1="=testfield", field2="testfield2")
    with pytest.raises(InvalidChar):
        decorated_func(field1="testfield", field2="testfiel`d")
    with pytest.raises(InvalidChar):
        decorated_func(field1="testfield", field2="<testfield2")


def test_validate_file_exists_deco() -> None:
    file_name = "test1.txt"

    @validations_deco.validate_file_exists_deco("file_name", "not_field")
    def decorated_func(file_name: str) -> str:
        return file_name

    assert decorated_func(file_name=file_name)

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

    @validations_deco.validate_file_exists_deco("file_name", "group_files")
    def decorated_func_group(
        file_name: str, group_files: list[GroupFile] | None
    ) -> tuple:
        return (file_name, group_files)

    assert decorated_func_group(
        file_name=file_name,
        group_files=group_files,
    )
    with pytest.raises(ErrorFileNameAlreadyExists):
        decorated_func_group(file_name="test2.txt", group_files=group_files)
    with pytest.raises(ErrorFileNameAlreadyExists):
        decorated_func_group(file_name="test3.txt", group_files=group_files)

    class TestClass(NamedTuple):
        file_name: str

    test_obj = TestClass(file_name="test1.txt")
    test_obj_fail = TestClass(file_name="test2.txt")

    @validations_deco.validate_file_exists_deco(
        "test_obj.file_name", "group_files"
    )
    def decorated_func_obj(
        test_obj: TestClass,
        group_files: list[GroupFile] | None,
    ) -> tuple[TestClass, list[GroupFile] | None]:
        return (test_obj, group_files)

    assert decorated_func_obj(test_obj=test_obj, group_files=group_files)
    with pytest.raises(ErrorFileNameAlreadyExists):
        decorated_func_obj(test_obj=test_obj_fail, group_files=group_files)


def test_validate_file_name_deco() -> None:
    @validations_deco.validate_file_name_deco("file_name")
    def decorated_func(file_name: str) -> str:
        return file_name

    assert decorated_func(file_name="test123.py")
    with pytest.raises(InvalidChar):
        decorated_func(file_name="test|=$invalidname!.py")
    with pytest.raises(InvalidChar):
        decorated_func(file_name="test.test.py")

    class TestClass(NamedTuple):
        file_name: str

    @validations_deco.validate_file_name_deco("test_object.file_name")
    def decorated_func_obj(test_object: TestClass) -> TestClass:
        return test_object

    test_object = TestClass(file_name="valid")
    test_object_fail = TestClass(file_name="test.test.py")
    assert decorated_func_obj(test_object=test_object)
    with pytest.raises(InvalidChar):
        decorated_func_obj(test_object=test_object_fail)


def test_validate_group_name_deco() -> None:
    @validations_deco.validate_group_name_deco("group")
    def decorated_func(group: str) -> str:
        return group

    assert decorated_func(group="test")
    with pytest.raises(InvalidField):
        decorated_func(group="=test2@")

    class TestClass(NamedTuple):
        group: str

    test_obj = TestClass(group="test")
    test_obj_fail = TestClass(group="=test2@")

    @validations_deco.validate_group_name_deco("test_obj.group")
    def decorated_func_obj(test_obj: TestClass) -> TestClass:
        return test_obj

    assert decorated_func_obj(test_obj=test_obj)
    with pytest.raises(InvalidField):
        decorated_func_obj(test_obj=test_obj_fail)


def test_validate_int_range_deco() -> None:
    @validations_deco.validate_int_range_deco(
        "int_value", lower_bound=11, upper_bound=12, inclusive=True
    )
    def decorated_func_inclusive(int_value: int) -> int:
        return int_value

    assert decorated_func_inclusive(int_value=12)
    with pytest.raises(NumberOutOfRange):
        decorated_func_inclusive(int_value=13)

    @validations_deco.validate_int_range_deco(
        "int_value", lower_bound=10, upper_bound=12, inclusive=False
    )
    def decorated_func_not_inclusive(int_value: int) -> int:
        return int_value

    assert decorated_func_not_inclusive(int_value=11)
    with pytest.raises(NumberOutOfRange):
        decorated_func_not_inclusive(int_value=12)

    class TestClass(NamedTuple):
        int_value: int

    test_obj = TestClass(int_value=12)
    test_obj_fail = TestClass(int_value=13)

    @validations_deco.validate_int_range_deco(
        "test_obj.int_value", lower_bound=11, upper_bound=12, inclusive=True
    )
    def decorated_func_obj(test_obj: TestClass) -> TestClass:
        return test_obj

    assert decorated_func_obj(test_obj=test_obj)
    with pytest.raises(NumberOutOfRange):
        decorated_func_obj(test_obj=test_obj_fail)


@pytest.mark.parametrize(
    "field1, field2, field3",
    [
        {
            '"=invalidField"',
            "'not_check",
            "'+invalidField",
        },
        {
            ",-invalidField",
            "not_check",
            ";@invalidField",
        },
        {
            "-invalidField",
            "not_check",
            "@invalidField",
        },
        {
            "\\ninvalidField",
            "not_check",
            '"=invalidField"',
        },
    ],
)
def test_validate_sanitized_csv_input_deco(
    field1: str, field2: str, field3: str
) -> None:
    @validations_deco.validate_sanitized_csv_input_deco(
        field_names=["field1", "field3"]
    )
    def decorated_func(field1: str, field2: str, field3: str) -> str:
        return field1 + field2 + field3

    assert decorated_func(
        field1="validfield@",
        field2="not_check",
        field3="valid field",
    )
    with pytest.raises(UnsanitizedInputFound):
        decorated_func(
            field1=field1,
            field2=field2,
            field3=field3,
        )

    class TestClass(NamedTuple):
        field1: str
        field2: str
        field3: str

    test_obj = TestClass(
        field1="validfield@",
        field2="not_check",
        field3="valid field",
    )
    test_obj_fail = TestClass(
        field1="\\ninvalidField",
        field2="not_check",
        field3='"=invalidField"',
    )

    @validations_deco.validate_sanitized_csv_input_deco(
        field_names=["test_obj.field1", "test_obj.field3", "field"]
    )
    def decorated_func_obj(test_obj: TestClass) -> TestClass:
        return test_obj

    assert decorated_func_obj(test_obj=test_obj)
    with pytest.raises(UnsanitizedInputFound):
        decorated_func_obj(test_obj=test_obj_fail)


def test_validate_sequence_deco() -> None:
    @validations_deco.validate_sequence_deco("value")
    def decorated_func(value: str) -> str:
        return value

    assert decorated_func(value="a1221b")
    with pytest.raises(InvalidReportFilter):
        decorated_func(value="aabcc")

    class TestClass(NamedTuple):
        value: object

    @validations_deco.validate_sequence_deco("test_obj.value")
    def decorated_func_obj(test_obj: TestClass) -> TestClass:
        return test_obj

    test_obj = TestClass(value="a1221b")
    test_obj_fail = TestClass(value=54321)

    assert decorated_func_obj(test_obj=test_obj)
    with pytest.raises(InvalidReportFilter):
        decorated_func_obj(test_obj=test_obj_fail)


@pytest.mark.parametrize(
    "value,should_fail",
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
def test_validate_symbols_deco(value: str, should_fail: bool) -> None:
    @validations_deco.validate_symbols_deco("value")
    def decorated_func(value: str) -> str:
        return value

    if should_fail:
        with pytest.raises(InvalidReportFilter):
            decorated_func(value=value)
    else:
        assert decorated_func(value=value)

    class TestClass(NamedTuple):
        value: str

    @validations_deco.validate_symbols_deco("test_obj.value")
    def decorated_func_obj(test_obj: TestClass) -> TestClass:
        return test_obj

    test_obj = TestClass(value="a'123b")
    test_obj_fail = TestClass(value="a123b")

    assert decorated_func_obj(test_obj=test_obj)
    with pytest.raises(InvalidReportFilter):
        decorated_func_obj(test_obj=test_obj_fail)


def test_validate_finding_id_deco() -> None:
    @validations_deco.validate_finding_id_deco("finding_id")
    def decorated_func(finding_id: str) -> str:
        return finding_id

    assert decorated_func(finding_id="3c475384-834c-47b0-ac71-a41a022e401c")
    assert decorated_func(finding_id="123456781234567812345678")

    with pytest.raises(InvalidField):
        decorated_func(finding_id="12345678-1234-1234-1234-1234567890a")
    with pytest.raises(InvalidField):
        decorated_func(finding_id="invalid_finding_id")

    class TestClass(NamedTuple):
        finding_id: str

    @validations_deco.validate_finding_id_deco("test_obj.finding_id")
    def decorated_func_obj(test_obj: TestClass) -> TestClass:
        return test_obj

    test_obj = TestClass(finding_id="8b3a4c2d-e5f6-4g1h-9i8j-7k6l5m4n3o2r")
    test_obj_fail = TestClass(finding_id="12345678-1234-1234-1234-1234567890a")

    assert decorated_func_obj(test_obj=test_obj)
    with pytest.raises(InvalidField):
        decorated_func_obj(test_obj=test_obj_fail)


@pytest.mark.parametrize(
    "language, should_fail",
    [
        ("en", False),
        ("ES", False),
        ("fr", True),
        ("", True),
        (123, True),
    ],
)
def test_validate_group_language_deco(
    language: str, should_fail: bool
) -> None:
    @validations_deco.validate_group_language_deco("value")
    def decorated_func(value: str) -> str:
        return value

    if should_fail:
        with pytest.raises(InvalidField):
            decorated_func(value=language)
    else:
        assert decorated_func(value=language)

    class TestClass(NamedTuple):
        language: str

    test_obj = TestClass(language="es")
    test_obj_fail = TestClass(language="fr")

    @validations_deco.validate_group_language_deco("test_obj.language")
    def decorated_func_obj(test_obj: TestClass) -> TestClass:
        return test_obj

    assert decorated_func_obj(test_obj=test_obj)
    with pytest.raises(InvalidField):
        decorated_func_obj(test_obj=test_obj_fail)


def test_validate_space_field_deco() -> None:
    @validations_deco.validate_space_field_deco("field")
    def decorated_func(field: str) -> str:
        return field

    # Test valid input
    assert decorated_func(field="test")

    # Test invalid input
    with pytest.raises(InvalidSpacesField):
        decorated_func(field="  ")

    class TestClass(NamedTuple):
        field: str

    test_obj = TestClass(field="test")
    test_obj_fail = TestClass(field="   ")

    @validations_deco.validate_space_field_deco("test_obj.field")
    def decorated_func_obj(test_obj: TestClass) -> TestClass:
        return test_obj

    assert decorated_func_obj(test_obj=test_obj)
    with pytest.raises(InvalidSpacesField):
        decorated_func_obj(test_obj=test_obj_fail)


def test_validate_commit_hash_deco() -> None:
    @validations_deco.validate_commit_hash_deco(
        "comm",
    )
    def decorated_func(comm: str) -> str:
        return comm

    decorated_func(comm="da39a3ee5e6b4b0d3255bfef95601890afd80709")
    decorated_func(
        comm="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )

    with pytest.raises(InvalidCommitHash):
        decorated_func(comm="invalid Hash")

    class TestClass(NamedTuple):
        comm: str

    test_obj = TestClass(comm="da39a3ee5e6b4b0d3255bfef95601890afd80709")
    test_obj_fail = TestClass(comm="invalid Hash")

    @validations_deco.validate_commit_hash_deco("test_obj.comm")
    def decorated_func_obj(test_obj: TestClass) -> TestClass:
        return test_obj

    assert decorated_func_obj(test_obj=test_obj)
    with pytest.raises(InvalidCommitHash):
        decorated_func_obj(test_obj=test_obj_fail)


def test_validate_start_letter_deco() -> None:
    @validations_deco.validate_start_letter_deco(
        "field",
    )
    def decorated_func(field: str) -> str:
        return field

    decorated_func(field="abc123")

    with pytest.raises(InvalidReportFilter):
        decorated_func(field="123abc")

    class TestClass(NamedTuple):
        field: str

    test_obj = TestClass(field="abc123")
    test_obj_fail = TestClass(field="123abc")

    @validations_deco.validate_start_letter_deco("test_obj.field")
    def decorated_func_obj(test_obj: TestClass) -> TestClass:
        return test_obj

    assert decorated_func_obj(test_obj=test_obj)
    with pytest.raises(InvalidReportFilter):
        decorated_func_obj(test_obj=test_obj_fail)


def test_validate_include_number_deco() -> None:
    @validations_deco.validate_include_number_deco(
        "field",
    )
    def decorated_func(field: str) -> str:
        return field

    decorated_func(field="abc123")

    with pytest.raises(InvalidReportFilter):
        decorated_func(field="abcdef")

    class TestClass(NamedTuple):
        field: str

    test_obj = TestClass(field="abc123")
    test_obj_fail = TestClass(field="abcdef")

    @validations_deco.validate_include_number_deco("test_obj.field")
    def decorated_func_obj(test_obj: TestClass) -> TestClass:
        return test_obj

    assert decorated_func_obj(test_obj=test_obj)
    with pytest.raises(InvalidReportFilter):
        decorated_func_obj(test_obj=test_obj_fail)


def test_validate_include_lowercase_deco() -> None:
    @validations_deco.validate_include_lowercase_deco("field")
    def decorated_func(field: str) -> str:
        return field

    assert decorated_func(field="abc123")

    with pytest.raises(InvalidReportFilter):
        decorated_func(field="ABC123")

    class TestClass(NamedTuple):
        field: str

    test_obj = TestClass(field="abc123")
    test_obj_fail = TestClass(field="ABC123")

    @validations_deco.validate_include_lowercase_deco("test_obj.field")
    def decorated_func_obj(test_obj: TestClass) -> TestClass:
        return test_obj

    assert decorated_func_obj(test_obj=test_obj)
    with pytest.raises(InvalidReportFilter):
        decorated_func_obj(test_obj=test_obj_fail)


def test_validate_include_uppercase_deco() -> None:
    @validations_deco.validate_include_uppercase_deco(
        "field",
    )
    def decorated_func(field: str) -> str:
        return field

    decorated_func(field="aBc123")

    with pytest.raises(InvalidReportFilter):
        decorated_func(field="abc123")

    class TestClass(NamedTuple):
        field: str

    test_obj = TestClass(field="aBc123")
    test_obj_fail = TestClass(field="abc123")

    @validations_deco.validate_include_uppercase_deco("test_obj.field")
    def decorated_func_obj(test_obj: TestClass) -> TestClass:
        return test_obj

    assert decorated_func_obj(test_obj=test_obj)
    with pytest.raises(InvalidReportFilter):
        decorated_func_obj(test_obj=test_obj_fail)


def test_validate_url_deco() -> None:
    @validations_deco.validate_url_deco("url")
    def decorated_func(url: str) -> str:
        return url

    assert decorated_func(
        url="https://www.example.com/path/to/page?query=1%20and%202"
    )
    assert decorated_func(
        url="ftp://user:password@ftp.example.com:21/path/to/file"
    )

    with pytest.raises(InvalidChar):
        decorated_func(
            url="https://www.example.com/path/to/page!query=1%20and%202"
        )


def test_validate_markdown_deco() -> None:
    @validations_deco.validate_markdown_deco("text")
    def decorated_func(text: str) -> str:
        return text

    assert decorated_func(text="<h1>Heading level\t 1</h1>")
    assert decorated_func(
        text="ftp://user:password@ftp.example.com:21/path/to/file"
    )

    with pytest.raises(InvalidMarkdown):
        decorated_func(text="<span>Example Text</span>")


def test_validate_no_duplicate_drafts_deco() -> None:
    @validations_deco.validate_no_duplicate_drafts_deco(
        "title_field", "drafts_field", "findings_field"
    )
    def decorated_func(
        title_field: str,
        drafts_field: tuple[Finding, ...],
        findings_field: tuple[Finding, ...],
    ) -> tuple:
        return (title_field, drafts_field, findings_field)

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

    assert decorated_func(
        title_field="New Title", drafts_field=(), findings_field=test_finding
    )
    assert decorated_func(
        title_field="New Title", drafts_field=test_finding, findings_field=()
    )

    with pytest.raises(DuplicateDraftFound):
        decorated_func(
            title_field="001. SQL injection - C Sharp SQL API",
            drafts_field=(),
            findings_field=test_finding,
        )
    with pytest.raises(DuplicateDraftFound):
        decorated_func(
            title_field="001. SQL injection - C Sharp SQL API",
            drafts_field=test_finding,
            findings_field=(),
        )


def test_validate_missing_severity_field_names_deco() -> None:
    @validations_deco.validate_missing_severity_field_names_deco("fields")
    def decorated_func(fields: set[str]) -> tuple:
        return (fields,)

    fields_31_severity = {
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

    assert decorated_func(fields=fields_31_severity)

    fields_31_severity.remove("attack_complexity")
    with pytest.raises(IncompleteSeverity):
        decorated_func(fields=fields_31_severity)


def test_validate_update_severity_values_deco() -> None:
    @validations_deco.validate_update_severity_values_deco("dictionary")
    def decorated_func(dictionary: dict) -> dict:
        return dictionary

    my_dict = {"field1": 2, "field2": 6, "field3": 9}
    my_dict_fail = {"field1": 2, "field2": 12, "field3": 9}

    assert decorated_func(dictionary=my_dict)

    with pytest.raises(InvalidSeverityUpdateValues):
        decorated_func(dictionary=my_dict_fail)


def test_validate_chart_field_deco() -> None:
    @validations_deco.validate_chart_field_deco("value", "name")
    def decorated_func(value: str, name: str) -> str:
        return value + name

    assert decorated_func(value="content", name="field")

    with pytest.raises(InvalidChar):
        decorated_func(value="content!", name="field")


def test_validate_severity_range_deco() -> None:
    @validations_deco.validate_severity_range_deco(
        "severity", min_value=Decimal(2), max_value=Decimal(6)
    )
    def decorated_func(severity: int) -> float:
        return severity

    assert decorated_func(severity=3)
    with pytest.raises(InvalidSeverity):
        decorated_func(severity=7)
    with pytest.raises(InvalidSeverity):
        decorated_func(severity=1)


def test_validate_field_exist_deco() -> None:
    @validations_deco.validate_field_exist_deco("missing")
    def decorated_func(missing: str | None) -> str | None:
        return missing or "test"

    assert decorated_func(missing="something")
    assert decorated_func(missing="")
    with pytest.raises(InvalidParameter):
        decorated_func(missing=None)


def test_validate_chart_field_dict_deco() -> None:
    @validations_deco.validate_chart_field_dict_deco(
        "my_dict", ("param1", "param3")
    )
    def decorated_func(my_dict: dict) -> dict:
        return my_dict

    my_dict = {"param1": "arg1", "param2": "agr2", "param3": "arg3"}
    my_dict_fail = {"param1": "arg1", "param2": "agr2", "param3": "a`r`g3"}
    assert decorated_func(my_dict=my_dict)

    with pytest.raises(
        InvalidChar, match="Exception - Invalid characters in param3"
    ):
        decorated_func(my_dict=my_dict_fail)
