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
from utils import (
    graph as g,
)


def only_one_argument(graph: Graph, n_id: NId) -> bool:
    if (args := g.match_ast(graph, n_id)) and (len(args) == 1):
        return True
    return False


def has_eval(method: MethodsEnum, graph: Graph, n_id: NId) -> bool:
    sensitive_methods = {"eval", "Function"}
    if (
        (
            graph.nodes[n_id].get("expression") in sensitive_methods
            or graph.nodes[n_id].get("name") in sensitive_methods
        )
        and (args_id := graph.nodes[n_id].get("arguments_id"))
        and only_one_argument(graph, args_id)
        and get_node_evaluation_results(method, graph, n_id, set())
    ):
        return True
    return False
