from model.graph import (
    Graph,
    MethodSupplies,
    NId,
)
from utils import (
    graph as g,
)


def _has_dangerous_literal(graph: Graph, args: dict) -> bool:
    sensitive_params = {'"*"'}
    if (
        len(args) == 2
        and (scnd_param := graph.nodes[args["__1__"]])
        and (scnd_param.get("label_type") == "Literal")
        and (scnd_param.get("value") in sensitive_params)
    ):
        return True
    return False


def has_dangerous_param(
    graph: Graph, method_supplies: MethodSupplies
) -> list[NId]:
    vuln_nodes: list[NId] = []
    sensitive_methods = {"contentWindow.postMessage"}

    for member in method_supplies.selected_nodes:
        if (
            graph.nodes[member].get("expression")[-25:] in sensitive_methods
            and (args_id := graph.nodes[member].get("arguments_id"))
            and (args := g.match_ast(graph, args_id))
            and (_has_dangerous_literal(graph, args))
        ):
            vuln_nodes.append(member)

    return vuln_nodes
