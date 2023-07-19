"""
    This utils package houses the schema deprecation parsing and filters to
    find out and report overdue fields in the schema and gather the needed info
    to send deprecation notices
"""
from custom_utils.deprecations.ast import (
    get_deprecations_by_period,
    get_due_date,
)
from custom_utils.deprecations.filters import (
    filter_api_deprecation_dict,
    filter_api_deprecation_list,
)
from custom_utils.deprecations.types import (
    ApiDeprecation,
    ApiFieldType,
)

__all__ = [
    "ApiDeprecation",
    "ApiFieldType",
    "filter_api_deprecation_dict",
    "filter_api_deprecation_list",
    "get_deprecations_by_period",
    "get_due_date",
]
