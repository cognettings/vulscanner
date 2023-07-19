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
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from symbolic_eval.utils import (
    get_forward_paths,
)
from utils import (
    graph as g,
)


def no_size_limit(
    method: MethodsEnum, graph: Graph, parent: str, var_name: str
) -> bool:
    for path in get_forward_paths(graph, parent):
        for n_id in g.filter_nodes(
            graph,
            nodes=path,
            predicate=g.pred_has_labels(label_type="MethodInvocation"),
        ):
            n_attrs = graph.nodes[n_id]
            if (
                n_attrs["expression"] == "setMaxUploadSize"
                and (symbol_id := n_attrs.get("object_id"))
                and graph.nodes[symbol_id]["symbol"] == var_name
            ):
                return get_node_evaluation_results(method, graph, n_id, set())
    return True


def get_vuln_nodes(
    method: MethodsEnum, graph: Graph, selected_nodes: list[str]
) -> list[str]:
    danger_objs = {"CommonsMultipartResolver", "MultipartConfigFactory"}
    vuln_nodes: list[str] = []
    for n_id in selected_nodes:
        n_name = graph.nodes[n_id].get("name")

        if n_name in danger_objs:
            parent = g.pred_ast(graph, n_id)[0]
            var_name = graph.nodes[parent].get("variable")
            if no_size_limit(method, graph, parent, var_name):
                vuln_nodes.append(parent)
    return vuln_nodes


def java_insecure_file_upload_size(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_UPLOAD_SIZE_LIMIT

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in get_vuln_nodes(
            method, graph, method_supplies.selected_nodes
        ):
            yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f354.java_upload_size_limit",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
