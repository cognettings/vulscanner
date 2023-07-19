from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Dict,
)

# This map is used to replace each key phrase with a
# shorter user defined alias in column names.
# Useful when column names exceed the maximum size.
_replace_map: Dict[str, str] = {}


def _transform_field_name(_field: str) -> str:
    result = _field
    for target, replacement in _replace_map.items():
        if target in _field:
            result = result.replace(target, replacement)
    return result


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class FieldName:
    _private: _Private = field(repr=False, hash=False, compare=False)
    raw: str

    @staticmethod
    def from_raw(raw: str) -> FieldName:
        return FieldName(
            _Private(), _transform_field_name(raw).replace("%", "%%").lower()
        )
