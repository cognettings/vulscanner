import bleach
from collections.abc import (
    Iterable,
    Sized,
)
from custom_exceptions import (
    CustomBaseException,
    DuplicateDraftFound,
    ErrorFileNameAlreadyExists,
    IncompleteSeverity,
    InvalidChar,
    InvalidCommitHash,
    InvalidField,
    InvalidFieldChange,
    InvalidFieldLength,
    InvalidMarkdown,
    InvalidMinTimeToRemediate,
    InvalidReportFilter,
    InvalidSeverityUpdateValues,
    InvalidSpacesField,
    NumberOutOfRange,
    UnsanitizedInputFound,
)
from custom_utils import (
    utils,
)
from db_model.findings.enums import (
    FindingStatus,
)
from db_model.findings.types import (
    CVSS31Severity,
    Finding,
)
from db_model.groups.types import (
    GroupFile,
)
from decimal import (
    Decimal,
)
import itertools
import re
from typing import (
    cast,
    NamedTuple,
    TypeVar,
)

# Typing
T = TypeVar("T")


def check_exp(field: str, regexp: str, ex: CustomBaseException) -> None:
    if not re.match(regexp, field.replace("\n", " ").strip(), re.MULTILINE):
        raise ex


def check_email(email: str, ex: CustomBaseException) -> None:
    if "+" in email:
        raise ex
    check_exp(
        email,
        r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$",
        ex,
    )


def validate_email_address(email: str) -> bool:
    if "+" in email:
        raise InvalidField("email address")
    try:
        check_field(
            email,
            r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$",
        )
        return True
    except InvalidChar as ex:
        raise InvalidField("email address") from ex


def validate_fields(fields: Iterable[str]) -> None:
    allowed_chars = (
        r"a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ\s'~:;%@&_$#=¡!¿"
        r"\,\.\*\-\?\"\[\]\|\(\)\/\{\}\>\+"
    )
    regex = rf'^[{allowed_chars.replace("=", "")}][{allowed_chars}]*$'
    for field in map(str, fields):
        if field:
            check_field(field, regex)


def isinstance_namedtuple(obj: object) -> bool:
    return (
        isinstance(obj, tuple)
        and hasattr(obj, "_asdict")
        and hasattr(obj, "_fields")
    )


def check_all_attr(obj: object, regex: str, ex: CustomBaseException) -> None:
    for val in list(cast(NamedTuple, obj)._asdict().values()):
        check_exp(str(val), regex, ex)


def check_all_list(
    list_to_check: list[str], regex: str, ex: CustomBaseException
) -> None:
    for val in list_to_check:
        if val:
            check_exp(str(val), regex, ex)


def check_fields(
    fields: Iterable[str], kwargs: dict, ex: CustomBaseException
) -> None:
    allowed_chars = (
        r"a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ\s'~:;%@&_$#=¡!¿"
        r"\,\.\*\-\?\"\[\]\|\(\)\/\{\}\>\+"
    )
    regex = rf'^[{allowed_chars.replace("=", "")}][{allowed_chars}]*$'
    for field in fields:
        value = kwargs.get(field)
        if isinstance_namedtuple(value):
            check_all_attr(value, regex, ex)
        elif isinstance(value, list):
            check_all_list(value, regex, ex)
        elif "." in field:
            obj_name, attr_name = field.split(".")
            obj = kwargs.get(obj_name)
            if obj_name in kwargs:
                field_content = getattr(obj, attr_name)
                if field_content:
                    check_exp(str(field_content), regex, ex)
        elif field in kwargs and value:
            check_exp(str(value), regex, ex)


def is_fluid_staff(email: str) -> bool:
    return email.endswith("@fluidattacks.com")


def validate_url(url: str | None) -> None:
    clean_url: str = url if url is not None else ""
    encoded_chars_whitelist: list[str] = ["%20"]
    for encoded_char in encoded_chars_whitelist:
        clean_url = clean_url.replace(encoded_char, "")

    if clean_url:
        allowed_chars = r"a-zA-Z0-9(),./:;@_$#=\?-"
        check_field(
            clean_url,
            rf'^[{allowed_chars.replace("=", "")}]+[{allowed_chars}]*$',
        )


