from model.core import (
    MethodsEnum,
)
from model.graph import (
    Graph,
    MethodSupplies,
    NId,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)


def weak_random(
    graph: Graph, method: MethodsEnum, method_supplies: MethodSupplies
) -> list[NId]:
    vuln_nodes: list[NId] = []
    for n_id in method_supplies.selected_nodes:
        if (
            "cookie" in graph.nodes[n_id]["expression"]
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and (test_nid := g.match_ast(graph, al_id).get("__1__"))
            and get_node_evaluation_results(
                method, graph, test_nid, {"Random"}, False
            )
        ):
            vuln_nodes.append(n_id)

    return vuln_nodes
