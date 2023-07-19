from model.core import (
    MethodsEnum,
)
from model.graph import (
    Graph,
    NId,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)


def insecure_http_headers(
    graph: Graph, n_id: NId, method: MethodsEnum
) -> bool:
    if graph.nodes[n_id].get(
        "name"
    ) == "HttpHeaders" and get_node_evaluation_results(
        method, graph, n_id, set()
    ):
        return True
    return False
