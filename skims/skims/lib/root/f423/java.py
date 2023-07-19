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
    Graph,
    GraphShard,
    GraphShardNode,
    MethodSupplies,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils import (
    graph as g,
)


def get_parent_method_name(graph: Graph, n_id: str) -> str:
    parent = g.pred_ast(graph, n_id)[0]
    while graph.nodes[parent].get("label_type") != "MethodDeclaration":
        get_nodes = g.pred_ast(graph, parent)
        if get_nodes:
            parent = get_nodes[0]
        else:
            return "no_method_found"

    return graph.nodes[parent]["name"]


def uses_exit_method(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_USES_SYSTEM_EXIT
    exit_methods = {
        "System.exit",
        "Runtime.getRuntime.exit",
        "Runtime.getRuntime.halt",
    }

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            m_name = concatenate_name(graph, nid)
            if (
                get_parent_method_name(graph, nid) != "main"
                and m_name in exit_methods
            ):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f423.uses_system_exit",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
