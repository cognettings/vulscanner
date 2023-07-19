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
import re
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils import (
    graph as g,
)


def get_vuln_nodes(graph: Graph, n_id: NId) -> bool:
    if args_n_id := g.match_ast_d(graph, n_id, "ArgumentList"):
        args_values = set()
        for arg_n_id in g.adj(graph, args_n_id):
            if (graph.nodes[arg_n_id].get("label_type") == "Literal") and (
                val := graph.nodes[arg_n_id].get("value")
            ):
                args_values.add(val.lower()[1:-1])
        if args_values == {"accept", "*/*"}:
            return True
    return False


def kt_accepts_any_mime_type(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.KOTLIN_ACCEPTS_ANY_MIME_TYPE
    method_re = re.compile(r"^\w+\.setRequestProperty$")

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            if (
                (expr := graph.nodes[n_id].get("expression"))
                and method_re.match(expr)
                and get_vuln_nodes(graph, n_id)
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_http.analyze_headers.accept.insecure",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
