from arch_lint.dag import (
    DagMap,
)
from arch_lint.graph import (
    FullPathModule,
)
from typing import (
    Dict,
    FrozenSet,
    Tuple,
    TypeVar,
    Union,
)

_T = TypeVar("_T")


def _raise_or_return(item: _T | Exception) -> _T:
    if isinstance(item, Exception):
        raise item
    return item


_dag: Dict[str, Tuple[Union[Tuple[str, ...], str], ...]] = {
    "db_snapshot": (
        "core",
        "_logger",
    ),
}


def project_dag() -> DagMap:
    return _raise_or_return(DagMap.new(_dag))


def forbidden_allowlist() -> Dict[FullPathModule, FrozenSet[FullPathModule]]:
    _raw: Dict[str, FrozenSet[str]] = {}
    return {
        FullPathModule.assert_module(k): frozenset(
            FullPathModule.assert_module(i) for i in v
        )
        for k, v in _raw.items()
    }
