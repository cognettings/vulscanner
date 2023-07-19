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


def is_lambda_danger(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    block_id = graph.nodes[n_id]["block_id"]
    if graph.nodes[block_id]["label_type"] == "ExecutionBlock" and (
        return_id := g.match_ast_d(graph, block_id, "Return")
    ):
        return get_node_evaluation_results(method, graph, return_id, set())
    return get_node_evaluation_results(method, graph, block_id, set())


def is_validation_dangerous(
    graph: Graph, n_id: NId, method: MethodsEnum
) -> bool:
    parent_id = g.pred(graph, n_id)[0]
    if graph.nodes[parent_id]["label_type"] == "Assignment":
        assign_id = g.adj_ast(graph, parent_id)[1]
        label_type = graph.nodes[assign_id]["label_type"]
        if label_type == "MethodDeclaration" and is_lambda_danger(
            graph, assign_id, method
        ):
            return True
    return False


def c_sharp_insecure_certificate_validation(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSECURE_CERTIFICATE_VALIDATION
    danger_m = "ServerCertificateValidationCallback"

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get(
                "member"
            ) == danger_m and is_validation_dangerous(graph, node, method):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f060.insecure_certificate_validation",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
