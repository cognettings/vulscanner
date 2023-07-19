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


def dart_insecure_logging(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.DART_INSECURE_LOGGING
    log_members = {"log", "logger"}
    log_methods = {
        "fine",
        "finest",
        "config",
        "info",
        "warning",
        "severe",
        "shout",
    }

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            n_expr = graph.nodes[nid]["expression"].split(".")
            if (
                n_expr[0] in log_members
                and (len(n_expr) == 1 or n_expr[1] in log_methods)
                and get_node_evaluation_results(
                    method, graph, nid, {"usesLogger"}
                )
            ):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f091.log_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
