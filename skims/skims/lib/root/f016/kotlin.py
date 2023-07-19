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


def kt_default_http_client_deprecated(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.KT_DEFAULT_HTTP_CLIENT_DEPRECATED
    danger_methods = {"DefaultHttpClient"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]

            if n_attrs["expression"] in danger_methods:
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f016.default_http_client_deprecated",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
