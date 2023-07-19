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
from utils import (
    graph as g,
)


def is_vulnerable_origin(
    method: MethodsEnum, graph: Graph, nid: NId, check: str
) -> bool:
    arg_id = graph.nodes[nid].get("arguments_id")
    if not arg_id:
        return False

    childs = g.adj_ast(graph, arg_id)
    test_node = None
    if (
        check == "add"
        and len(childs) > 1
        and graph.nodes[childs[0]].get("value")
        == '"Access-Control-Allow-Origin"'
    ):
        test_node = childs[1]

    if check in {"allowedorigins", "addallowedorigin"} and len(childs) == 1:
        test_node = childs[0]

    if test_node:
        return get_node_evaluation_results(method, graph, test_node, set())

    return False


def java_insecure_cors_origin(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_CORS_ORIGIN
    insecure_methods = {"add", "allowedorigins", "addallowedorigin"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            expr = graph.nodes[nid].get("expression")
            if (
                expr
                and expr.lower() in insecure_methods
                and is_vulnerable_origin(method, graph, nid, expr.lower())
            ):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="f134.cors_policy_allows_any_origin",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def _has_vulnerable_modifiers(
    graph: Graph, annot_ids: list[NId]
) -> NId | None:
    for _id in annot_ids:
        if graph.nodes[_id]["name"] != "CrossOrigin" or not (
            al_id := g.match_ast_d(graph, _id, "ArgumentList")
        ):
            continue

        for arg_id in g.match_ast_group_d(graph, al_id, "NamedArgument"):
            if (
                graph.nodes[arg_id]["argument_name"] == "origins"
                and (val_id := graph.nodes[arg_id]["value_id"])
                and (value := graph.nodes[val_id].get("value"))
                and value[1:-1] == "*"
            ):
                return arg_id
    return None


def java_insecure_cors_origin_modifier(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_CORS_ORIGIN

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (modif_id := graph.nodes[nid].get("modifiers_id"))
                and (
                    annot_ids := g.match_ast_group_d(
                        graph, modif_id, "Annotation"
                    )
                )
                and (vuln_id := _has_vulnerable_modifiers(graph, annot_ids))
            ):
                yield shard, vuln_id

    return get_vulnerabilities_from_n_ids(
        desc_key="f134.cors_policy_allows_any_origin",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
