from collections.abc import (
    Iterator,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
    Graph,
    GraphShard,
    GraphShardNode,
    MethodSupplies,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def has_http_only_attr(
    method: MethodsEnum, graph: Graph, n_id: NId, cookie_name: str
) -> bool:
    for path in get_backward_paths(graph, n_id):
        for node in path:
            n_attrs = graph.nodes[node]
            if (
                n_attrs.get("label_type") == "MethodInvocation"
                and n_attrs.get("expression")
                == cookie_name + "." + "setSecure"
                and n_attrs.get("label_type") == "MethodInvocation"
                and n_attrs.get("arguments_id")
                and graph.nodes.get(n_attrs.get("expression_id")).get(
                    "expression"
                )
                == cookie_name
            ):
                return get_node_evaluation_results(
                    method, graph, n_attrs["arguments_id"], set()
                )
    return True


def analyze_insecure_cookie(
    method: MethodsEnum, graph: Graph, expr_id: NId, al_id: NId
) -> bool:
    args_ids = g.adj_ast(graph, al_id)
    if (
        len(args_ids) == 1
        and get_node_evaluation_results(
            method, graph, expr_id, {"userresponse"}
        )
        and (cookie_name := graph.nodes[args_ids[0]].get("symbol"))
        and get_node_evaluation_results(
            method, graph, args_ids[0], {"isCookieObject"}
        )
    ):
        return has_http_only_attr(method, graph, args_ids[0], cookie_name)
    return False


def kt_cookie_set_secure(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.KOTLIN_SECURE_COOKIE
    danger_methods = {"addCookie"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            expr = n_attrs["expression"].split(".")
            if (
                expr[-1] in danger_methods
                and (obj_id := n_attrs.get("expression_id"))
                and (symbol_id := graph.nodes[obj_id].get("expression_id"))
                and (al_id := graph.nodes[n_id].get("arguments_id"))
                and analyze_insecure_cookie(method, graph, symbol_id, al_id)
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f130.set_cookie_set_secure",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
