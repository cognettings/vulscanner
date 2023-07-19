from collections.abc import (
    Iterator,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
    GraphShard,
    GraphShardNode,
    MethodSupplies,
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


def kt_anonymous_ldap(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.KT_ANONYMOUS_LDAP

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            parent = pred_ast(graph, n_id)
            arg_list = graph.nodes[parent[0]].get("arguments_id")

            if (
                n_attrs["member"] == "put"
                and (child := adj_ast(graph, n_id)[0])
                and get_node_evaluation_results(
                    method, graph, child, {"enviromentConnection"}
                )
                and arg_list
                and get_node_evaluation_results(
                    method, graph, arg_list, {"authContext", "anonymous"}
                )
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f107.anonymous_ldap",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