def check_url(url: str | None, ex: CustomBaseException) -> None:
    clean_url: str = url if url is not None else ""
    encoded_chars_whitelist: list[str] = ["%20"]
    for encoded_char in encoded_chars_whitelist:
        clean_url = clean_url.replace(encoded_char, "")

    if clean_url:
        allowed_chars = r"a-zA-Z0-9(),./:;@_$#=\?-"
        check_exp(
            clean_url,
            rf'^[{allowed_chars.replace("=", "")}]+[{allowed_chars}]*$',
            ex,
        )


def validate_chart_field(param_value: str, param_name: str) -> None:
    is_valid = bool(re.search("^[A-Za-z0-9 #_-]*$", str(param_value)))
    if not is_valid:
        raise InvalidChar(param_name)


def validate_file_name(name: str) -> None:
    """Verify that filename has valid characters. Raises InvalidChar
    otherwise."""
    name = str(name)
    name_len = len(name.split("."))
    if name_len <= 2:
        is_valid = bool(
            re.search("^[A-Za-z0-9!_.*/'()&$@=;:+,? -]*$", str(name))
        )
        if not is_valid:
            raise InvalidChar("filename")
    else:
        raise InvalidChar("filename")


def validate_file_exists(
    file_name: str, group_files: list[GroupFile] | None
) -> None:
    """Verify that file name is not already in group files."""
    if group_files:
        file_to_check = next(
            (
                group_file
                for group_file in group_files
                if group_file.file_name == file_name
            ),
            None,
        )
        if file_to_check is not None:
            raise ErrorFileNameAlreadyExists.new()


def check_field(field: str, regexp: str) -> None:
    if not re.match(regexp, field.replace("\n", " ").strip(), re.MULTILINE):
        raise InvalidChar()


def check_length(
    payload: str,
    min_length: int | None = None,
    max_length: int | None = None,
    ex: CustomBaseException = InvalidFieldLength(),
) -> bool:
    """
    Checks if payload length is between `min_length` and `max_length` and
    returns **True** if it is. Otherwise, throws ex.

    min_length and max_length are inclusive and optional.
    If they are not provided, they are not checked.
    """
    if payload is None:
        raise ex
    str_length = len(payload)
    if (min_length is not None and str_length < min_length) or (
        max_length is not None and str_length > max_length
    ):
        raise ex
    return True


def validate_finding_id(finding_id: str) -> None:
    if not re.fullmatch(
        r"[0-9A-Za-z]{8}-[0-9A-Za-z]{4}-4[0-9A-Za-z]{3}-[89ABab]"
        r"[0-9A-Za-z]{3}-[0-9A-Za-z]{12}|\d+",
        finding_id,
    ):
        raise InvalidField("finding id")


def validate_group_language(language: str) -> None:
    if language.upper() not in {"EN", "ES"}:
        raise InvalidField("group language")


def validate_group_name(group_name: str) -> None:
    if not group_name.isalnum():
        raise InvalidField("group name")


def validate_markdown(text: str) -> str:
    """
    Escapes special characters and accepts only
    the use of certain html tags
    """
    allowed_tags = [
        "a",
        "b",
        "br",
        "div",
        "dl",
        "dt",
        "em",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "img",
        "li",
        "ol",
        "p",
        "small",
        "strong",
        "table",
        "tbody",
        "td",
        "tfoot",
        "th",
        "tr",
        "tt",
        "ul",
    ]
    allowed_attrs = {
        "a": ["href", "rel", "target"],
        "img": ["src", "alt", "width", "height"],
    }
    cleaned = bleach.clean(
        text,
        tags=allowed_tags,
        attributes=allowed_attrs,
    )
    cleaned = cleaned.replace("&amp;", "&")
    if text != cleaned:
        raise InvalidMarkdown()

    return cleaned


def validate_missing_severity_field_names(field_names: set[str]) -> None:
    missing_field_names = {
        utils.snakecase_to_camelcase(field)
        for field in CVSS31Severity._fields
        if field not in field_names
    }
    if missing_field_names:
        raise IncompleteSeverity(missing_field_names)


