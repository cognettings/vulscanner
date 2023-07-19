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
    pred_ast,
)


def is_danger_expression(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    n_attrs = graph.nodes[n_id]
    memb = n_attrs["member"]
    parent_id = pred_ast(graph, n_id)[0]
    if (
        memb != "search_s"
        or graph.nodes[parent_id]["label_type"] != "MethodInvocation"
        or not get_node_evaluation_results(
            method, graph, n_attrs["expression_id"], {"ldapconnect"}
        )
    ):
        return False

    m_attrs = graph.nodes[parent_id]
    al_id = m_attrs.get("arguments_id")
    if not al_id:
        return False
    args_ids = adj_ast(graph, al_id)

    if (
        len(args_ids) > 2
        and get_node_evaluation_results(
            method, graph, args_ids[0], {"userparams"}
        )
        and get_node_evaluation_results(
            method, graph, args_ids[2], {"userparams"}
        )
    ):
        return True

    return False


def python_ldap_injection(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_LDAP_INJECTION

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            if is_danger_expression(graph, n_id, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f107.ldap_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
