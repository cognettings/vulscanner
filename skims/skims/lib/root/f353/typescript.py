from collections.abc import (
    Iterator,
)
from lib.root.f353.common import (
    insecure_jwt_decode,
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


def decode_insecure_jwt_token(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TS_DECODE_INSECURE_JWT_TOKEN

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            if (
                graph.nodes[n_id].get("expression") == "decode"
                and graph.nodes[n_id].get("member") == "jwt"
                and insecure_jwt_decode(graph, n_id)
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f353.js_decode_insecure_jwt_token",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
