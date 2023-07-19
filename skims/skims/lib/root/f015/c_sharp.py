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
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)


def c_sharp_insecure_authentication(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSECURE_AUTHENTICATION

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            if (
                n_attrs["expression"].endswith("Headers.Add")
                and (al_id := n_attrs.get("arguments_id"))
                and get_node_evaluation_results(
                    method,
                    graph,
                    n_attrs["expression_id"],
                    {"webreq"},
                    graph_db=method_supplies.graph_db,
                )
                and (arg_id := g.match_ast(graph, al_id).get("__1__"))
                and get_node_evaluation_results(
                    method,
                    graph,
                    arg_id,
                    {"basicauth"},
                    graph_db=method_supplies.graph_db,
                )
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f015.insecure_authentication",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
