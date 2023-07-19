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
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def is_node_danger(
    method: MethodsEnum,
    graph: Graph,
    n_id: NId,
    method_supplies: MethodSupplies,
) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(
            method, graph, path, n_id, graph_db=method_supplies.graph_db
        )
        if (
            evaluation
            and evaluation.danger
            and evaluation.triggers != {"SafeRegex"}
            and evaluation.triggers == {"UserParams", "HttpParams"}
        ):
            return True
    return False


def java_vuln_regular_expression(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_VULN_REGEX
    regex_methods = {"matches"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if (
                graph.nodes[node].get("expression") in regex_methods
                and (al_id := g.match_ast_d(graph, node, "ArgumentList"))
                and (args_nids := g.adj_ast(graph, al_id))
                and len(args_nids) >= 1
                and is_node_danger(method, graph, node, method_supplies)
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f211.regex_vulnerable",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
