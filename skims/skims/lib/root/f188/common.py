from model.core import (
    MethodsEnum,
)
from model.graph import (
    Graph,
    NId,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def is_insec_invocation(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.triggers != {"origin_comparison"}:
            return True
    return False


def is_message_on_args(
    graph: Graph,
    n_id: NId,
) -> bool:
    arg_list = g.adj_ast(graph, n_id, label_type="ArgumentList")[0]
    args_childs = g.adj_ast(graph, arg_list)
    if (
        graph.nodes[args_childs[0]]["value"] == "'message'"
        and graph.nodes[args_childs[1]]["label_type"] == "MethodDeclaration"
    ):
        return True
    return False


def has_dangerous_param(
    graph: Graph, n_id: NId, method: MethodsEnum
) -> NId | None:
    sensitive_methods = {"window.addEventListener"}
    if (
        graph.nodes[n_id].get("expression") in sensitive_methods
        and is_message_on_args(graph, n_id)
        and is_insec_invocation(graph, n_id, method)
    ):
        return n_id
    return None
