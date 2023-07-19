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
    match_ast_d,
    match_ast_group_d,
    pred_ast,
)


def is_unsafe_context(graph: Graph, n_id: NId) -> bool:
    if (al_id := match_ast_d(graph, n_id, "ArgumentList")) and (
        args := match_ast_group_d(graph, al_id, "NamedArgument")
    ):
        for _id in args:
            if (
                graph.nodes[_id]["argument_name"] == "verify"
                and (val_id := graph.nodes[_id]["value_id"])
                and graph.nodes[val_id].get("value") == "False"
            ):
                return True
    return False


def is_unsafe_certificate(
    method: MethodsEnum, graph: Graph, n_id: NId
) -> bool:
    if (
        val_id := graph.nodes[n_id].get("value_id")
    ) and get_node_evaluation_results(method, graph, val_id, {"cert_none"}):
        return True
    return False


def python_unsafe_certificate_validation(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_UNSAFE_CERTIFICATE_VALIDATION
    danger_memb = {"requests.get", "requests.request"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            parent_id = pred_ast(graph, n_id)[0]
            if (
                f"{n_attrs['expression']}.{n_attrs['member']}" in danger_memb
                and is_unsafe_context(graph, parent_id)
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f313.unsafe_certificate_validation",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def python_unsafe_ssl_context_certificate(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_UNSAFE_CERTIFICATE_VALIDATION

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            parent_id = pred_ast(graph, n_id)[0]
            if (
                n_attrs["member"] == "verify_mode"
                and is_unsafe_certificate(method, graph, parent_id)
                and get_node_evaluation_results(
                    method, graph, n_attrs["expression_id"], {"sslcontext"}
                )
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f313.unsafe_certificate_validation",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
