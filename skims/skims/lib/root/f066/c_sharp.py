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
from utils import (
    graph as g,
)


def c_sharp_has_console_functions(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_HAS_CONSOLE_FUNCTIONS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            pred_nid = g.pred_ast(graph, node)[0]
            expr = graph.nodes[pred_nid].get("expression")
            if expr == "Console.WriteLine":
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f066.has_console_functions",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
