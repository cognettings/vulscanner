from model import (
    core,
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


def is_insecure_jwt(
    graph: Graph,
    n_id: NId,
    method: core.MethodsEnum,
) -> bool:
    danger_set = {"unsafealgorithm"}
    member = graph.nodes[n_id].get("member")

    parent = g.pred(graph, n_id)[0]
    al_id = graph.nodes[parent].get("arguments_id")
    if not al_id:
        return False

    args_ids = g.adj_ast(graph, al_id)
    if len(args_ids) > 2:
        return get_node_evaluation_results(
            method, graph, args_ids[2], danger_set
        )

    if member == "jwt" and len(args_ids) <= 2:
        return True

    return False
