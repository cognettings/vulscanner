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
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def get_eval_results(
    method: MethodsEnum,
    graph: Graph,
    n_id: NId,
    danger_stmt: str,
    method_supplies: MethodSupplies,
) -> bool:
    for path in get_backward_paths(graph, n_id):
        eval_res = evaluate(
            method, graph, path, n_id, method_supplies.graph_db
        )
        if (
            eval_res
            and danger_stmt in eval_res.triggers
            and len(eval_res.triggers.intersection({"secure", "httponly"}))
            != 2
        ):
            return True
    return False


def is_attribute_weak(
    method: MethodsEnum,
    graph: Graph,
    obj_id: NId,
    al_id: NId,
    method_supplies: MethodSupplies,
) -> bool:
    args_ids = g.adj_ast(graph, al_id)
    if (
        len(args_ids) >= 2
        and graph.nodes[args_ids[0]].get("symbol") == "cookieName"
        and get_eval_results(
            method, graph, obj_id, "userrequest", method_supplies
        )
        and get_eval_results(
            method, graph, args_ids[1], "weakrandom", method_supplies
        )
    ):
        return True

    return False


def is_weak_random(
    method: MethodsEnum,
    graph: Graph,
    obj_id: NId,
    al_id: NId,
    method_supplies: MethodSupplies,
) -> bool:
    if graph.nodes[obj_id].get("expression") == "getSession":
        return is_attribute_weak(method, graph, obj_id, al_id, method_supplies)

    if (
        (args_ids := g.adj_ast(graph, al_id))
        and len(args_ids) == 1
        and get_eval_results(
            method, graph, obj_id, "userresponse", method_supplies
        )
    ):
        return get_eval_results(
            method, graph, args_ids[0], "weakrandom", method_supplies
        )

    return False


def java_weak_random(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_WEAK_RANDOM_COOKIE
    danger_methods = {"setAttribute", "addCookie"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            expr = n_attrs["expression"].split(".")
            if (
                expr[-1] in danger_methods
                and (obj_id := n_attrs.get("object_id"))
                and (al_id := graph.nodes[node].get("arguments_id"))
                and is_weak_random(
                    method, graph, obj_id, al_id, method_supplies
                )
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f034.use_insecure_random_method",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
