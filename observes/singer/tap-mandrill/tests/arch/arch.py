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

_dag: Dict[str, Tuple[Union[Tuple[str, ...], str], ...]] = {
    "tap_mandrill": (
        "cli",
        ("streams", "singer"),
        "api",
        ("_logger", "_files", "_utils"),
    ),
    "tap_mandrill.api": (
        "export",
        ("_api_key", "objs"),
        "_utils",
    ),
    "tap_mandrill.api.export": (
        "_api_1",
        "_core",
    ),
    "tap_mandrill.api.export._api_1": (
        ("_activity", "_download", "_get_job"),
        "_decode",
    ),
    "tap_mandrill.singer": (
        "activity",
        "core",
    ),
    "tap_mandrill._files": (
        "_zip_file",
        "_csv_file",
        "_str_file",
        "_bin_file",
    ),
}

_T = TypeVar("_T")


def raise_or_return(item: Exception | _T) -> _T:
    if isinstance(item, Exception):
        raise item
    return item


def project_dag() -> DagMap:
    return raise_or_return(DagMap.new(_dag))


def forbidden_allowlist() -> Dict[FullPathModule, FrozenSet[FullPathModule]]:
    _raw: Dict[str, FrozenSet[str]] = {
        "dateutil": frozenset(["tap_mandrill._utils"]),
        "mailchimp_transactional": frozenset(
            [
                "tap_mandrill.api.export._api_1._activity",
                "tap_mandrill.api.export._api_1._get_job",
                "tap_mandrill.api.export._api_1",
                "tap_mandrill.api._utils",
            ]
        ),
    }
    return {
        raise_or_return(FullPathModule.from_raw(k)): frozenset(
            raise_or_return(FullPathModule.from_raw(i)) for i in v
        )
        for k, v in _raw.items()
    }
