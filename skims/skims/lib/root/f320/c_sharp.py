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
from utils import (
    graph as g,
)


def c_sharp_ldap_connections_authenticated(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_LDAP_CONN_AUTH

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            parent_id = g.pred_ast(graph, node)[0]
            if (
                n_attrs["member"] == "AuthenticationType"
                and (val_id := graph.nodes[parent_id].get("value_id"))
                and get_node_evaluation_results(
                    method,
                    graph,
                    n_attrs["expression_id"],
                    set(),
                    graph_db=method_supplies.graph_db,
                )
                and get_node_evaluation_results(
                    method,
                    graph,
                    val_id,
                    {"danger_auth"},
                    graph_db=method_supplies.graph_db,
                )
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f320.authenticated_ldap_connections",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_ldap_connections_directory(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_LDAP_CONN_AUTH

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            if (
                n_attrs["name"] == "DirectoryEntry"
                and (al_id := n_attrs.get("arguments_id"))
                and get_node_evaluation_results(
                    method,
                    graph,
                    al_id,
                    {"danger_auth"},
                    graph_db=method_supplies.graph_db,
                )
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f320.authenticated_ldap_connections",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
