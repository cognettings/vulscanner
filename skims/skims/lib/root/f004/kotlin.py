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
import utils.graph as g


def kt_remote_command_exec(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.KT_REMOTE_COMMAND_EXECUTION
    danger_methods = {"loadLibrary", "exec"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            parent = g.pred_ast(graph, node)
            arg_list = graph.nodes[parent[0]].get("arguments_id")

            if (
                n_attrs["member"] in danger_methods
                and (child := g.adj_ast(graph, node)[0])
                and get_node_evaluation_results(
                    method,
                    graph,
                    child,
                    {"getRuntime"},
                    graph_db=method_supplies.graph_db,
                )
                and arg_list
                and get_node_evaluation_results(
                    method,
                    graph,
                    arg_list,
                    {"UserConnection"},
                    graph_db=method_supplies.graph_db,
                )
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f004.remote_command_execution",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
