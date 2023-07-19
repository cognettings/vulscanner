from collections.abc import (
    Callable,
)
from custom_exceptions import (
    CustomBaseException,
    InvalidFieldLength,
    InvalidMobileNumber,
)
from custom_utils import (
    validations,
)
from db_model.stakeholders.types import (
    StakeholderPhone,
)
import functools
from typing import (
    Any,
)


def validate_phone(phone: StakeholderPhone) -> None:
    try:
        validations.check_length(phone.calling_country_code, max_length=3)
    except InvalidFieldLength as exc:
        raise InvalidMobileNumber() from exc
    try:
        validations.check_length(phone.national_number, max_length=12)
    except InvalidFieldLength as exc:
        raise InvalidMobileNumber() from exc

    if not (
        phone.calling_country_code.isdecimal()
        and phone.national_number.isdecimal()
    ):
        raise InvalidMobileNumber()


def _check_phone(phone: StakeholderPhone, ex: CustomBaseException) -> None:
    validations.check_length(
        phone.calling_country_code,
        max_length=3,
        ex=ex,
    )
    validations.check_length(
        phone.national_number,
        max_length=12,
        ex=ex,
    )
    if not (
        phone.calling_country_code.isdecimal()
        and phone.national_number.isdecimal()
    ):
        raise ex


def validate_phone_deco(phone_field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            phone = validations.get_attr_value(
                field=phone_field, kwargs=kwargs, obj_type=StakeholderPhone
            )
            if phone:
                _check_phone(phone=phone, ex=InvalidMobileNumber())
            return func(*args, **kwargs)

        return decorated

    return wrapper
