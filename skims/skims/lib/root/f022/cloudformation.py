from collections.abc import (
    Iterator,
)
from lib.root.utilities.json import (
    is_parent,
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


def cfn_server_port_insecure_channel(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_HTTP_GET_INSECURE_CHANNELS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            key_id = graph.nodes[nid]["key_id"]
            value_id = graph.nodes[nid]["value_id"]

            if (
                graph.nodes[key_id]["value"] == "protocol"
                and graph.nodes[value_id].get("value") in {"http", "HTTP"}
                and is_parent(graph, nid, ["port", "servers"])
            ):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="f022.http_insecure_channel",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
