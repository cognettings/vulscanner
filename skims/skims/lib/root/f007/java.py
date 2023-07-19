from collections.abc import (
    Iterator,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
    GraphShard,
    GraphShardNode,
    MethodSupplies,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils import (
    graph as g,
)


def java_csrf_protections_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    csrf_methods = {"disable", "ignoringAntMatchers"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            expr_id = graph.nodes[node]["expression_id"]
            if (
                graph.nodes[expr_id].get("symbol") == "csrf"
                and (parent_id := g.pred_ast(graph, node)[0])
                and (expr_id := graph.nodes[parent_id].get("expression_id"))
                and graph.nodes[expr_id].get("symbol") in csrf_methods
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f007.csrf_protections_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_CSRF_PROTECTIONS_DISABLED,
    )
