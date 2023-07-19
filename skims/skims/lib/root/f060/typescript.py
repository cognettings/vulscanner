from collections.abc import (
    Iterator,
)
from lib.root.f060.common import (
    has_dangerous_param,
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


def unsafe_origin(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TS_UNSAFE_ORIGIN

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in has_dangerous_param(graph, method_supplies):
            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f060.common_unsafe_origin",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
