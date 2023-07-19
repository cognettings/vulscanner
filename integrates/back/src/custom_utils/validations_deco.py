import bleach
from collections.abc import (
    Callable,
    Iterable,
)
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
    utils,
    validations,
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
import functools
import itertools
import re
from typing import (
    Any,
)


def validate_email_address_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = validations.get_attr_value(
                field=field, kwargs=kwargs, obj_type=str
            )
            validations.check_email(
                field_content, InvalidField("email address")
            )
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_fields_deco(fields: Iterable[str]) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            validations.check_fields(fields, kwargs, InvalidChar())
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_url_deco(url_field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            url = validations.get_attr_value(
                field=url_field, kwargs=kwargs, obj_type=str
            )
            validations.check_url(url=url, ex=InvalidChar())
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_chart_field_deco(
    param_value_field: str, param_name_field: str
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            param_value = validations.get_attr_value(
                field=param_value_field, kwargs=kwargs, obj_type=str
            )
            param_name = validations.get_attr_value(
                field=param_name_field, kwargs=kwargs, obj_type=str
            )
            is_valid = bool(re.search("^[A-Za-z0-9 #_-]*$", str(param_value)))
            if not is_valid:
                raise InvalidChar(param_name)
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_chart_field_dict_deco(
    dict_field: str, params_names: Iterable[str]
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            dict_value = validations.get_attr_value(
                field=dict_field, kwargs=kwargs, obj_type=dict
            )
            for param_name in params_names:
                validations.check_exp(
                    str(dict_value.get(param_name)),
                    r"^[A-Za-z0-9 #_-]*$",
                    InvalidChar(param_name),
                )

            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_file_name_deco(field: str) -> Callable:
    """Verify that filename has valid characters. Raises InvalidChar
    otherwise."""

    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = str(
                validations.get_attr_value(
                    field=field, kwargs=kwargs, obj_type=str
                )
            )
            name_len = len(field_content.split("."))
            if name_len <= 2:
                is_valid = bool(
                    re.search(
                        "^[A-Za-z0-9!_.*/'()&$@=;:+,? -]*$", str(field_content)
                    )
                )
                if not is_valid:
                    raise InvalidChar("filename")
                return func(*args, **kwargs)
            raise InvalidChar("filename")

        return decorated

    return wrapper


def validate_file_exists_deco(
    field_name: str, field_group_files: str
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            file_name = validations.get_attr_value(
                field=field_name, kwargs=kwargs, obj_type=str
            )
            group_files = validations.get_attr_value(
                field=field_group_files,
                kwargs=kwargs,
                obj_type=list[GroupFile],
            )
            if group_files is not None:
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
            return func(*args, **kwargs)

        return decorated

    return wrapper


def _validate_field_length(
    field_content: Any, min_length: int | None, max_length: int | None
) -> bool:
    """This method validates field content
    according to type and length.

    If field_content was validated successfully, it returns True.
    Otherwise, it raises InvalidFieldLength.

    If field_content is None, it returns False.
    """
    if field_content is None:
        return False
    if isinstance(field_content, list):
        if min_length is not None and len(field_content) == 0:
            raise InvalidFieldLength()
        for val in field_content:
            validations.check_length(
                val, min_length, max_length, InvalidFieldLength()
            )
    if isinstance(field_content, str):
        validations.check_length(
            field_content, min_length, max_length, InvalidFieldLength()
        )
    return True


def validate_length_deco(
    field: str, min_length: int | None = None, max_length: int | None = None
) -> Callable:
    """
    Validates if field length is between `min_length` and
    `max_length` (inclusive).

    `min_length` and `max_length` are optional. If they are
    not provided, they are not checked.

    Empty strings are allowed when `min_length` is not defined.

    Backward compatibility: if an object has a field as `None`
    and you want to validate its length, it is always valid.

    Throws:
        InvalidFieldLength()
    """

    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = validations.get_attr_value(
                field=field, kwargs=kwargs, obj_type=str
            )
            _validate_field_length(field_content, min_length, max_length)
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_all_fields_length_deco(
    max_length: int, min_length: int | None = None
) -> Callable:
    """
    Validates if field length is between `min_length` and
    `max_length` (inclusive) for every field.

    `min_length` is optional. If they are
    not provided, they are not checked.

    Empty strings are allowed when `min_length` is not defined.

    Throws:
        InvalidFieldLength()
    """

    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            for value in kwargs.values():
                _validate_field_length(value, min_length, max_length)
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_fields_length_deco(
    fields: Iterable[str],
    min_length: int | None = None,
    max_length: int | None = None,
) -> Callable:
    """
    Validates if field length is between `min_length` and
    `max_length` (inclusive) for each field in `fields`.

    `min_length` and `max_length` are optional. If they are
    not provided, they are not checked.

    Empty strings are allowed when `min_length` is not defined.

    Backward compatibility: if an object has a field as `None`
    and you want to validate its length, it is always valid.

    Throws:
        InvalidFieldLength()
    """

    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            for field in fields:
                field_content = validations.get_sized_attr_value(
                    field=field, kwargs=kwargs
                )
                _validate_field_length(field_content, min_length, max_length)
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_finding_id_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = str(
                validations.get_attr_value(
                    field=field, kwargs=kwargs, obj_type=str
                )
            )
            if not re.fullmatch(
                r"[0-9A-Za-z]{8}-[0-9A-Za-z]{4}-4[0-9A-Za-z]{3}-[89ABab]"
                r"[0-9A-Za-z]{3}-[0-9A-Za-z]{12}|\d+",
                field_content,
            ):
                raise InvalidField("finding id")
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_group_language_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            language = str(
                validations.get_attr_value(
                    field=field, kwargs=kwargs, obj_type=str
                )
            )
            if language.upper() not in {"EN", "ES"}:
                raise InvalidField("group language")
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_group_name_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = str(
                validations.get_attr_value(
                    field=field, kwargs=kwargs, obj_type=str
                )
            )
            if not field_content.isalnum():
                raise InvalidField("group name")
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_markdown_deco(text_field: str) -> Callable:
    """
    Escapes special characters and accepts only
    the use of certain html tags
    """

    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            text = validations.get_attr_value(
                field=text_field, kwargs=kwargs, obj_type=str
            )
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
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_missing_severity_field_names_deco(
    field_names_field: str,
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_names = validations.get_attr_value(
                field=field_names_field, kwargs=kwargs, obj_type=set[str]
            )
            missing_field_names = {
                utils.snakecase_to_camelcase(field)
                for field in CVSS31Severity._fields
                if field not in field_names
            }
            if missing_field_names:
                raise IncompleteSeverity(missing_field_names)
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_update_severity_values_deco(dictionary_field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            dictionary = validations.get_attr_value(
                field=dictionary_field, kwargs=kwargs, obj_type=dict
            )
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
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_space_field_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = str(
                validations.get_attr_value(
                    field=field, kwargs=kwargs, obj_type=str
                )
            )
            if not re.search(r"\S", field_content):
                raise InvalidSpacesField
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_alphanumeric_field_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = str(
                validations.get_attr_value(
                    field=field, kwargs=kwargs, obj_type=str
                )
            )
            is_alnum = all(word.isalnum() for word in field_content.split())
            if is_alnum or field_content == "-" or not field_content:
                return func(*args, **kwargs)
            raise InvalidField()

        return decorated

    return wrapper


def validate_no_duplicate_drafts_deco(
    new_title_field: str, drafts_field: str, findings_field: str
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            new_title = validations.get_attr_value(
                field=new_title_field, kwargs=kwargs, obj_type=str
            )
            drafts = validations.get_attr_value(
                field=drafts_field, kwargs=kwargs, obj_type=tuple[Finding, ...]
            )
            findings = validations.get_attr_value(
                field=findings_field,
                kwargs=kwargs,
                obj_type=tuple[Finding, ...],
            )
            for draft in drafts:
                if new_title == draft.title:
                    raise DuplicateDraftFound(kind="draft")
            for finding in findings:
                if new_title == finding.title:
                    raise DuplicateDraftFound(kind="finding")
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_sanitized_csv_input_deco(field_names: list[str]) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> None:
            """Checks for the presence of any character that could be
            interpreted as the start of a formula by a spreadsheet editor
            according to
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
            fields_to_validate = [
                str(kwargs.get(field))
                if "." not in field
                else str(
                    getattr(
                        kwargs.get(field.split(".")[0]), field.split(".")[1]
                    )
                )
                for field in field_names
            ]
            fields_union = [field.split() for field in fields_to_validate]
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
            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_commit_hash_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            commit_hash = str(
                validations.get_attr_value(
                    field=field, kwargs=kwargs, obj_type=str
                )
            )
            validations.check_commit_hash(commit_hash, InvalidCommitHash())
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_int_range_deco(
    field: str, lower_bound: int, upper_bound: int, inclusive: bool
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            value = validations.get_attr_value(
                field=field, kwargs=kwargs, obj_type=int
            )
            validations.check_range(
                value,
                lower_bound,
                upper_bound,
                inclusive,
                NumberOutOfRange(lower_bound, upper_bound, inclusive),
            )
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_start_letter_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = str(
                validations.get_attr_value(
                    field=field, kwargs=kwargs, obj_type=str
                )
            )
            if not field_content[0].isalpha():
                raise InvalidReportFilter(
                    "Password should start with a letter"
                )
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_include_number_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = str(
                validations.get_attr_value(
                    field=field, kwargs=kwargs, obj_type=str
                )
            )
            if not re.search(r"\d", field_content):
                raise InvalidReportFilter(
                    "Password should include at least one number"
                )
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_include_lowercase_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = str(
                validations.get_attr_value(
                    field=field, kwargs=kwargs, obj_type=str
                )
            )
            if not any(val.islower() for val in field_content):
                raise InvalidReportFilter(
                    "Password should include lowercase characters"
                )
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_include_uppercase_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = str(
                validations.get_attr_value(
                    field=field, kwargs=kwargs, obj_type=str
                )
            )
            if not any(val.isupper() for val in field_content):
                raise InvalidReportFilter(
                    "Password should include uppercase characters"
                )
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_sequence_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            value = str(
                validations.get_attr_value(
                    field=field, kwargs=kwargs, obj_type=str
                )
            )
            if validations.has_sequence(value):
                raise InvalidReportFilter(
                    "Password should not include sequentials characters"
                )
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_symbols_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            value = str(
                validations.get_attr_value(
                    field=field, kwargs=kwargs, obj_type=str
                )
            )
            if not re.search(
                r"[!\";#\$%&'\(\)\*\+,-./:<=>\?@\[\]^_`\{\|\}~]", value
            ):
                raise InvalidReportFilter(
                    "Password should include symbols characters"
                )
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_severity_range_deco(
    field: str, min_value: Decimal, max_value: Decimal
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            severity = validations.get_attr_value(
                field=field, kwargs=kwargs, obj_type=int
            )
            validations.check_range_severity(
                severity,
                min_value,
                max_value,
                InvalidSeverity([min_value, max_value]),
            )
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_field_exist_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            if kwargs[field] is None:
                raise InvalidParameter(field)
            return func(*args, **kwargs)

        return decorated

    return wrapper
