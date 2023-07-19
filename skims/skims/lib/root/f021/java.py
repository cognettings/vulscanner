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


def java_unsafe_xpath_injection(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_XPATH_INJECTION_EVALUATE
    danger_methods = {"evaluate"}
    danger_set = {"userparameters", "userconnection"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            if n_attrs[
                "expression"
            ] in danger_methods and get_node_evaluation_results(
                method,
                graph,
                node,
                danger_set,
                False,
                method_supplies.graph_db,
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f021.xpath_injection_evaluate",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
