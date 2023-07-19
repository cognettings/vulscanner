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


def kotlin_weak_random(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.KT_WEAK_RANDOM

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            expr = graph.nodes[n_id]["expression"].split(".")[-1]
            if (
                expr in {"SecureRandom", "setSeed"}
                and (ar_id := graph.nodes[n_id].get("arguments_id"))
                and (test_node := g.match_ast(graph, ar_id).get("__0__"))
                and get_node_evaluation_results(
                    method, graph, test_node, set()
                )
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="f034.use_insecure_random_method",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
