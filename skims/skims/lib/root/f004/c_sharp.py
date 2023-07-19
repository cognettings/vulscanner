from collections.abc import (
    Iterator,
)
from lib.root.utilities.common import (
    check_methods_expression,
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


def c_sharp_remote_command_execution(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_REMOTE_COMMAND_EXECUTION
    danger_p1 = {"UserConnection", "UserParams"}
    danger_p2 = {"Executor", "UserConnection", "UserParams"}
    danger_methods = {"Start", "Execute"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            expression = graph.nodes[node]["expression"].split(".")[-1].lower()
            if check_methods_expression(graph, node, danger_methods) and (
                (
                    expression == "start"
                    and get_node_evaluation_results(
                        method,
                        graph,
                        node,
                        danger_p1,
                        False,
                        graph_db=method_supplies.graph_db,
                    )
                )
                or (
                    expression == "execute"
                    and get_node_evaluation_results(
                        method,
                        graph,
                        node,
                        danger_p2,
                        False,
                        graph_db=method_supplies.graph_db,
                    )
                )
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f004.remote_command_execution",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