def validate_update_severity_values(dictionary: dict) -> None:
    if (
        len(
            list(
                filter(
                    lambda item: item[1] < 0 or item[1] > 10,
                    dictionary.items(),
                )
            )
        )
        > 0
    ):
        raise InvalidSeverityUpdateValues()


def validate_space_field(field: str) -> None:
    if not re.search(r"\S", field):
        raise InvalidSpacesField


def check_alnum(field: str) -> bool:
    is_alnum = all(word.isalnum() for word in field.split())
    return is_alnum or field == "-" or not field


def validate_alphanumeric_field(field: str) -> bool:
    """Optional whitespace separated string, with alphanumeric characters."""
    if check_alnum(field=field):
        return True
    raise InvalidField()


def validate_finding_title_change_policy(
    old_title: str, new_title: str, status: FindingStatus
) -> bool:
    """Blocks finding title changes from going through if the Finding has been
    already approved"""
    if old_title != new_title and status in [
        FindingStatus.SAFE,
        FindingStatus.VULNERABLE,
    ]:
        raise InvalidFieldChange(
            fields=["title"],
            reason=(
                "The title of a Finding cannot be edited if there are "
                "vulnerabilities on it"
            ),
        )
    return True


def get_attr_value(field: str, kwargs: dict, obj_type: type[T]) -> T:
    if "." not in field:
        return cast(T, kwargs.get(field))
    obj_name, obj_attr = field.split(".", 1)
    parts = obj_attr.split(".")
    obj = kwargs.get(obj_name)
    for part in parts:
        value = getattr(obj, part)
        obj = value
    if isinstance_namedtuple(value) and obj_type is dict:
        return value._asdict()
    if not isinstance(value, obj_type):
        return cast(T, value)
    return value


def get_sized_attr_value(field: str, kwargs: dict) -> Sized:
    if "." in field:
        obj_name, obj_attr = field.split(".", 1)
        parts = obj_attr.split(".")
        obj = kwargs[obj_name]
        field_name = parts[-1]
        for part in parts:
            value = getattr(obj, part)
            obj = value
    else:
        value = kwargs[field]
        field_name = field
    if not isinstance(value, Sized):
        raise InvalidField(field_name)
    return value


def validate_no_duplicate_drafts(
    new_title: str, drafts: tuple[Finding, ...], findings: tuple[Finding, ...]
) -> bool:
    """Checks for new draft proposals that are already present in the group,
    returning `True` if there are no duplicates"""
    for draft in drafts:
        if new_title == draft.title:
            raise DuplicateDraftFound(kind="draft")
    for finding in findings:
        if new_title == finding.title:
            raise DuplicateDraftFound(kind="finding")
    return True


def check_and_set_min_time_to_remediate(mttr: int | str | None) -> int | None:
    """Makes sure that min_time_to_remediate is either None or a positive
    number and returns it as an integer."""
    try:
        if mttr is None:
            return None
        if int(mttr) > 0:
            return int(mttr)
        raise InvalidMinTimeToRemediate()
    except ValueError as error:
        raise InvalidMinTimeToRemediate() from error


def validate_sanitized_csv_input(*fields: str) -> None:
    """Checks for the presence of any character that could be interpreted as
    the start of a formula by a spreadsheet editor according to
    https://owasp.org/www-community/attacks/CSV_Injection"""
    forbidden_characters: tuple[str, ...] = (
        "-",
        "=",
        "+",
        "@",
        "\t",
        "\r",
        "\n",
        "\\",
    )
    separators: tuple[str, ...] = ('"', "'", ",", ";")
    fields_union = [field.split() for field in fields]
    fields_flat = list(itertools.chain(*fields_union))
    for field in fields_flat:
        for character in forbidden_characters:
            # match characters at the beginning of string
            if re.match(re.escape(character), field):
                raise UnsanitizedInputFound()
            # check for field separator and quotes
            char_locations: list[int] = [
                match.start()
                for match in re.finditer((re.escape(character)), field)
            ]
            for location in char_locations:
                if any(
                    separator in field[location - 1]
                    for separator in separators
                ):
                    raise UnsanitizedInputFound()


