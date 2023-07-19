from collections.abc import (
    Iterator,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
    Graph,
    GraphShard,
    GraphShardNode,
    MethodSupplies,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)


def is_unsafe_context(method: MethodsEnum, graph: Graph, n_id: NId) -> bool:
    if (
        val_id := graph.nodes[n_id].get("value_id")
    ) and get_node_evaluation_results(method, graph, val_id, set()):
        return True
    return False


def python_unsafe_ssl_hostname(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_UNSAFE_SSL_HOSTNAME

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            parent_id = g.pred_ast(graph, n_id)[0]
            if (
                n_attrs["member"] == "check_hostname"
                and is_unsafe_context(method, graph, parent_id)
                and get_node_evaluation_results(
                    method, graph, n_attrs["expression_id"], {"sslcontext"}
                )
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f060.common_unsafe_origin",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
