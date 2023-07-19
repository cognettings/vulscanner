from .types import (
    IndicatorsChecker,
)
import logging
from typing import (
    Any,
    Callable,
)

LOGGER = logging.getLogger("cloudwatch")


def format_indicators(indicators: dict[str, Any]) -> dict[str, Any]:
    """Cleanup method for indicators.

    It adds the `unreliable_indicators` prefix to the keys of the
    `indicators` dict. Also, it removes the keys with `None` values.
    """
    return {
        f"unreliable_indicators.{key}": value
        for key, value in indicators.items()
    }


def _format_nested_key(key: str) -> str:
    return key.replace(".", "_")


def format_to_expression_attributes_names(values: set[str]) -> dict[str, str]:
    """Returns a dict with the `ExpressionAttributesNames`
    field format.

    Example: {"id", "name"} -> {"#id": "id", "#name": "name" }"""
    return {f"#{value}": value for value in values}


def format_to_project_expression(values: set[str]) -> str:
    """Returns a string with the `ProjectExpression`
    field format.

    Example: {"id", "name"} -> "#id,#name" """
    return ",".join([f"#{value}" for value in values])


def format_to_expression_attributes_values(
    values: dict[str, Any]
) -> dict[str, str]:
    """Returns a dict with the `ExpressionAttributesValues`
    field format.

    Example: {"id": 1, "first.name": "john"}
    -> {":id": 1, ":first_name": "john" }
    """
    return {
        f":{_format_nested_key(key)}": value for key, value in values.items()
    }


def format_to_update_expression(values: dict[str, Any]) -> str:
    """Returns a dict with the `UpdateExpression`
    field format.

    Example: {"id": 1, "first.name": "john"}
    -> "SET id = :id,first_name = :john"
    """
    return "SET " + ",".join(
        f"{key} = :{_format_nested_key(key)}" for key in values.keys()
    )


def is_zr_confirmed_or_requested(vuln: dict[str, Any]) -> bool:
    """ "If the vulnerability has zero risk and the status
    is `CONFIRMED` or `REQUESTED`, returns `True`.

    Otherwise, returns `False`."""
    return "zero_risk" in vuln and vuln["zero_risk"]["status"] in [
        "CONFIRMED",
        "REQUESTED",
    ]


def is_zr_requested(vuln: dict[str, Any]) -> bool:
    """ "If the vulnerability has zero risk and the status
    is `REQUESTED`, returns `True`.

    Otherwise, returns `False`."""
    return "zero_risk" in vuln and vuln["zero_risk"]["status"] in [
        "REQUESTED",
    ]


def verbose_for(field_name: str) -> Callable:
    """Decorator for adding verbose logs for
    specific field name once method finished.

    Args:
        field_name (str): Field name to log.
    """

    def wrapper(func: Callable) -> Callable:
        def decorated(*args: Any, **kwargs: Any) -> None:
            func(*args, **kwargs)
            params: IndicatorsChecker = kwargs.get("params", None)
            if params is None:
                return
            current = params.current_indicators.get(str(field_name))
            new = params.new_indicators.get(str(field_name))
            LOGGER.info("%s: %s -> %s", field_name, current, new)

        return decorated

    return wrapper
