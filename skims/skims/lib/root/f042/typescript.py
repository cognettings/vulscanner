from collections.abc import (
    Iterator,
)
from lib.root.f042.common import (
    is_insecure_cookie,
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


def insecurely_generated_cookies(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSEC_COOKIES

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for nid in is_insecure_cookie(graph, method, method_supplies):
            yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f042.java_insecure_set_cookies.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