def validate_commit_hash(commit_hash: str) -> None:
    if not (
        # validate SHA-1
        re.match(
            r"^[A-Fa-f0-9]{40}$",
            commit_hash,
        )
        # validate SHA-256
        or re.match(
            r"^[A-Fa-f0-9]{64}$",
            commit_hash,
        )
    ):
        raise InvalidCommitHash()


def check_commit_hash(commit_hash: str, ex: CustomBaseException) -> None:
    # validate SHA-1 or SHA-256
    check_exp(commit_hash, r"^[A-Fa-f0-9]{40}$|^[A-Fa-f0-9]{64}$", ex)


def validate_int_range(
    value: int, lower_bound: int, upper_bound: int, inclusive: bool = True
) -> None:
    if inclusive:
        if not lower_bound <= value <= upper_bound:
            raise NumberOutOfRange(lower_bound, upper_bound, inclusive)
    else:
        if not lower_bound < value < upper_bound:
            raise NumberOutOfRange(lower_bound, upper_bound, inclusive)


def validate_start_letter(value: str) -> None:
    if not value[0].isalpha():
        raise InvalidReportFilter("Password should start with a letter")


def validate_include_number(value: str) -> None:
    if not re.search(r"\d", value):
        raise InvalidReportFilter(
            "Password should include at least one number"
        )


def validate_include_lowercase(value: str) -> None:
    if not any(val.islower() for val in value):
        raise InvalidReportFilter(
            "Password should include lowercase characters"
        )


def validate_include_uppercase(value: str) -> None:
    if not any(val.isupper() for val in value):
        raise InvalidReportFilter(
            "Password should include uppercase characters"
        )


def sequence_increasing(
    char: str, current_ord: int, sequence: list[int], is_increasing: bool
) -> list[int]:
    if is_increasing and str(chr(sequence[-1])).isalnum() and char.isalnum():
        return [*sequence, current_ord]

    return [current_ord]


def sequence_decreasing(
    char: str, current_ord: int, sequence: list[int], is_increasing: bool
) -> list[int]:
    if (
        not is_increasing
        and str(chr(sequence[-1])).isalnum()
        and char.isalnum()
    ):
        return [*sequence, current_ord]

    return [current_ord]


def has_sequence(value: str, sequence_size: int = 3) -> bool:
    if len(value) < sequence_size or sequence_size <= 0:
        return False

    sequence: list[int] = [ord(value[0])]
    is_increasing = False
    for char in value[1:]:
        current_ord: int = ord(char)

        if sequence[-1] + 1 == current_ord:
            if len(sequence) == 1:
                is_increasing = True
            sequence = sequence_increasing(
                char, current_ord, sequence, is_increasing
            )
        elif sequence[-1] - 1 == current_ord:
            if len(sequence) == 1:
                is_increasing = False
            sequence = sequence_decreasing(
                char, current_ord, sequence, is_increasing
            )
        else:
            sequence = [current_ord]

        if len(sequence) == sequence_size:
            return True

    return False


def validate_sequence(value: str) -> None:
    if has_sequence(value):
        raise InvalidReportFilter(
            "Password should not include sequentials characters"
        )


def validate_symbols(value: str) -> None:
    if not re.search(r"[!\";#\$%&'\(\)\*\+,-./:<=>\?@\[\]^_`\{\|\}~]", value):
        raise InvalidReportFilter("Password should include symbols characters")


def check_range(
    value: int,
    lower_bound: int,
    upper_bound: int,
    inclusive: bool,
    ex: CustomBaseException,
) -> None:
    if inclusive:
        if not lower_bound <= value <= upper_bound:
            raise ex
    else:
        if not lower_bound < value < upper_bound:
            raise ex


def check_range_severity(
    severity: int,
    min_value: Decimal,
    max_value: Decimal,
    ex: CustomBaseException,
) -> None:
    if severity and severity != -1:
        check_range(
            severity,
            int(min_value),
            int(max_value),
            False,
            ex,
        )
