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
from utils.graph import (
    adj_ast,
    pred_ast,
)


def is_salting_unsafe(graph: Graph, n_id: NId) -> bool:
    parent_id = pred_ast(graph, n_id)[0]
    if (
        (args_id := graph.nodes[parent_id].get("arguments_id"))
        and (first_arg := next(iter(g.adj(graph, args_id)), None))
        and (
            args_salted := adj_ast(
                graph, first_arg, depth=2, strict=False, label_type="Literal"
            )
        )
        and len(args_salted) >= 1
        and all(len(adj_ast(graph, _id)) == 0 for _id in args_salted)
    ):
        return True
    return False


def get_vuln_nodes(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    if (
        graph.nodes[n_id].get("expression") == "update"
        and (member_id := g.adj_ast(graph, n_id)[0])
        and get_node_evaluation_results(
            method, graph, member_id, {"createHash"}
        )
        and is_salting_unsafe(graph, n_id)
    ):
        return True

    return False
