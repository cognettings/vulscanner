from collections.abc import (
    Iterator,
)
from dynamodb.types import (
    Item,
)
from lib.root.utilities.common import (
    check_methods_expression,
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


def is_session_vuln(
    method: MethodsEnum,
    graph: Graph,
    session_args: tuple[NId, ...],
    method_supplies: MethodSupplies,
) -> bool:
    if get_node_evaluation_results(
        method,
        graph,
        session_args[0],
        {"hostkey"},
        graph_db=method_supplies.graph_db,
    ) and get_node_evaluation_results(
        method,
        graph,
        session_args[1],
        {"disablecheck"},
        graph_db=method_supplies.graph_db,
    ):
        return True
    return False


def check_vulnerability_results(
    method: MethodsEnum,
    graph: Graph,
    n_attrs: Item,
    method_supplies: MethodSupplies,
) -> bool:
    if (
        get_node_evaluation_results(
            method,
            graph,
            n_attrs["object_id"],
            {"sshSession", "jshObject"},
            graph_db=method_supplies.graph_db,
        )
        and (al_list := n_attrs.get("arguments_id"))
        and (args_nodes := g.adj_ast(graph, al_list))
        and len(args_nodes) == 2
        and is_session_vuln(method, graph, args_nodes, method_supplies)
    ):
        return True
    return False


def java_host_key_checking(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_HOST_KEY_CHECKING
    danger_methods = {"setConfig"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            if check_methods_expression(
                graph, node, danger_methods
            ) and check_vulnerability_results(
                method, graph, n_attrs, method_supplies
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f368.insecure_host_key_checking",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
