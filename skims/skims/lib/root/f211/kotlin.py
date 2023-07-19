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


def is_node_danger(method: MethodsEnum, graph: Graph, n_id: NId) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if (
            evaluation
            and evaluation.danger
            and evaluation.triggers != {"SafeRegex"}
            and evaluation.triggers == {"UserParams", "HttpParams"}
        ):
            return True
    return False


def kt_vuln_regular_expression(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.KOTLIN_VULN_REGEX

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            expression_id = graph.nodes[nid]["expression_id"]

            if (
                graph.nodes[expression_id].get("member") == "matches"
                and (al_id := g.match_ast_d(graph, nid, "ArgumentList"))
                and (args_nids := g.adj_ast(graph, al_id))
                and len(args_nids) >= 1
                and is_node_danger(method, graph, nid)
            ):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f211.regex_vulnerable",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
