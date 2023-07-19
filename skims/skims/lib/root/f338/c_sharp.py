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
from utils.graph import (
    adj_ast,
)


def check_hashes_salt(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_CHECK_HASHES_SALT

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            if (
                n_attrs.get("name") == "Rfc2898DeriveBytes"
                and (al_id := n_attrs.get("arguments_id"))
                and (args_nids := adj_ast(graph, al_id))
                and len(args_nids) >= 2
                and get_node_evaluation_results(
                    method,
                    graph,
                    args_nids[1],
                    {
                        "hardcode_salt",
                    },
                )
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="f338.salt_is_hardcoded",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
