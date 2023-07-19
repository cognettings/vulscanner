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


def c_sharp_ldap_injection(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_LDAP_INJECTION
    danger_methods = {"FindOne", "FindAll"}
    danger_params = {"directorysearcher", "userparameters", "userconnection"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for node in method_supplies.selected_nodes:
            expr = graph.nodes[node]["expression"].split(".")
            if expr[-1] in danger_methods and get_node_evaluation_results(
                method,
                graph,
                node,
                danger_params,
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f107.ldap_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
