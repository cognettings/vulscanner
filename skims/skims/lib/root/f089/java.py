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


def is_danger_request(
    method: MethodsEnum,
    graph: Graph,
    obj_id: NId,
    method_supplies: MethodSupplies,
) -> bool:
    n_attrs = graph.nodes[obj_id]
    if (
        n_attrs.get("expression") == "getSession"
        and (sess_id := n_attrs.get("object_id"))
        and get_node_evaluation_results(
            method,
            graph,
            sess_id,
            {"userconnection"},
            graph_db=method_supplies.graph_db,
        )
    ):
        return True
    return False


def java_trust_boundary_violation(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_TRUST_BOUNDARY_VIOLATION
    danger_methods = {"setAttribute", "putValue"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            if (
                n_attrs["expression"] in danger_methods
                and (obj_id := n_attrs.get("object_id"))
                and is_danger_request(method, graph, obj_id, method_supplies)
                and (al_id := graph.nodes[node].get("arguments_id"))
                and get_node_evaluation_results(
                    method,
                    graph,
                    al_id,
                    {"userparams", "userconnection"},
                    graph_db=method_supplies.graph_db,
                )
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f089.trust_boundary_violation",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
