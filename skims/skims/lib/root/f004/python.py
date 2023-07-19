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
from utils import (
    graph as g,
)


def is_danger_shell(
    graph: Graph,
    n_ids: list[NId],
    method: MethodsEnum,
    method_supplies: MethodSupplies,
) -> bool:
    for _id in n_ids:
        if graph.nodes[_id]["argument_name"] != "shell":
            continue
        val_id = graph.nodes[_id]["value_id"]
        return get_node_evaluation_results(
            method, graph, val_id, set(), graph_db=method_supplies.graph_db
        )
    return False


def is_danger_expression(
    graph: Graph,
    n_id: NId,
    method: MethodsEnum,
    method_supplies: MethodSupplies,
) -> bool:
    m_attrs = graph.nodes[n_id]
    expr: str = m_attrs["expression"]
    al_id = m_attrs.get("arguments_id")
    if not al_id:
        return False
    args_ids = list(g.adj_ast(graph, al_id))

    if (
        expr.startswith("os.")
        and get_node_evaluation_results(
            method,
            graph,
            args_ids[0],
            {"userparams"},
            graph_db=method_supplies.graph_db,
        )
    ) or (
        len(args_ids) > 1
        and is_danger_shell(graph, args_ids[1:], method, method_supplies)
        and get_node_evaluation_results(
            method,
            graph,
            args_ids[0],
            {"userparams"},
            graph_db=method_supplies.graph_db,
        )
    ):
        return True
    return False


def python_remote_command_execution(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_REMOTE_COMMAND_EXECUTION
    danger_set = {"os.popen", "subprocess.Popen"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node][
                "expression"
            ] in danger_set and is_danger_expression(
                graph, node, method, method_supplies
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f004.remote_command_execution",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
