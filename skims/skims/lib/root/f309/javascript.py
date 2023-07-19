from collections.abc import (
    Iterator,
)
from lib.root.f309.common import (
    is_insecure_jwt,
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


def js_insecure_jwt_token(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JS_INSECURE_JWT_TOKEN
    jwt_methods = {"sign", "verify"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get(
                "expression"
            ) in jwt_methods and is_insecure_jwt(graph, nid, method):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f309.js_uses_insecure_jwt_token",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
