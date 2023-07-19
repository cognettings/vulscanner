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
from utils.graph import (
    adj_ast,
    matching_nodes,
)


def check_danger_arguments(graph: Graph, n_id: NId) -> bool:
    nodes = graph.nodes
    if (
        (args_n_id := nodes[n_id].get("arguments_id"))
        and (args := adj_ast(graph, args_n_id))
        and len(args) > 0
        and len(args) % 2 == 0
    ):
        for index in range(0, len(args), 2):
            if (
                (val_1 := nodes[args[index]].get("value"))
                and val_1[1:-1] == "Accept"
                and (val_2 := nodes[args[index + 1]].get("value"))
                and val_2[1:-1] == "*/*"
            ):
                return True
    return False


def get_vuln_nodes_plain(
    graph: Graph,
    method: MethodsEnum,
    dang_invocations: set[str],
    method_supplies: MethodSupplies,
) -> Iterator[NId]:
    for node in method_supplies.selected_nodes:
        if graph.nodes[node].get(
            "expression"
        ) in dang_invocations and get_node_evaluation_results(
            method, graph, node, {"all_myme_types_allowed"}
        ):
            yield node
    for node in matching_nodes(
        graph, label_type="ObjectCreation", name="Header"
    ):
        if check_danger_arguments(graph, node):
            yield node


def java_http_accepts_any_mime_type(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_HTTP_REQ_ACCEPTS_ANY_MIMETYPE
    dang_invocations: set[str] = {
        "setRequestProperty",
        "header",
        "setHeader",
        "addHeader",
        "add",
    }

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get(
                "expression"
            ) in dang_invocations and get_node_evaluation_results(
                method, graph, node, {"all_myme_types_allowed"}
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_http.analyze_headers.accept.insecure",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def java_http_accepts_any_mime_type_obj(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_HTTP_REQ_ACCEPTS_ANY_MIMETYPE

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get(
                "name"
            ) == "Header" and check_danger_arguments(graph, node):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_http.analyze_headers.accept.insecure",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def java_accepts_any_mime_type_chain(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_ACCEPTS_ANY_MIMETYPE_CHAIN
    dang_invocations: set[str] = {"header", "setHeader", "headers"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if (
                graph.nodes[node].get("expression") in dang_invocations
                and check_danger_arguments(graph, node)
                and get_node_evaluation_results(
                    method,
                    graph,
                    node,
                    set(),
                    graph_db=method_supplies.graph_db,
                )
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_http.analyze_headers.accept.insecure",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
