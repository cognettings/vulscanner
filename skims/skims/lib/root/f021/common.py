from lib.root.utilities.common import (
    check_methods_expression,
)
from lib.root.utilities.javascript import (
    file_imports_module,
)
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


def insecure_dynamic_xpath(
    graph: Graph, method: MethodsEnum, method_supplies: MethodSupplies
) -> list[NId]:
    vuln_nodes: list[NId] = []
    danger_methods = {"select", "parse"}
    danger_set = {"userparameters"}
    if not (
        file_imports_module(graph, "fs")
        and file_imports_module(graph, "xpath")
    ):
        return vuln_nodes
    for n_id in method_supplies.selected_nodes:
        if (
            check_methods_expression(graph, n_id, danger_methods)
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and (args_ids := g.adj_ast(graph, al_id))
            and len(args_ids) >= 1
            and get_node_evaluation_results(
                method, graph, args_ids[0], danger_set
            )
        ):
            vuln_nodes.append(n_id)
    return vuln_nodes
