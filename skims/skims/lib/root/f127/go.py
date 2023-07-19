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


def go_insecure_query_float(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.GO_INSECURE_QUERY_FLOAT
    danger_methods = {
        "Exec",
        "ExecContext",
        "Query",
        "QueryContext",
        "QueryRow",
        "QueryRowContext",
    }

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            m_name = graph.nodes[n_id]["expression"].split(".")
            if (
                m_name[-1] in danger_methods
                and (al_id := graph.nodes[n_id].get("arguments_id"))
                and get_node_evaluation_results(
                    method, graph, al_id, {"userconnection"}
                )
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f127.type_confusion",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
