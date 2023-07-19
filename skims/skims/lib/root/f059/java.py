from collections.abc import (
    Iterator,
)
from lib.root.utilities.java import (
    concatenate_name,
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


def java_sensitive_log_info(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_SENSITIVE_INFO_IN_LOGS
    danger_methods = {"logger.info", "log.debug", "log.info"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            method_name = concatenate_name(graph, node)
            if (
                method_name.lower() in danger_methods
                and (al_id := graph.nodes[node].get("arguments_id"))
                and get_node_evaluation_results(
                    method,
                    graph,
                    al_id,
                    {"sensitiveinfo"},
                    graph_db=method_supplies.graph_db,
                )
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f059.java_sensitive_info_logs",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
