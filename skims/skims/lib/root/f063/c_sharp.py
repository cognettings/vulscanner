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
    evaluate,
    get_node_evaluation_results,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def is_node_vuln(
    graph: Graph,
    n_id: NId,
    method: MethodsEnum,
    danger_set: set[str],
    method_supplies: MethodSupplies,
) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(
            method, graph, path, n_id, method_supplies.graph_db
        )
        if (
            evaluation
            and evaluation.danger
            and evaluation.triggers == danger_set
        ):
            return True
    return False


def c_sharp_open_redirect(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_OPEN_REDIRECT

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get("expression") == "Response" and (
                graph.nodes[node].get("member") == "Redirect"
                and (pred := g.pred_ast(graph, node)[0])
                and get_node_evaluation_results(
                    method,
                    graph,
                    pred,
                    set(),
                    graph_db=method_supplies.graph_db,
                )
            ):
                yield shard, pred

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f063.c_sharp_open_redirect",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_unsafe_path_traversal(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_UNSAFE_PATH_TRAVERSAL
    danger_methods = {
        "File.Copy",
        "File.Create",
        "File.Delete",
        "File.Exists",
        "File.Move",
        "File.Open",
        "File.Replace",
    }
    danger_set = {"userconnection", "userparameters"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if check_methods_expression(
                graph, node, danger_methods
            ) and is_node_vuln(
                graph, node, method, danger_set, method_supplies
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f063_path_traversal.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
