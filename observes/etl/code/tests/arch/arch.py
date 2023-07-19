from arch_lint.dag import (
    DagMap,
)
from arch_lint.graph import (
    FullPathModule,
)
from fa_purity import (
    FrozenList,
)
from typing import (
    Dict,
    FrozenSet,
)

root = FullPathModule.assert_module("code_etl")
_dag: Dict[str, FrozenList[FrozenList[str] | str]] = {
    "code_etl": (
        "cli",
        ("init_tables", "compute_bills", "upload_repo", "migration"),
        "amend",
        "clients",
        ("client", "arm"),
        ("factories", "mailmap"),
        "objs",
        (
            "_logger",
            "_error",
            "_patch",
            "_utils",
            "str_utils",
            "time_utils",
            "parallel",
        ),
    ),
    "code_etl.compute_bills": (
        "_keeper",
        "_report",
        "_getter",
        ("core",),
    ),
    "code_etl.clients": (
        "_dry_client",
        "_real_client",
        "_raw",
        ("encoder", "_query", "decoder"),
        "_raw_file_commit",
        ("_raw_objs", "_assert"),
    ),
    "code_etl.client": (
        "_core",
        "_delta_update",
    ),
    "code_etl.amend": (
        "actions",
        "core",
    ),
    "code_etl.arm": (
        ("_ignored_paths", "_group_org"),
        "_raw_client",
        "_retry",
        "_error",
    ),
    "code_etl.arm._retry": (
        ("delay", "handlers"),
        "_core",
    ),
    "code_etl.clients._raw_file_commit": (
        "_client",
        ("_encode", "_decode", "_factory"),
    ),
    "code_etl.upload_repo": ("actions", ("extractor", "_ignored")),
}


def project_dag() -> DagMap:
    item = DagMap.new(_dag)
    if isinstance(item, Exception):
        raise item
    return item


def forbidden_allowlist() -> Dict[FullPathModule, FrozenSet[FullPathModule]]:
    _raw: Dict[str, FrozenSet[str]] = {}
    return {
        FullPathModule.assert_module(k): frozenset(
            FullPathModule.assert_module(i) for i in v
        )
        for k, v in _raw.items()
    }
