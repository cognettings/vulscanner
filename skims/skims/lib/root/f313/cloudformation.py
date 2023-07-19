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


def cfn_insecure_certificate(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_INSECURE_CERTIFICATE

    def n_ids() -> Iterator[GraphShardNode]:
        """
        Source:
        https://nodejs.org/api/cli.html#node_tls_reject_unauthorizedvalue
        """
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            key_id = graph.nodes[nid]["key_id"]
            value_id = graph.nodes[nid]["value_id"]

            if (
                graph.nodes[key_id]["value"] == "NODE_TLS_REJECT_UNAUTHORIZED"
                and graph.nodes[value_id].get("value") == "0"
                and is_parent(
                    graph,
                    nid,
                    [
                        "environment",
                    ],
                )
            ):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f313.unsafe_certificate_validation",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
