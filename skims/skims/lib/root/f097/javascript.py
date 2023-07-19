from collections.abc import (
    Iterator,
)
from lib.root.f097.common import (
    get_vulns_n_ids,
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


def has_reverse_tabnabbing(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JS_HAS_REVERSE_TABNABBING

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            f_name = graph.nodes[n_id].get("expression")
            if f_name == "window.open" and get_vulns_n_ids(graph, n_id):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f097.has_reverse_tabnabbing",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
