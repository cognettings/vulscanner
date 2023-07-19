from collections.abc import (
    Iterator,
)
from lib.root.f008.common import (
    unsafe_xss_content_nodes,
)
from model import (
    core,
)
from model.core import (
    MethodsEnum,
)
from model.graph import (
    GraphShard,
    GraphShardNode,
    MethodSupplies,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def js_unsafe_xss_content(
    shard: GraphShard, method_supplies: MethodSupplies
) -> core.Vulnerabilities:
    method = MethodsEnum.JS_UNSAFE_XSS_CONTENT

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in unsafe_xss_content_nodes(graph, method, method_supplies):
            yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f008.insec_addheader_write",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
