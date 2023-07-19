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
from utils.string import (
    split_on_last_dot,
)


def get_vuln_nodes(graph: Graph, nid: NId, method: MethodsEnum) -> bool:
    danger_set = {"UserConnection", "NonParametrizedQuery"}
    f_name = split_on_last_dot(graph.nodes[nid]["expression"])
    if f_name[-1] == "query" and get_node_evaluation_results(
        method, graph, nid, danger_set, False
    ):
        return True

    return False
