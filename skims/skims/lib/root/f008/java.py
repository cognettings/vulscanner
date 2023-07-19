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


def is_xss_content_creation(
    method: MethodsEnum,
    graph: Graph,
    method_id: NId,
    obj_id: NId,
    method_supplies: MethodSupplies,
) -> bool:
    danger_set1 = {"userconnection", "userparameters"}
    danger_set2 = {"userresponse"}
    al_id = graph.nodes[method_id].get("arguments_id")
    response_id = graph.nodes[obj_id].get("object_id")
    if not (al_id and response_id):
        return False

    if get_node_evaluation_results(
        method, graph, al_id, danger_set1, False, method_supplies.graph_db
    ) and get_node_evaluation_results(
        method,
        graph,
        response_id,
        danger_set2,
        False,
        method_supplies.graph_db,
    ):
        return True
    return False


def java_unsafe_xss_content(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_UNSAFE_XSS_CONTENT
    danger_methods = {"format", "write", "println", "printf", "print"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            if (
                n_attrs["expression"] in danger_methods
                and (obj_id := n_attrs.get("object_id"))
                and graph.nodes[obj_id].get("expression") == "getWriter"
                and is_xss_content_creation(
                    method, graph, node, obj_id, method_supplies
                )
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f008.insec_addheader_write",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
