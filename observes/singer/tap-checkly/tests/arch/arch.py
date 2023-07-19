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
    TypeVar,
)

_dag: Dict[str, FrozenList[FrozenList[str] | str]] = {
    "tap_checkly": (
        "cli",
        "streams",
        "state",
        ("singer", "api"),
        ("objs", "_utils", "_logger"),
    ),
    "tap_checkly.api": (
        ("alert_channels", "checks", "groups", "report"),
        ("_raw", "_utils"),
    ),
    "tap_checkly.api._raw": (("_requests", "_retry"),),
    "tap_checkly.api.alert_channels": (
        "_client",
        "_decode",
    ),
    "tap_checkly.api.checks": (
        "_client",
        "_decode",
        ("results", "status"),
    ),
    "tap_checkly.api.checks.results": ("_client", "_decode", "time_range"),
    "tap_checkly.api.checks.results._decode": (("_api_result", "_browser"),),
    "tap_checkly.api.checks.status": (
        "_client",
        "_decode",
    ),
    "tap_checkly.api.groups": (
        "_client",
        "_decode",
    ),
    "tap_checkly.api.report": (
        "_client",
        "_decode",
    ),
    "tap_checkly.singer": (
        ("_alert_channels", "_groups", "_report", "_checks"),
        ("_core", "_encoder"),
    ),
    "tap_checkly.singer._checks": (
        "_encoders",
        ("results", "status"),
    ),
    "tap_checkly.singer._checks.results._encoders": (
        ("_core", "_api", "_browser"),
    ),
    "tap_checkly.streams": (
        "_emit",
        ("_reports", "_state", "_objs"),
    ),
    "tap_checkly.objs": (
        "_root",
        "_report",
        "_group",
        "_subscriptions",
        ("_check", "_alert", "_dashboard", "result"),
        "_id_objs",
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
        "requests": frozenset(["tap_checkly.api._raw._requests"]),
    }
    return {
        raise_or_return(FullPathModule.from_raw(k)): frozenset(
            raise_or_return(FullPathModule.from_raw(i)) for i in v
        )
        for k, v in _raw.items()
    }
