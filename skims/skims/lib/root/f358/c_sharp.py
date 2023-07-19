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


def get_vuln_nodes(
    graph: Graph,
    node: NId,
    method: MethodsEnum,
    method_supplies: MethodSupplies,
) -> bool:
    nodes = graph.nodes
    if (
        (parent_n_id := next(iter(g.pred_ast(graph, node)), None))
        and nodes[parent_n_id].get("label_type") == "Assignment"
        and (sibling_n_id := nodes[parent_n_id].get("value_id"))
        and get_node_evaluation_results(
            method,
            graph,
            sibling_n_id,
            {"return_true"},
            False,
            graph_db=method_supplies.graph_db,
        )
    ):
        return True

    return False


def c_sharp_cert_validation_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_CERT_VALIDATION_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if (
                graph.nodes[node].get("expression") == "ServicePointManager"
                and graph.nodes[node].get("member")
                == "ServerCertificateValidationCallback"
                and get_vuln_nodes(graph, node, method, method_supplies)
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f358.csharp_cert_validation_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
