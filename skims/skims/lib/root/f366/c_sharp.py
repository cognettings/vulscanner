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
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def is_danger_class_in_path(graph: Graph, method_id: NId) -> bool:
    for path in get_backward_paths(graph, method_id):
        class_nodes = [
            n_id for n_id in path if graph.nodes[n_id]["label_type"] == "Class"
        ]
        if any(
            get_action_filter(graph, n_id, "SecurityCritical")
            for n_id in class_nodes
        ):
            return True
    return False


def get_action_filter(graph: Graph, n_id: NId, filter_name: str) -> NId | None:
    if attr_list_ids := g.match_ast_group_d(graph, n_id, "Modifiers"):
        for attr_id in attr_list_ids:
            if f_node := g.adj_ast(graph, attr_id)[0]:
                if (
                    f_name := graph.nodes[f_node].get("name")
                ) and f_name == filter_name:
                    return f_node
    return None


def conflicting_annotations(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_CONFLICTING_ANNOTATIONS
    dang_filter = "SecuritySafeCritical"

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            if (
                filter_node := get_action_filter(graph, n_id, dang_filter)
            ) and is_danger_class_in_path(graph, n_id):
                yield shard, filter_node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f366.conflicting_transparency_annotations",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
