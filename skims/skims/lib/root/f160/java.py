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
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)
from utils.string import (
    complete_attrs_on_set,
    split_on_last_dot as split_last,
)


def validate_import(graph: Graph, check: str) -> Iterator[str]:
    for node in g.matching_nodes(graph, label_type="Import"):
        form, _ = split_last(graph.nodes[node].get("expression"))
        yield form + "." + check


def is_secure(options: Iterator[str], pattern: set[str]) -> bool:
    if any(library in pattern for library in options):
        return True
    return False


def is_method_danger(
    graph: Graph, n_id: NId, method_supplies: MethodSupplies
) -> bool:
    method = MethodsEnum.JAVA_CREATE_TEMP_FILE
    lib = {"java.nio.file.Files.createTempFile"}
    exp = graph.nodes[n_id].get("expression")

    if obj := graph.nodes[n_id].get("object_id"):
        imp_check = graph.nodes[obj].get("symbol") + "." + exp
    else:
        imp_check = exp

    lib_safe = is_secure(validate_import(graph, imp_check), lib)
    if not lib_safe:
        return True

    if (
        (al_id := graph.nodes[n_id].get("arguments_id"))
        and (test_nid := g.match_ast(graph, al_id).get("__1__"))
        and get_node_evaluation_results(
            method, graph, test_nid, set(), graph_db=method_supplies.graph_db
        )
    ):
        return True
    return False


def java_file_create_temp_file(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    danger_methods = complete_attrs_on_set({"java.io.File.createTempFile"})
    method = MethodsEnum.JAVA_CREATE_TEMP_FILE

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if check_methods_expression(
                graph, node, danger_methods
            ) and is_method_danger(graph, node, method_supplies):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f160.java_file_create_temp_file",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
