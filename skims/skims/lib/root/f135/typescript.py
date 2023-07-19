from collections.abc import (
    Iterator,
)
from lib.root.f135.common import (
    insecure_http_headers,
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


def ts_insecure_http_headers(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TS_UNSAFE_HTTP_XSS_PROTECTION

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            if insecure_http_headers(graph, n_id, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f135.ts_unsafe_http_xss_protection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
