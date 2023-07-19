from model.core import (
    MethodsEnum,
)
from model.graph import (
    Graph,
    NId,
)
from symbolic_eval.evaluate import (
    evaluate,
    get_node_evaluation_results,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def local_storage_from_http(
    graph: Graph, n_id: NId, method: MethodsEnum
) -> NId | None:
    if (
        graph.nodes[n_id].get("expression") == "localStorage.setItem"
        and (parameters_n_id := g.match_ast_d(graph, n_id, "ArgumentList"))
        and (val_id := g.adj(graph, parameters_n_id)[1])
        and get_node_evaluation_results(method, graph, val_id, set())
    ):
        return val_id
    return None


def vuln_assignment_n_ids(
    graph: Graph, method: MethodsEnum, n_id: NId
) -> set[NId]:
    vuln_nodes: set[NId] = set()
    for path in get_backward_paths(graph, n_id):
        if evaluation := evaluate(method, graph, path, n_id):
            vuln_n_ids = set(
                map(lambda x: x.split("this_")[1], evaluation.triggers)
            )
            vuln_nodes.update(vuln_n_ids)
    return vuln_nodes


def local_storage_from_assignment(
    graph: Graph, n_id: NId, method: MethodsEnum
) -> set[NId]:
    vuln_nodes: set[NId] = set()
    if (
        (var_id := graph.nodes[n_id].get("variable_id"))
        and (graph.nodes[var_id].get("label_type") == "MemberAccess")
        and (graph.nodes[var_id].get("member") == "client")
        and (graph.nodes[var_id].get("expression") == "onload")
    ):
        danger_id = graph.nodes[n_id].get("value_id")
        vuln_n_ids = vuln_assignment_n_ids(graph, method, danger_id)
        vuln_nodes.update(vuln_n_ids)
    return vuln_nodes
