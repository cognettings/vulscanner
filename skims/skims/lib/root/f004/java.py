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


def java_remote_command_1(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_REMOTE_COMMAND_EXECUTION
    danger_set = {"pbuilder", "userparams", "userconnection"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            if (
                n_attrs["expression"] == "start"
                and not n_attrs.get("arguments_id")
                and get_node_evaluation_results(
                    method,
                    graph,
                    n_attrs["object_id"],
                    danger_set,
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


def java_remote_command_2(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_REMOTE_COMMAND_EXECUTION
    danger_set = {"userparams", "userconnection"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            if (
                n_attrs["expression"] == "exec"
                and get_node_evaluation_results(
                    method,
                    graph,
                    n_attrs["object_id"],
                    {"runtime"},
                    graph_db=method_supplies.graph_db,
                )
                and (al_id := n_attrs.get("arguments_id"))
                and get_node_evaluation_results(
                    method,
                    graph,
                    al_id,
                    danger_set,
                    False,
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
