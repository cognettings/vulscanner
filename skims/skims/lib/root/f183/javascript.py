from collections.abc import (
    Iterator,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
    GraphShard,
    GraphShardNode,
    MethodSupplies,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def js_debugging_enabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JS_DEBUGGER_ENABLED

    def n_ids() -> Iterator[GraphShardNode]:
        for nid in method_supplies.selected_nodes:
            yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f183.debugger_enabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
