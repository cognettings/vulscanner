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
from utils import (
    graph as g,
)


def is_unsafe_param(graph: Graph, n_id: NId) -> bool:
    if (
        (al_id := graph.nodes[n_id].get("arguments_id"))
        and (childs := g.adj_ast(graph, al_id))
        and len(childs) > 0
        and (member := graph.nodes[childs[0]].get("member"))
    ):
        return member == "CLEARTEXT"
    return False


def kt_unencrypted_channel(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    danger_methods = {"FTPClient", "SMTPClient", "TelnetClient"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            if n_attrs["expression"] in danger_methods or (
                n_attrs["expression"] == "ConnectionSpec.Builder"
                and is_unsafe_param(graph, node)
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f332.unencrypted_channel",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.KT_UNENCRYPTED_CHANNEL,
    )
