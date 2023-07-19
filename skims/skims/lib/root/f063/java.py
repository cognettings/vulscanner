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
    evaluate,
    get_node_evaluation_results,
)
from symbolic_eval.types import (
    Path,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def has_cannonical_check(graph: Graph, file_name: str, path: Path) -> bool:
    for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
        n_attrs = graph.nodes[n_id]
        if (
            n_attrs["expression"] == "getCanonicalPath"
            and (obj_id := graph.nodes[n_id].get("object_id"))
            and graph.nodes[obj_id].get("symbol") == file_name
            and g.pred(graph, n_id)[0] in path
        ):
            return True
    return False


def is_argument_danger(
    graph: Graph,
    n_id: NId,
    method: MethodsEnum,
    method_supplies: MethodSupplies,
) -> bool:
    symbol = graph.nodes[n_id].get("symbol")
    for path in get_backward_paths(graph, n_id):
        if (
            (
                evaluation := evaluate(
                    method, graph, path, n_id, method_supplies.graph_db
                )
            )
            and evaluation.danger
            and evaluation.triggers == {"ZipFile"}
            and not has_cannonical_check(graph, symbol, path)
        ):
            return True
    return False


def java_zip_slip_injection(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_ZIP_SLIP_PATH_INJECTION
    danger_methods = {"readFileToString"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            if (
                n_attrs["expression"] in danger_methods
                and (al_id := n_attrs.get("arguments_id"))
                and (test_id := g.match_ast(graph, al_id).get("__0__"))
                and is_argument_danger(graph, test_id, method, method_supplies)
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f063.zip_slip_path_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def java_unsafe_path_traversal(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_UNSAFE_PATH_TRAVERSAL
    danger_obj = {
        "java.io.File",
        "java.io.FileInputStream",
        "java.io.FileOutputStream",
    }

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            if (
                n_attrs.get("name") in danger_obj
                and (args_id := n_attrs.get("arguments_id"))
                and (al_id := g.adj_ast(graph, args_id))
                and len(al_id) >= 1
                and get_node_evaluation_results(
                    method,
                    graph,
                    al_id[0],
                    {"userparameters", "userconnection"},
                    graph_db=method_supplies.graph_db,
                )
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f063_path_traversal.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
