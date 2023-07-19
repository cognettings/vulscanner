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


def _has_dangerous_literal(graph: Graph, args: dict) -> bool:
    sensitive_params = {'"Set-Cookie"', '"connect.sid"'}
    if (
        len(args) == 2
        and (first_param := graph.nodes[args["__0__"]])
        and (first_param.get("label_type") == "Literal")
        and (first_param.get("value") in sensitive_params)
    ):
        return True
    return False


def has_dangerous_param(
    method: MethodsEnum,
    graph: Graph,
    member: NId,
) -> bool:
    sensitive_methods = {"res.setHeader", "res.cookie"}

    if (
        graph.nodes[member].get("expression") in sensitive_methods
        and (args_id := graph.nodes[member].get("arguments_id"))
        and (args := g.match_ast(graph, args_id))
        and (_has_dangerous_literal(graph, args))
        and get_node_evaluation_results(method, graph, member, set())
    ):
        return True

    return False
