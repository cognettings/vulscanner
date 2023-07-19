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
)

DANGER_METHODS = {
    "ClientSession",
    "Request",
    "add_header",
    "add_unredirected_header",
    "urlopen",
    "make_headers",
    "delete",
    "get",
    "head",
    "patch",
    "post",
    "put",
    "request",
}


def is_danger_headers(
    method: MethodsEnum,
    graph: Graph,
    al_id: NId,
) -> bool:
    for _id in adj_ast(graph, al_id):
        if graph.nodes[_id].get("argument_name") != "headers":
            continue
        val_id = graph.nodes[_id]["value_id"]
        return get_node_evaluation_results(
            method, graph, val_id, {"danger_accept"}, False
        )
    return False


def python_danger_accept_header(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_ACCEPTS_ANY_MIME

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            m_attrs = graph.nodes[n_id]
            expr = str(m_attrs.get("expression"))
            if (
                expr.rsplit(".", maxsplit=1)[-1] in DANGER_METHODS
                and (al_id := m_attrs.get("arguments_id"))
                and is_danger_headers(method, graph, al_id)
                and (expr_id := m_attrs.get("expression_id"))
                and get_node_evaluation_results(
                    method,
                    graph,
                    expr_id,
                    {"client_connection"},
                    False,
                )
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="f153.accept_header_insecure",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
