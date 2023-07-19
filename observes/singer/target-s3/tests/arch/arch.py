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
    Union,
)

root = FullPathModule.assert_module("target_s3")
_dag: Dict[str, Tuple[Union[Tuple[str, ...], str], ...]] = {
    "target_s3": (
        "_cli",
        "executor",
        "upload",
        "csv_keeper",
        "_grouper",
        "core",
        ("_s3", "_input", "_output", "_utils", "_parallel", "_logger"),
    ),
    "target_s3.core": (
        "_record_group",
        "_complete_record",
        "_plain_record",
        "_ro_file",
    ),
    "target_s3.csv_keeper": (
        "_writer",
        "_format",
        "_core",
    ),
}


def project_dag() -> DagMap:
    item = DagMap.new(_dag)
    if isinstance(item, Exception):
        raise item
    return item


def forbidden_allowlist() -> Dict[FullPathModule, FrozenSet[FullPathModule]]:
    _raw: Dict[str, FrozenSet[str]] = {
        "pathos": frozenset(["target_s3._parallel"]),
    }
    return {
        FullPathModule.assert_module(k): frozenset(
            FullPathModule.assert_module(i) for i in v
        )
        for k, v in _raw.items()
    }
