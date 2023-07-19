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


def check_danger_arguments(graph: Graph, n_id: NId) -> bool:
    nodes = graph.nodes
    if (
        (args_n_id := nodes[n_id].get("arguments_id"))
        and (args := g.adj_ast(graph, args_n_id))
        and (len(args) > 0 and len(args) % 2 == 0)
    ):
        for index in range(0, len(args), 2):
            if (nodes[args[index]].get("value")[1:-1] == "Accept") and (
                nodes[args[index + 1]].get("value")[1:-1] == "*/*"
            ):
                return True
    return False


def get_dang_instances(graph: Graph) -> set[str]:
    def predicate_matcher(node: dict[str, str]) -> bool:
        return bool(
            (
                (node.get("label_type") == "VariableDeclaration")
                and (node.get("variable_type") in dang_classes)
            )
            or (
                (node.get("label_type") == "ObjectCreation")
                and (node.get("name") in dang_classes)
            )
        )

    dang_instances: set[str] = set()
    dang_classes = {"HttpClient", "HttpRequestMessage", "WebClient"}

    for n_id in g.filter_nodes(graph, graph.nodes, predicate_matcher):
        if (var_name := graph.nodes[n_id].get("variable")) or (
            (p_id := g.pred_ast(graph, n_id))
            and (v_id := graph.nodes[p_id[0]].get("variable_id"))
            and (var_name := graph.nodes[v_id].get("symbol"))
        ):
            dang_instances.add(var_name)

    return dang_instances


def get_dang_callings(graph: Graph) -> set[str]:
    dang_callings: set[str] = set()
    dang_invocations = {
        "DefaultRequestHeaders.Add",
        "DefaultRequestHeaders.Accept.Add",
        "Headers.Add",
        "Headers.Accept.Add",
    }
    for invocation in dang_invocations:
        for inst_name in get_dang_instances(graph):
            dang_callings.add(f"{inst_name}.{invocation}")

    return dang_callings


def c_sharp_accepts_any_mime_type(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.C_SHARP_ACCEPTS_ANY_MIMETYPE

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        dang_callings = get_dang_callings(graph)
        for node in method_supplies.selected_nodes:
            if (
                graph.nodes[node].get("expression") in dang_callings
                and (args_id := graph.nodes[node].get("arguments_id"))
                and get_node_evaluation_results(
                    method,
                    graph,
                    args_id,
                    set(),
                    graph_db=method_supplies.graph_db,
                )
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_http.analyze_headers.accept.insecure",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
