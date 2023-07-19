from arch_lint.dag import (
    DAG,
    DagMap,
)
from arch_lint.graph import (
    FullPathModule,
)
from fa_purity import (
    FrozenList,
)
from typing import (
    TypeVar,
)

_T = TypeVar("_T")
_dag: dict[str, FrozenList[FrozenList[str] | str]] = {
    "tap_json": (
        "cli",
        ("linearize", "auto_schema"),
        "_core",
        (
            "clean_str",
            "_logger",
            "env",
            "utils",
        ),
    ),
    "tap_json.auto_schema": (
        "_schema",
        "_types",
    ),
    "tap_json.linearize": (
        ("_to_table", "_flattener"),
        "_nested_id",
        "_core",
    ),
}


def raise_if_exception(item: _T | Exception) -> _T:
    if isinstance(item, Exception):
        raise item
    return item


def project_dag() -> DagMap:
    return raise_if_exception(DagMap.new(_dag))


def forbidden_allowlist() -> dict[FullPathModule, frozenset[FullPathModule]]:
    _raw: dict[str, frozenset[str]] = {}
    return {
        FullPathModule.assert_module(k): frozenset(
            FullPathModule.assert_module(i) for i in v
        )
        for k, v in _raw.items()
    }
