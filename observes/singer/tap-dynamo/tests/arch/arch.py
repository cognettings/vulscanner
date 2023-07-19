from arch_lint.dag import (
    DagMap,
)
from arch_lint.graph import (
    FullPathModule,
)
from typing import (
    Dict,
    FrozenSet,
    NoReturn,
    Tuple,
    TypeVar,
    Union,
)

_T = TypeVar("_T")


def raise_or_return(item: _T | Exception) -> _T | NoReturn:
    if isinstance(item, Exception):
        raise item
    return item


def _module(path: str) -> FullPathModule | NoReturn:
    return raise_or_return(FullPathModule.from_raw(path))


_dag: Dict[str, Tuple[Union[Tuple[str, ...], str], ...]] = {
    "tap_dynamo": (
        "cli",
        "extractor",
        ("client", "dynamo"),
        ("_logger", "_utils"),
    ),
    "tap_dynamo.dynamo": ("item_factory", "core"),
}


def project_dag() -> DagMap:
    return raise_or_return(DagMap.new(_dag))


def forbidden_allowlist() -> Dict[FullPathModule, FrozenSet[FullPathModule]]:
    _raw: Dict[str, FrozenSet[str]] = {
        "boto3": frozenset(
            [
                "tap_dynamo.client",
                "tap_dynamo.dynamo.item_factory",
                "tap_dynamo.dynamo.core",
            ]
        ),
        "pathos": frozenset(
            [
                "tap_dynamo._utils",
            ]
        ),
    }
    return {
        _module(k): frozenset(_module(i) for i in v) for k, v in _raw.items()
    }
